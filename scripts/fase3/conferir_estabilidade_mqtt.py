"""Observo conexão e atualidade separadamente, sem publicar leituras de teste."""
import argparse
import json
from pathlib import Path
import time
import urllib.request


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sessao', required=True)
    parser.add_argument('--duracao', type=float, default=100)
    parser.add_argument('--saida', type=Path, required=True)
    args = parser.parse_args()
    args.saida.mkdir(parents=True, exist_ok=True)
    initial_deadline = time.monotonic() + 180
    started = None
    samples = []
    previous = None
    while True:
        with urllib.request.urlopen('http://127.0.0.1:1880/cardioia/api/state', timeout=5) as response:
            view = json.load(response)
        if started is None:
            if view.get('session') != args.sessao or not view.get('lastSequence'):
                assert time.monotonic() < initial_deadline, 'Ainda nao recebi a primeira leitura da nova sessao.'
                time.sleep(1)
                continue
            started = time.monotonic()
            print('Iniciei observacao da sessao '+args.sessao, flush=True)
        assert view['session'] == args.sessao, 'A sessao mudou durante a observacao.'
        sample = {key: view.get(key) for key in ('mode', 'connection', 'broker', 'status', 'lastSequence', 'ageSeconds', 'ack')}
        sample['elapsed_seconds'] = round(time.monotonic() - started, 2)
        samples.append(sample)
        signature = (sample['mode'], sample['connection'], sample['lastSequence'])
        if signature != previous:
            print(json.dumps(sample), flush=True)
            previous = signature
        if time.monotonic() - started >= args.duracao:
            break
        time.sleep(1)
    (args.saida/'observacao.json').write_text(json.dumps(samples, indent=2)+'\n', encoding='utf-8')
    success = all(s['connection'] == 'online' and s['broker'] == 'connected' for s in samples)
    result = {'resultado': 'aprovado' if success else 'revisar', 'session_id': args.sessao,
              'duracao_observada_s': samples[-1]['elapsed_seconds'],
              'leituras_observadas': sorted({s['lastSequence'] for s in samples}),
              'modos_de_atualidade': sorted({s['mode'] for s in samples}),
              'interrupcoes_de_conexao': sum(s['connection'] != 'online' for s in samples)}
    (args.saida/'resultado.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result), flush=True)
    assert success, 'Observei interrupcao de conexao; mantenho a revisao pendente.'


if __name__ == '__main__':
    main()
