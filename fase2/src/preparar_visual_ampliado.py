"""Recupera versão 2 da fonte da Fase 1 sem alterar assets/.

Uso: python fase2/src/preparar_visual_ampliado.py --cache /tmp/cardioia-ecg-raw
Os originais contêm cabeçalhos: cache deve ficar FORA do repositório.
Derivados não são publicados automaticamente; exigem inspeção de privacidade.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import time
from urllib.request import Request, urlopen
from PIL import Image, ImageOps

RAIZ = Path(__file__).resolve().parents[2]
FOLDERS = {
 'myocardial_infarction': '1c51d4ad-07c4-45be-9e44-1f840ac3f379',
 'abnormal_heartbeat': '195dc2f1-0814-4a75-8704-a26b0df14a18',
 'history_mi': '4aa38605-c5a3-4802-816c-95ba8f6a3053',
 'normal': 'c796cd29-7f24-405a-81f9-0fbb7db63511',
}


def salvar_exemplos(destino, inventario):
    """Mantém uma miniatura sanitizada de cada classe para o repositório."""
    exemplos = destino / 'exemplos'
    exemplos.mkdir(parents=True, exist_ok=True)
    for classe in FOLDERS:
        item = next(valor for valor in inventario if valor['classe_original'] == classe)
        with Image.open(RAIZ / item['arquivo']) as imagem:
            imagem.thumbnail((192, 112), Image.Resampling.LANCZOS)
            imagem.save(exemplos / f'{classe}.png', optimize=True)
def abrir(url, timeout):
    return urlopen(Request(url, headers={'User-Agent': 'CardioIA-FIAP/2.0'}), timeout=timeout)


def baixar_bytes(url, tentativas=3):
    """Baixa com novas tentativas para tornar a reprodução menos frágil."""
    ultimo_erro = None
    for tentativa in range(tentativas):
        try:
            with abrir(url, 120) as response:
                return response.read()
        except Exception as erro:  # a fonte pública pode oscilar
            ultimo_erro = erro
            if tentativa + 1 < tentativas:
                time.sleep(2 ** tentativa)
    raise ultimo_erro

def preparar(cache):
    cache = Path(cache).resolve()
    if cache == RAIZ or RAIZ in cache.parents:
        raise ValueError('Cache de originais deve ficar fora do repositório.')
    cache.mkdir(parents=True, exist_ok=True)
    destino = RAIZ / 'fase2/dados/visual_ampliado'
    inventario, contagens, vistos = [], {}, {}
    for classe, folder in FOLDERS.items():
        with abrir(f'https://data.mendeley.com/public-api/datasets/gwbz3fsgp8/files?folder_id={folder}&version=2', 90) as response:
            arquivos = json.load(response)
        unicos = {}
        for item in arquivos:
            digest = item['content_details']['sha256_hash']
            if digest in vistos and vistos[digest] != classe:
                raise ValueError('Mesmo hash em classes diferentes; revisar antes de treinar.')
            vistos[digest] = classe
            unicos.setdefault(digest, item)
        contagens[classe] = dict(arquivos=len(arquivos), unicos=len(unicos))
        print(classe, contagens[classe], flush=True)
        def baixar(par):
            digest, item = par
            raw = cache / (digest + '.jpg')
            if not raw.exists():
                raw.write_bytes(baixar_bytes(item['content_details']['download_url']))
            if hashlib.sha256(raw.read_bytes()).hexdigest() != digest:
                raise ValueError('Hash do download não confere.')
            output = destino / classe / (digest + '.png')
            output.parent.mkdir(parents=True, exist_ok=True)
            with Image.open(raw) as img:
                if img.size != (2213, 1572):
                    raise ValueError('Layout divergente: revisar recorte administrativo.')
                # Remove cabeçalho identificável e rodapé com data/hora do exame.
                crop = ImageOps.grayscale(img.crop((0, 283, img.width, 1430)))
                crop = ImageOps.autocontrast(crop)
                crop.thumbnail((384, 224), Image.Resampling.LANCZOS)
                canvas = Image.new('L', (384, 224), 255)
                canvas.paste(crop, ((384-crop.width)//2, (224-crop.height)//2))
                canvas.save(output, optimize=True)
            return dict(arquivo=str(output.relative_to(RAIZ)), classe_original=classe,
                alvo=int(classe != 'normal'), hash_original=digest,
                hash_derivado=hashlib.sha256(output.read_bytes()).hexdigest())
        with ThreadPoolExecutor(max_workers=24) as pool:
            inventario.extend(pool.map(baixar, sorted(unicos.items())))
    output = RAIZ / 'fase2/auditoria/inventario_visual_ampliado.json'
    output.write_text(json.dumps(dict(fonte='10.17632/gwbz3fsgp8.2',
        contagens=contagens, imagens=inventario,
        aviso='Hashes não provam indivíduos distintos. Recortes exigem revisão visual antes de publicação.'), indent=2))
    salvar_exemplos(destino, inventario)
    return inventario

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cache', required=True)
    args = parser.parse_args()
    print('Total recuperado:', len(preparar(args.cache)))
