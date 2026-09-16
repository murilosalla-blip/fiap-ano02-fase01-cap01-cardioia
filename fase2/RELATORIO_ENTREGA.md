# Relatório de entrega — Fase 2 CardioIA

## Situação executiva

A implementação técnica do escopo obrigatório, dos dois desafios Ir Além e da extensão tabular está concluída e testada. O Streamlit agora funciona como produto principal unificado e o portal React, publicado separadamente, é um protótipo administrativo complementar. Resta publicar os vídeos não listados no YouTube.

## Evidências por requisito

| Bloco | Evidência | Situação |
|---|---|---|
| 10 relatos simulados | `fase2/dados/relatos_sintomas.txt` | Concluído |
| Mapa sintoma–doença | `fase2/dados/mapa_conhecimento.csv` | Concluído |
| Extrator Python | `fase2/src/extrair_sintomas.py` | Concluído |
| Base textual de risco | `fase2/dados/classificacao_risco.csv` | Concluído |
| TF-IDF e classificador | `fase2/src/classificar_risco_texto.py` e notebook | Concluído |
| Avaliação e vieses | métricas, matriz de confusão e teste contrafactual | Concluído |
| Portal React | `portal-cardioia/` e `Julia-carvalho96/fiap-cardioia-portal` | Concluído e publicado |
| Produto unificado | Streamlit com avaliações, ECG, histórico e links recíprocos | Concluído |
| MLP de ECG | script, notebook, testes e resultados visuais | Concluído |
| README e repositório público | documentação no branch público | Concluído no repositório principal |
| Vídeos | não publicados | Links do YouTube pendentes |

## Resultado dos testes

- NLP: 120 frases únicas; 96 treino e 24 teste; acurácia, precisão, recall, F1 e ROC AUC iguais a 1,0.
- Contrafactual de sexo: diferença absoluta média de 0,002549 e máxima de 0,003250.
- Streamlit: navegação, integração com o portal, ECG transparente, histórico da sessão e fluxos tabular, extração e classificação textual cobertos.
- Portal: seis testes cobrem proteção de rota, login válido e inválido, busca/erro de pacientes, carteira e agenda fictícias, criação/persistência/remoção de consultas, vínculo com o Streamlit e logout; build Vite concluído.
- Visual: 60 imagens únicas e equilibradas; 48 treino e 12 teste; hashes sem sobreposição; arquitetura Keras validada.
- MLP visual: acurácia e acurácia balanceada de 0,4167; ROC AUC de 0,6667.
- Revisão visual: 491 imagens únicas; 313 treino, 79 validação e 99 teste; acurácia balanceada de 0,7840; F1 anormal de 0,7833; ROC AUC de 0,8350.
- Reprodutibilidade ampliada: duas execuções produziram métricas idênticas com semente 42.
- Robustez textual: 16 sondagens sintéticas; quatro entradas sem vocabulário e apenas 0,0121 de diferença entre afirmação e negação, registrada como limitação explícita no front.
- Demografia tabular: avaliação adicional em três faixas etárias (18, 25 e 18 pacientes), com métricas e IC 95% por 2.000 reamostragens.

## Resposta ao feedback anterior

- **Análise por sexo/demografia:** realizada por sexo e faixa etária no modelo tabular, com intervalos de confiança, e complementada com teste contrafactual feminino/masculino no texto.
- **Separação por paciente/exame:** o Cleveland usa registros independentes; no visual não há ID de paciente na fonte, então foi aplicada separação por hash de conteúdo e a limitação foi registrada. Hash elimina repetição exata, mas não prova indivíduos distintos.
- **Balanceamento 30 por classe:** mantido no baseline para preservar a Fase 1. A revisão usa as 491 imagens únicas disponíveis, com pesos calculados no treino; nenhum dos dois desenhos é apresentado como prevalência.
- **Modalidades independentes:** texto, tabular e imagem possuem pipelines, resultados e interfaces separados.

## Limitações que devem ser ditas na apresentação

- 100% no NLP resulta de uma base simulada pequena e deliberadamente separável.
- O baseline visual tem teste muito pequeno; a revisão ampliada melhora a evidência, mas continua insuficiente para uso real.
- Nenhum modelo foi validado externamente ou clinicamente.
- Os subgrupos etários têm somente 18 a 25 pacientes; métricas altas e intervalos amplos não demonstram generalização ou equidade.
- A ausência de ID de paciente nas imagens impede garantir separação por paciente.
- O balanceamento experimental não representa prevalência de doenças.

## Pendências externas

1. Gravar e publicar os vídeos como não listados.
2. Inserir os URLs finais nos READMEs.
3. Realizar a auditoria final da submissão.
