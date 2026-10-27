# Verificação da Fase 1

Conferimos o inventário de 223 itens registrado no início da Fase 2, que inclui os 181 arquivos do fechamento da Fase 1. Mantemos 212 arquivos nos destinos locais e identificamos os 11 PDFs de aulas retirados pelo mesmo hash Git original, conforme o [registro de preservação](../../document/other/organizacao/README.md):

Preparar o ambiente pelo [guia da Fase 1](../../document/fase1/README.md). Executar da raiz no PowerShell, sem dependências adicionais para esta verificação:

```powershell
.\.venv\Scripts\python.exe scripts/fase1/verificar_preservacao.py
```

Mantemos o código de preparação em [src/fase1](../../src/fase1/README.md).
