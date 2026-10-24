"""Copio a execução anterior para a área local e confiro os bancos, sem apagar a origem."""
import argparse
from contextlib import closing
import json
import os
from pathlib import Path
import shutil
import sqlite3

REPOSITORIO = Path(__file__).resolve().parents[2]


def conferir_banco(path):
    with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as db:
        if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError(f"Banco sem integridade: {path.name}")
        tables = [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        return {name: db.execute('SELECT COUNT(*) FROM "' + name.replace('"', '""') + '"').fetchone()[0] for name in tables}


def migrar(origem, destino):
    origem, destino = Path(origem).resolve(), Path(destino).resolve()
    for path in (origem, destino):
        if not path.is_relative_to(REPOSITORIO) or path == REPOSITORIO:
            raise ValueError("Mantenho origem e destino dentro deste projeto.")
    if origem == destino or origem in destino.parents or destino in origem.parents:
        raise ValueError("Uso diretórios separados para preservar a origem.")
    if not origem.is_dir():
        raise FileNotFoundError("Não encontrei a execução anterior.")
    if destino.exists():
        raise FileExistsError("O destino já existe; não sobrescrevo dados de outra execução.")
    temporario = destino.with_name(destino.name + ".em_migracao")
    if temporario.exists():
        raise FileExistsError("Preservo a tentativa anterior para conferência.")
    temporario.mkdir(parents=True)
    bancos, arquivos = {}, 0
    for directory, dirs, files in os.walk(origem, followlinks=False):
        base = Path(directory)
        dirs[:] = [name for name in dirs if name != "node_modules" and not (base / name).is_symlink() and not (base / name).is_junction()]
        target = temporario / base.relative_to(origem)
        target.mkdir(parents=True, exist_ok=True)
        for name in files:
            source = base / name
            if source.is_symlink() or name.endswith(("-wal", "-shm")):
                continue
            dest = target / name
            if source.suffix == ".sqlite3":
                with closing(sqlite3.connect(source.as_uri() + "?mode=ro", uri=True)) as old, closing(sqlite3.connect(dest)) as new:
                    old.backup(new)
                before, after = conferir_banco(source), conferir_banco(dest)
                if before != after:
                    raise ValueError("As contagens do banco divergiram; preservo a origem e a cópia para análise.")
                bancos[source.relative_to(origem).as_posix()] = before
            else:
                shutil.copy2(source, dest)
            arquivos += 1
    resultado = {"resultado": "aprovado", "origem": origem.relative_to(REPOSITORIO).as_posix(), "destino": destino.relative_to(REPOSITORIO).as_posix(), "arquivos_copiados": arquivos, "bancos": bancos, "origem_preservada": True}
    (temporario / "migracao.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporario.rename(destino)
    return resultado


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--origem", type=Path, default=REPOSITORIO / "fase3/runtime")
    parser.add_argument("--destino", type=Path, default=REPOSITORIO / ".tools/runtime/fase3")
    args = parser.parse_args()
    print(json.dumps(migrar(args.origem, args.destino), ensure_ascii=False, indent=2))
