# Compatibilidade e execução local da Fase 3

Organizo o código em [src/fase3](../src/fase3/), os contratos e dependências em [config/fase3](../config/fase3/), os auxiliares em [scripts/fase3](../scripts/fase3/) e o roteiro em [document/fase3](../document/fase3/README.md).

Mantenho `runtime/` e `build/` como saídas locais ignoradas pelo Git. Preservo o banco SQLite e os registros existentes em `runtime/`, sem reiniciar uma sessão em execução durante a reorganização.

Mantenho os comandos anteriores do consumidor e do painel por meio de pequenas entradas de compatibilidade. Consulto o passo a passo atualizado no [guia do painel](../document/fase3/node-red/README.md).
