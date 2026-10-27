# Organização e preservação do CardioIA

Organizamos o projeto conforme o [modelo FIAP](https://github.com/agodoi/templateFiapVfinal), revisão `50e1e2720637b222357a7ebd1919c38a44af7cd2`. Consolidamos neste registro a organização, os critérios de redação e a preservação das entregas.

## Estrutura e reprodução

Mantemos na raiz `.github`, `assets`, `config`, `document`, `scripts` e `src`. Agrupamos as três fases dentro de `assets`, `config`, `document` e `src`; mantemos o portal em `src/fase2/portal-cardioia`. Os [guias por fase](../../README.md) orientam a reprodução atual; preservamos os PDFs das entregas anteriores sem alterar seu conteúdo.

Usamos a primeira pessoa do plural para relatar atividades do grupo e o infinitivo para orientar a reprodução. Documentamos pré-requisitos, comandos a partir da raiz, resultados esperados e limites. Distinguimos requisitos, escolhas de implementação, testes concluídos e entregas pendentes; não apresentamos planos como resultados.

Mantemos as exigências dos enunciados nas matrizes das [Fases 2](../../fase2/CHECKLIST_ENUNCIADO.md) e [3](../../fase3/CHECKLIST_ENUNCIADO.md) e nos [guias da Fase 1](../../fase1/README.md). Relatórios paginados, desafios, vídeo e submissão da Fase 3 continuam sujeitos à matriz de requisitos; esta organização não os substitui.

## Preservação e higienização

Registramos os destinos anteriores em [mapa_arquivos.json](mapa_arquivos.json) e [mudancas_padronizacao.json](mudancas_padronizacao.json), sem apagar seus itens. Preservamos o inventário de 223 itens do início da Fase 2 em [preservacao_fase1.json](preservacao_fase1.json): ele inclui os 181 arquivos do fechamento da Fase 1 e 42 acrescentados no início da Fase 2, não 223 arquivos exclusivos da Fase 1.

Em 25/10/2026, retiramos 63 arquivos de apoio: 34 PDFs de aulas, 11 entradas transitórias substituídas, 13 estados do primeiro ensaio de rede, quatro registros de organização consolidados aqui e um workflow aninhado sem execução neste repositório. Identificamos cada retirada por caminho, categoria, hash e commit em [higienizacao.json](higienizacao.json). Recuperamos os arquivos no [commit anterior à limpeza](https://github.com/murilosalla-blip/fiap-ano02-fase03-cardioia/tree/ba328f487bd99cd844834161b0ee30fad10a13e9), pelos caminhos registrados. Mantemos também uma cópia local de segurança fora do Git, em `.tools/backups/higienizacao-ba328f4/`, com os arquivos identificados pelo hash Git e pela extensão.

Dos 223 itens anteriores, conferimos 212 arquivos presentes e identificamos os 11 PDFs de aulas da Fase 1 pelo mesmo hash Git original no registro de recuperação. Não retiramos datasets, textos da amostra, imagens ECG, enunciados, fontes utilizadas, PDFs submetidos, código de execução, notebooks, métricas ou dependências. Mantemos as 16 cópias históricas em `document/other/historico/fase1/`, necessárias à conferência dos conteúdos originais. Não confundimos material didático com artefato necessário para executar o exercício.

Mantemos os logs funcionais e as capturas do Wokwi, os estados de `teste_rede_final/`, os registros de estabilidade e a validação guiada do painel. Retiramos somente o primeiro ensaio substituído, preservando as evidências finais. Mantemos os diagramas e cabeçalhos compartilhados nas duas pastas do firmware, pois cada projeto Wokwi precisa dos próprios arquivos locais.

Preservamos os 18 endereços externos originais do README, registrados em [links_externos_preservados.json](links_externos_preservados.json), incluindo as três pastas do Drive e o vídeo da Fase 2. Os repositórios históricos das [Fases 1](https://github.com/murilosalla-blip/fiap-ano02-fase01-cardioia) e [2](https://github.com/murilosalla-blip/fiap-ano02-fase02-cardioia) mantêm seus fechamentos originais. Não alteramos esses repositórios nesta higienização.

## Publicações e dados locais

Mantemos `src/fase2/app.py` e o arquivo adjacente `requirements.txt`, que aponta para `config/fase2/requirements.txt`. A aplicação Streamlit publicada está vinculada ao fork da Julia; preservamos esse vínculo e a publicação independente do portal. O workflow aninhado retirado não realizava a publicação a partir deste repositório.

Mantemos bancos SQLite, logs de execução e dependências locais em `.tools/`, fora do Git. Não removemos nem sobrescrevemos esses arquivos na higienização. Para uma cópia antiga ainda com dados em `fase3/runtime`, encerrar primeiro painel e consumidor e executar `python scripts/fase3/migrar_runtime.py`; o migrador preserva a origem e recusa sobrescrever destinos existentes. Em uma cópia nova, seguir diretamente o guia de instalação, sem migração.

## Como verificar

Executar na raiz:

```powershell
python scripts/validar_organizacao.py
python scripts/fase1/verificar_preservacao.py
python -m unittest discover -s scripts/tests -p 'test_*.py' -v
```

Conferimos os arquivos atuais, os hashes protegidos, as saídas históricas dos notebooks e os links locais. As exceções são individuais e limitadas às categorias de apoio registradas; não autorizam retirar dados ou programas. Para as verificações funcionais, seguir os guias de cada fase. Preservar um endereço não comprova suas permissões públicas; conferir esse acesso antes da submissão.

Na conferência de 25/10/2026, comparamos os arquivos antes e depois da higienização: mantivemos byte a byte os 250 arquivos de dados e execução conferidos em `assets`, `config` e `src`, excluindo textos Markdown revisados e o workflow inativo retirado. Reproduzimos os 303 registros da Fase 1 e conferimos as saídas dos quatro notebooks. Aprovamos os testes de NLP, Streamlit, sete testes do portal e seu build, 16 testes Python da Fase 3, 19 do painel, seis de proteção contra retiradas indevidas e os dois executáveis C++ de fila e confirmação MQTT. Conferimos novamente os logs existentes com os validadores Edge e MQTT; isso não representa uma nova simulação manual no Wokwi. Validamos a sintaxe dos quatro workflows e mantivemos os itens e hashes dos três inventários anteriores.

## Revisão das instruções de reprodução - 27/10/2026

Revisamos o README raiz, os guias atuais de cada fase, os guias auxiliares e os três relatórios da Fase 3. Explicitamos pré-requisitos, raiz de execução, preparação do ambiente, terminais separados, endereços, resultados esperados, encerramento e diagnóstico. Preservamos os PDFs submetidos nas fases anteriores e orientamos utilizar os guias atuais para executar a organização atual.

Preparamos uma cópia isolada dos arquivos versionados e das alterações locais em revisão, sem copiar `.venv`, `.tools` ou `node_modules`. Não apresentamos essa cópia como um clone público já atualizado: as mudanças ainda dependem de publicação. Instalamos as dependências novamente. No primeiro caminho, muito aninhado, a instalação de Jupyter falhou com aviso de limite de caminho do Windows. Repetimos em pasta temporária curta e concluímos a instalação. Incluímos essa condição e a orientação de não mover ambientes virtuais no README.

Conferimos nessa reprodução:

- preparação numérica com 303 registros e verificação dos 223 itens inventariados;
- extração textual, testes NLP, treinamento textual e teste funcional Streamlit;
- conferência das saídas dos quatro notebooks entregues e reexecução do notebook textual com kernel registrado no ambiente novo, gravando a cópia em `.tools/reproducao/fase2/`;
- 23 testes Python da Fase 3, incluindo REST por HTTP local, e seis testes de proteção da preservação;
- instalação npm limpa, sete testes do portal e build concluído;
- instalação limpa do Node-RED, 19 testes do painel e resposta HTTP 200 no endereço `/dashboard/monitoramento`, usando porta isolada 1889 apenas neste ensaio.

Os logs e ambientes de trabalho ficam em `.tools/reproducao-20261027/` e em pasta temporária local, fora do versionamento. Os resultados desta revisão não representam novos ensaios manuais do Wokwi, nova validação dos links externos, reexecução de TensorFlow/treinamentos visuais ou testes em Linux/macOS. Mantemos as evidências anteriores desses experimentos e identificamos downloads, arquitetura e rede como dependências das instruções correspondentes. Não garantimos a disponibilidade futura de serviços externos nem a nota da avaliação.

Na mesma revisão de 27/10, detalhamos a Fase 3 para reprodução por iniciantes: vocabulário inicial, instalação e download, verificações antes de avançar, terminais A/B, etapas numeradas do circuito e painel, nove passos de REST e conferência final. Mantemos o Ir Além 2 identificado como pendente. Esta ampliação é de instruções; não representa nova execução dos ensaios registrados acima.

Reorganizamos também os três PDFs da Fase 3: Edge com sete passos em duas páginas; MQTT/dashboard com dez passos e preparação em quatro páginas; REST/e-mail com nove passos em duas páginas. Conferimos as oito páginas renderizadas e atualizamos os índices para a paginação atual. Mantivemos os mínimos de uma e duas páginas dos relatórios principais e o limite de uma a duas páginas do Ir Além 1. Os PDFs históricos das fases anteriores não foram reescritos.

Consolidamos a [conferência final de reprodução de 27/10](../fase3/evidencias/2026-10-27/reproducao/RESULTADOS.md): clone com revisão local aplicada, instalações novas, execução Serial, integração MQTT observada, REST completo após reinício e 12 cenários do painel pelo broker real. Registramos expressamente a limitação na repetição integral dos passos visuais do Wokwi. Corrigimos a orientação para aguardar Server now running e Started flows antes de abrir o painel.

Na continuação da mesma revisão, concluímos a repetição visual acompanhada do Wokwi e conferimos 41 medições únicas sem lacunas nem perdas, com entrada/retorno dos dois alertas e recuperação pela chave. A [conferência guiada](../fase3/evidencias/2026-10-27/reproducao/validacao_guiada/RESULTADOS.md) encerra a pendência visual registrada nas tentativas anteriores.
