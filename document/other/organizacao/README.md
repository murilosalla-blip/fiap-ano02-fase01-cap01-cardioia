# Nosso registro de organização do CardioIA

Organizamos o projeto conforme o [modelo FIAP](https://github.com/agodoi/templateFiapVfinal), revisão `50e1e2720637b222357a7ebd1919c38a44af7cd2`. Registramos a análise original em [analise_template_fiap.md](analise_template_fiap.md).

## Estrutura atual

Mantemos na raiz as pastas institucionais `.github`, `assets`, `config`, `document`, `scripts` e `src`, o README e os arquivos de controle do Git. Organizamos `fase1`, `fase2` e `fase3` dentro de `src`, `assets`, `config` e `document`. Agrupo o portal em `src/fase2/portal-cardioia`.

Retiramos as entradas transitórias `fase2/` e `fase3/` da raiz e preservamos seus arquivos no [histórico versionado](../historico/entradas_transitorias/). Mantemos os requisitos de publicação junto de `src/fase2/app.py`, por meio de `src/fase2/requirements.txt`, que aponta para `config/fase2/requirements.txt`. Confirmamos no perfil público do Streamlit que a publicação aponta para o fork `Julia-carvalho96/fiap-ano02-fase01-cap01-cardioia`, separado deste repositório. Preservamos esse vínculo; uma futura publicação a partir desta estrutura usa a entrada padronizada.

Migramos os bancos e logs para `.tools/runtime/fase3`, fora do Git, usando uma cópia consistente dos bancos SQLite. Mantemos o diretório de execução anterior em backup local. Registramos a revisão em [PADRONIZACAO_FASES.md](PADRONIZACAO_FASES.md).

## Preservação das entregas

Mantemos no README os 18 endereços externos originais, incluindo as três pastas do Drive da Fase 1 e a gravação da Fase 2 no YouTube. Registramos os endereços em [links_externos_preservados.json](links_externos_preservados.json).

Registramos os destinos dos 397 arquivos da primeira organização em [mapa_arquivos.json](mapa_arquivos.json). Preservamos o manifesto anterior da Fase 1 e os seus hashes em [preservacao_fase1.json](preservacao_fase1.json), conferindo o conteúdo original nas localizações atuais ou nas cópias históricas. Registramos as 191 renomeações desta revisão em [mudancas_padronizacao.json](mudancas_padronizacao.json).

Normalizo somente CRLF/LF na conferência de textos e mantemos binários íntegros. Preservamos as saídas anteriores dos notebooks e os mesmos projetos Wokwi. A publicação independente do portal continua em seu próprio repositório.

## Como verificar

```powershell
python scripts/validar_organizacao.py
python scripts/fase1/verificar_preservacao.py
```

Consultamos a [validação da primeira revisão](VALIDACAO.md) como registro histórico e os [resultados desta padronização](PADRONIZACAO_FASES.md) para os caminhos atuais.
