# Relatório de entrega — Fase 2 CardioIA

## Situação executiva

A implementação técnica do escopo obrigatório, dos dois desafios Ir Além e da extensão tabular está concluída e testada. Restam atividades externas de publicação: criar o repositório público separado do portal, autorizar/inserir integrantes e RMs nesse README e publicar os vídeos não listados no YouTube.

## Evidências por requisito

| Bloco | Evidência | Situação |
|---|---|---|
| 10 relatos simulados | `fase2/dados/relatos_sintomas.txt` | Concluído |
| Mapa sintoma–doença | `fase2/dados/mapa_conhecimento.csv` | Concluído |
| Extrator Python | `fase2/src/extrair_sintomas.py` | Concluído |
| Base textual de risco | `fase2/dados/classificacao_risco.csv` | Concluído |
| TF-IDF e classificador | `fase2/src/classificar_risco_texto.py` e notebook | Concluído |
| Avaliação e vieses | métricas, matriz de confusão e teste contrafactual | Concluído |
| Portal React | `portal-cardioia/` | Código concluído; repositório separado pendente |
| MLP de ECG | script, notebook, testes e resultados visuais | Concluído |
| README e repositório público | documentação no branch público | Concluído no repositório principal |
| Vídeos | roteiros prontos | Links do YouTube pendentes |

## Resultado dos testes

- NLP: 120 frases únicas; 96 treino e 24 teste; acurácia, precisão, recall, F1 e ROC AUC iguais a 1,0.
- Contrafactual de sexo: diferença absoluta média de 0,002549 e máxima de 0,003250.
- Streamlit: inicialização e fluxos tabular, extração e classificação textual cobertos.
- Portal: cinco testes cobrem proteção de rota, login válido e inválido, busca/erro de pacientes, criação/persistência/remoção de consultas e logout; build Vite concluído.
- Visual: 60 imagens únicas e equilibradas; 48 treino e 12 teste; hashes sem sobreposição; arquitetura Keras validada.
- MLP visual: acurácia e acurácia balanceada de 0,4167; ROC AUC de 0,6667.
- Revisão visual: 491 imagens únicas; 313 treino, 79 validação e 99 teste; acurácia balanceada de 0,7453; F1 anormal de 0,7458; ROC AUC de 0,8241.
- Reprodutibilidade ampliada: duas execuções produziram métricas idênticas com semente 42.
- Robustez textual: 16 sondagens sintéticas; quatro entradas sem vocabulário e apenas 0,0121 de diferença entre afirmação e negação, registrada como limitação explícita no front.

## Resposta ao feedback anterior

- **Análise por sexo/demografia:** realizada no modelo tabular e complementada com teste contrafactual feminino/masculino no texto.
- **Separação por paciente/exame:** o Cleveland usa registros independentes; no visual não há ID de paciente na fonte, então foi aplicada separação por hash de conteúdo e a limitação foi registrada. Hash elimina repetição exata, mas não prova indivíduos distintos.
- **Balanceamento 30 por classe:** mantido no baseline para preservar a Fase 1. A revisão usa as 491 imagens únicas disponíveis, com pesos calculados no treino; nenhum dos dois desenhos é apresentado como prevalência.
- **Modalidades independentes:** texto, tabular e imagem possuem pipelines, resultados e interfaces separados.

## Limitações que devem ser ditas na apresentação

- 100% no NLP resulta de uma base simulada pequena e deliberadamente separável.
- O baseline visual tem teste muito pequeno; a revisão ampliada melhora a evidência, mas continua insuficiente para uso real.
- Nenhum modelo foi validado externamente ou clinicamente.
- A ausência de ID de paciente nas imagens impede garantir separação por paciente.
- O balanceamento experimental não representa prevalência de doenças.

## Pendências externas

1. Criar um repositório público vazio chamado, por exemplo, `grupo-aura-cardioia-portal`.
2. Copiar `portal-cardioia/` para esse repositório.
3. Inserir integrantes e RMs após autorização explícita para republicação.
4. Gravar e publicar os vídeos como não listados.
5. Substituir os marcadores de vídeo nos READMEs pelos URLs finais.
