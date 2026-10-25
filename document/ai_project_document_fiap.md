<img src="../assets/logo-fiap.png" alt="FIAP" width="30%">

# AI Project Document — CardioIA

**Grupo Aura:** Murilo Salla (RM568041), Elias da Silva de Souza (RM568500) e Julia Duarte de Carvalho (RM567816).

**Tutor:** Leonardo Ruiz Orabona. **Coordenador:** André Godoi Chiovato.

## 1. Introdução

Desenvolvemos o CardioIA como projeto acadêmico para estudar dados cardiovasculares, modelos de IA e integração IoT. Organizamos a evolução por fase e preservamos as evidências de cada entrega. Uso dados públicos, bases textuais simuladas e sensores simulados; não interpretamos os resultados como diagnóstico ou validação clínica.

## 2. Visão geral

Na Fase 1, preparamos dados numéricos, textuais e visuais. Na Fase 2, implementamos extração de sintomas, classificação textual e experimentos complementares, com interfaces demonstrativas. Na Fase 3, integramos coleta no ESP32, recuperação offline, transporte MQTT, persistência e monitoramento em Node-RED.

| Fase | Documentação de referência |
|---|---|
| 1 | [Guia e submissão](fase1/README.md) |
| 2 | [Execução](fase2/README.md) e [relatório da entrega](fase2/RELATORIO_ENTREGA.md) |
| 3 | [Execução](fase3/README.md), [roteiro](fase3/ROTEIRO_ENTREGA.md) e [checklist](fase3/CHECKLIST_ENUNCIADO.md) |

## 3. Desenvolvimento

### 3.1 Dados e preparação

Reunimos 303 registros e 14 variáveis da base Cleveland, textos derivados de fontes oficiais de saúde e uma amostra de 120 imagens de ECG. Preservamos a rastreabilidade das fontes, os dicionários e os scripts de preparação da Fase 1. Na Fase 2, construímos uma base textual simulada e usamos uma base visual ampliada com 491 imagens deduplicadas, mantendo as limitações de identificação de pacientes registradas no relatório.

### 3.2 Modelos e interfaces

Implementamos um mapa de conhecimento para dez relatos de sintomas e um classificador TF-IDF com regressão logística. Separamos os pares de cenários entre treino e teste para evitar vazamento. Também comparamos modelos tabulares, avaliamos desempenho por subgrupos e experimentamos MLPs visuais. Construímos o aplicativo Streamlit e o portal React como interfaces acadêmicas, mantendo as modalidades e suas limitações explícitas.

### 3.3 Integração e testes da Fase 3

Implementamos coleta em janelas de cinco segundos simulados, fila em RAM limitada a 2.000 leituras e contagem de descartes. Usamos MQTT, identificação por dispositivo/sessão/sequência, deduplicação SQLite e ACK somente depois da gravação. A fila não sobrevive ao desligamento do ESP32. No Node-RED, separamos conexão, atualidade da leitura, recuperação e alertas didáticos, com histórico limitado e confirmação em duas janelas consecutivas.

Testamos os núcleos C++, os contratos, a persistência, as regras do painel e os fluxos de execução. Registramos separadamente os ensaios Python, as execuções no Wokwi e as validações do painel para não confundir publicações sintéticas de teste com evidência do ESP32.

## 4. Resultados e avaliações

Na Fase 1, concluímos a preparação das três modalidades. Na Fase 2, registramos acurácia de 1,000 em 24 frases simuladas de teste, ROC AUC tabular de aproximadamente 0,958 em 61 registros e acurácia balanceada de aproximadamente 0,745 no experimento visual ampliado com 99 imagens de teste. Consultamos divisões, métricas, vieses e limitações no [relatório da Fase 2](fase2/RELATORIO_ENTREGA.md); não generalizamos esses números para uso clínico.

Na Fase 3, validamos coleta offline, retomada, reenvio, deduplicação, pulsos, alteração da temperatura ambiente e alertas do dashboard. Preservamos os [resultados Edge](other/fase3/evidencias/2026-10-24/RESULTADOS.md), [MQTT](other/fase3/evidencias/2026-10-24/mqtt/RESULTADOS.md) e [Node-RED](other/fase3/evidencias/2026-10-24/dashboard/RESULTADOS.md).

## 5. Conclusões e trabalhos futuros

Concluímos a base de dados e os experimentos das Fases 1 e 2 e validamos as três primeiras entregas práticas da Fase 3. Ainda precisamos implementar e validar REST/e-mail, realizar a comparação com modelos neuromórficos e concluir os relatórios e a submissão final. Mantemos o acompanhamento no [roteiro da Fase 3](fase3/ROTEIRO_ENTREGA.md).

## 6. Referências

- [Fontes e documentação das modalidades da Fase 1](fase1/README.md).
- [Referências e limitações dos experimentos da Fase 2](fase2/RELATORIO_ENTREGA.md).
- [Modelo oficial de repositório FIAP](https://github.com/agodoi/templateFiapVfinal), revisão `50e1e2720637b222357a7ebd1919c38a44af7cd2`.
- [Enunciados e aulas por fase](other/referencias/README.md).

## 7. Anexos

- [Documento original da Fase 1](other/historico/fase1/document/ai_project_document_fiap.md).
- [Registro da organização e verificação de preservação](other/organizacao/README.md).
- [Submissão da Fase 1](fase1/cardioia_fase1_entrega_fiap.pdf).
- [Relatório da Fase 2](fase2/RELATORIO_ENTREGA.md).
