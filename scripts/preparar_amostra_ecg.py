"""
Seleciona uma amostra determinística e reproduzível de imagens de ECG a partir do
dataset bruto "ECG Images dataset of Cardiac Patients" (Mendeley, Khan & Hussain,
DOI 10.17632/gwbz3fsgp8.2), remove duplicatas exatas (por hash SHA-256), aplica
o crop de remoção do cabeçalho administrativo (região 0-283px, validada
visualmente em amostras das 4 classes) e grava o resultado em assets/imagens/ecg/,
junto com o manifesto de rastreabilidade em document/other/fontes_parte3/.

Fonte bruta (não incluída no repositório): pasta local informada em RAW_DIR.
Ajuste RAW_DIR para o caminho onde o dataset bruto do Mendeley Data foi baixado
e extraído na sua máquina antes de executar este script.
"""

import csv
import hashlib
import random
from pathlib import Path

from PIL import Image

RAW_DIR = Path("ecg_dataset_mendeley")  # ajuste para o caminho local do dataset bruto extraído
OUT_DIR = Path("assets/imagens/ecg")
MANIFEST_PATH = Path("document/other/fontes_parte3/manifesto_amostra.csv")

CROP_TOP = 283  # remove cabeçalho administrativo (ID, data/hora, dados demográficos)

CLASSES = {
    "myocardial_infarction": {
        "raw_folder": "ECG Images of Myocardial Infarction Patients (240x12=2880)",
        "prefix": "mi",
        "n_select": 30,
    },
    "abnormal_heartbeat": {
        "raw_folder": "ECG Images of Patient that have abnormal heartbeat (233x12=2796)",
        "prefix": "ahb",
        "n_select": 30,
    },
    "history_mi": {
        "raw_folder": "ECG Images of Patient that have History of MI (172x12=2064)",
        "prefix": "hmi",
        "n_select": 30,
    },
    "normal": {
        "raw_folder": "Normal Person ECG Images (284x12=3408)",
        "prefix": "normal",
        "n_select": 30,
    },
}

RANDOM_STATE = 42


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unique_files_by_hash(folder: Path) -> list[tuple[str, Path]]:
    """Retorna lista (hash, caminho) mantendo apenas o primeiro arquivo de cada hash,
    ordenado pelo nome do arquivo para garantir reprodutibilidade."""
    seen_hashes = {}
    for path in sorted(folder.iterdir()):
        if not path.is_file():
            continue
        h = sha256_of(path)
        if h not in seen_hashes:
            seen_hashes[h] = path
    return sorted(seen_hashes.items(), key=lambda item: item[1].name)


def main():
    manifest_rows = []

    for class_final, cfg in CLASSES.items():
        raw_folder = RAW_DIR / cfg["raw_folder"]
        unique = unique_files_by_hash(raw_folder)

        rng = random.Random(RANDOM_STATE)
        if len(unique) <= cfg["n_select"]:
            selected = unique
        else:
            selected = rng.sample(unique, cfg["n_select"])
            selected.sort(key=lambda item: item[1].name)

        out_class_dir = OUT_DIR / class_final
        out_class_dir.mkdir(parents=True, exist_ok=True)

        for idx, (file_hash, src_path) in enumerate(selected, start=1):
            final_name = f"{cfg['prefix']}_{idx:03d}.jpg"
            final_path = out_class_dir / final_name

            with Image.open(src_path) as im:
                im = im.convert("RGB")
                w, h = im.size
                cropped = im.crop((0, CROP_TOP, w, h))
                # remove EXIF/metadados: Image.crop já retorna uma imagem nova sem info,
                # e salvamos explicitamente sem parâmetro exif.
                cropped.save(final_path, format="JPEG", quality=95)

            manifest_rows.append({
                "classe_original": cfg["raw_folder"],
                "nome_arquivo_original": src_path.name,
                "hash_original": file_hash,
                "nome_arquivo_final": final_name,
                "classe_final": class_final,
                "transformacao_aplicada": f"crop remocao cabecalho administrativo (linhas 0-{CROP_TOP-1}px); conversao para RGB; remocao de metadados EXIF; sem redimensionamento",
            })

        print(f"{class_final}: {len(unique)} unicas disponiveis -> {len(selected)} selecionadas")

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "classe_original", "nome_arquivo_original", "hash_original",
            "nome_arquivo_final", "classe_final", "transformacao_aplicada",
        ])
        writer.writeheader()
        writer.writerows(manifest_rows)

    print(f"\nTotal selecionado: {len(manifest_rows)}")
    print(f"Manifesto gravado em: {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
