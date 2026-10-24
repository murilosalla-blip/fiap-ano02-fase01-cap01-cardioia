# Meu registro de organização do CardioIA

Organizei as três fases em 24/10/2026 com base no [modelo FIAP](https://github.com/agodoi/templateFiapVfinal), revisão `50e1e2720637b222357a7ebd1919c38a44af7cd2`. Registrei a análise em [analise_template_fiap.md](analise_template_fiap.md).

## Critério que apliquei

- Concentrei código, notebooks e testes em `src/`, com separação por fase e aplicativo.
- Concentrei guias, relatórios e roteiros em `document/faseN/` e registros complementares em `document/other/`.
- Separei dependências, contratos e configurações em `config/`; mantive os manifestos exigidos junto dos aplicativos.
- Separei recursos novos e imagens em `assets/faseN/`, preservando os caminhos dos datasets da Fase 1.
- Organizei aulas e enunciados em `document/other/referencias/faseN/` e preservei os PDFs submetidos.
- Atualizei caminhos nos guias, notebooks e workflows. Mantenho as evidências anteriores sem executar novamente a simulação para substituir os registros originais.

## Compatibilidade que preservei

Preservo no README os links externos das entregas anteriores, incluindo as três pastas de materiais da Fase 1 no Drive e a gravação da Fase 2 no YouTube. Registrei os endereços originais em [links_externos_preservados.json](links_externos_preservados.json); verifico sua presença com `python scripts/validar_organizacao.py`. Mantenho também os links nos guias das respectivas fases. Essa conferência verifica a preservação dos endereços; não altera as permissões dos serviços externos.

Mantenho `fase2/app.py` e `fase2/requirements.txt` como entradas para o Streamlit Cloud. O aplicativo completo fica em `src/fase2/app.py`. A publicação independente do portal usa outro repositório, cuja estrutura não alterei.

Mantenho `python src/fase3/python/consumidor_mqtt.py` e `node fase3/node-red/iniciar.js --com-consumidor` por meio de entradas que encaminham aos componentes atuais. O banco, os eventos e o diretório de execução continuam em `fase3/runtime/`; não movo o banco durante uma sessão em andamento. Para uma instalação nova, sigo os comandos atuais do [guia do painel](../../fase3/node-red/README.md).

Preservo os projetos públicos do Wokwi e os mesmos arquivos de firmware e circuito. Os caminhos atuais dos demais comandos estão nos guias; o [mapa de arquivos](mapa_arquivos.json) registra o destino de cada arquivo que já estava versionado.

## Como confiro a preservação

Registrei o commit anterior, os 397 arquivos versionados e seus hashes SHA-256 em `mapa_arquivos.json`. Confiro presença de todos os destinos e identidade dos binários, firmware, datasets e registros de execução. Normalizo somente CRLF/LF nos conteúdos textuais para permitir a mesma conferência no Windows e no Linux; comparo o fluxo JSON regenerado por conteúdo estruturado. Permito revisões de texto somente em documentação, caminhos operacionais, notebooks e workflows.

Preservo o [manifesto anterior](../fase2/auditoria/preservacao_pre_revisao.json) sem reescrever seus hashes. Registro seus destinos em [preservacao_fase1.json](preservacao_fase1.json). Quando atualizo um documento protegido pelo manifesto antigo, arquivo o blob original do histórico em `document/other/historico/fase1/`; verifico esse conteúdo pelo hash original. Essas cópias são registros históricos, com os caminhos e as orientações vigentes na época.

Executo, na raiz do repositório:

```powershell
python scripts/validar_organizacao.py
python src/fase2/tests/verificar_preservacao.py
```

Registro a validação funcional e seus limites em [VALIDACAO.md](VALIDACAO.md).
