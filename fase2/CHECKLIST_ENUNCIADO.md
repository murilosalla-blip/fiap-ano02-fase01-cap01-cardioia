# Checklist de aderência — Fase 2

Auditoria feita a partir do enunciado oficial enviado em 14/09/2026 e do feedback recebido na Fase 1.

## Entrega obrigatória

| Requisito | Evidência | Situação |
|---|---|---|
| 10 relatos completos de sintomas | `fase2/dados/relatos_sintomas.txt` | Concluído |
| Mapa de conhecimento em CSV | `fase2/dados/mapa_conhecimento.csv`, com 25 associações | Concluído |
| Código de extração de sintomas | `fase2/src/extrair_sintomas.py` | Concluído |
| Base de frases e rótulos | `fase2/dados/classificacao_risco.csv`, com 120 frases | Concluído |
| TF-IDF | Pipeline em `fase2/src/classificar_risco_texto.py` | Concluído |
| Classificador treinado e testado | Regressão Logística e teste agrupado por cenário | Concluído |
| Avaliação do modelo | Acurácia, precisão, recall, F1, ROC AUC e matriz de confusão | Concluído |
| Notebook comentado | `fase2/notebooks/classificacao_textual_tfidf.ipynb` | Concluído |
| Repositório público | Repositório atual | Concluído |
| README completo | `README.md` e `fase2/README.md` | Concluído |
| Vídeo de até 4 minutos, não listado | Roteiro em `fase2/ROTEIRO_VIDEO.md`; link ainda não fornecido | **Pendente** |

## Ir Além 1 — Portal React

| Requisito | Evidência | Situação |
|---|---|---|
| React + Vite | `portal-cardioia/` | Concluído |
| Autenticação via Context API | `src/contexts/AuthContext.jsx` | Concluído |
| JWT fictício no localStorage | `AuthContext.jsx` | Concluído |
| Rotas protegidas | `src/App.jsx` | Concluído |
| Pacientes via base simulada | `public/data/patients.json` e `src/services/api.js` | Concluído |
| Agendamento com useState e useReducer | `src/pages/Appointments.jsx` | Concluído |
| Dashboard | `src/pages/Dashboard.jsx` | Concluído |
| CSS Modules e responsividade | `src/styles/Portal.module.css` | Concluído |
| Testes de autenticação e rota | `src/App.test.jsx` | Concluído |
| Build de produção | Validada no GitHub Actions | Concluído |
| Repositório público separado | Código preparado no monorepo | **Pendente de criação/transferência** |
| Integrantes e RMs no novo README | Exige autorização explícita para nova publicação | **Pendente** |
| Vídeo de até 4 minutos | Roteiro em `fase2/ROTEIRO_VIDEO.md`; link ainda não fornecido | **Pendente** |

## Ir Além 2 — MLP visual

| Requisito | Evidência | Situação |
|---|---|---|
| Base pública de ECG | Amostra curada na Fase 1, com DOI documentado | Concluído |
| Classificação normal vs. anormal | `fase2/src/treinar_mlp_ecg.py` | Concluído |
| Tons de cinza e redimensionamento | 64 × 64, normalização e realce do traçado | Concluído |
| MLP com Keras | Duas camadas densas, dropout e saída sigmoide | Concluído |
| Treino e teste | Divisão estratificada por exame único | Concluído |
| Avaliação | Acurácia, acurácia balanceada, precisão, recall, F1 e ROC AUC | Concluído |
| Notebook comentado | Baseline em `mlp_ecg_binaria.ipynb`; revisão ampliada autocontida em `mlp_ecg_ampliada.ipynb` | Concluído |
| Evidências reproduzíveis | Workflow e artifact `resultados-mlp-ecg` | Concluído |
| Vídeo de até 4 minutos | Link ainda não fornecido | **Pendente** |

### Revisão ampliada do Ir Além 2

| Verificação adicional | Evidência | Situação |
|---|---|---|
| Uso da versão 2 completa da fonte | 928 arquivos físicos auditados; 491 conteúdos únicos | Concluído |
| Remoção de duplicatas exatas | SHA-256 original em `fase2/auditoria/inventario_visual_ampliado.json` | Concluído |
| Privacidade dos exemplos | Cabeçalho e rodapé removidos dos derivados em `fase2/dados/visual_ampliado/` | Concluído |
| Separação treino/validação/teste | 313/79/99, estratificada pela classe original e sem hash repetido | Concluído |
| Limiar sem consultar o teste | Escolhido na validação; teste final preservado | Concluído |
| Avaliação ampliada | Acurácia balanceada 78,4%; ROC AUC 0,835 | Concluído |
| Reprodutibilidade | Duas execuções locais produziram o mesmo arquivo de métricas | Concluído |
| Restrição por paciente | A fonte não fornece ID confiável; limitação declarada | Concluído com limitação |

## Feedback da Fase 1

| Feedback | Tratamento na Fase 2 |
|---|---|
| Avaliar desempenho por sexo e outras características | Modelo tabular avaliado por sexo e faixa etária, com tamanho dos grupos e IC 95%; classificador textual auditado com pares contrafactuais feminino/masculino |
| Separar por paciente ou exame original | Tabular: uma linha por paciente. Texto: pares agrupados por cenário. Visual: hashes exclusivos por exame; a fonte não possui ID de paciente e essa limitação é declarada |
| Não interpretar balanceamento visual como prevalência | Aviso registrado no notebook, script, front e documentação |
| Manter modalidades independentes | Pipelines, dados, métricas e notebooks separados para texto, tabela e imagem |

## Testes automatizados

### Workflow principal

- build e testes do portal React;
- sintaxe dos módulos Python;
- exatamente 10 relatos;
- pelo menos 20 associações no mapa;
- correspondência nos 10 relatos;
- normalização de caixa, acentos e pontuação;
- comportamento sem correspondência;
- 120 frases textuais únicas e balanceadas;
- pares contrafactuais completos;
- ausência de vazamento de cenário;
- desempenho mínimo do classificador;
- diferença contrafactual máxima;
- inicialização do Streamlit;
- clique nos três fluxos do app;
- treinamento e análise tabular;
- métricas e intervalos de confiança por sexo e faixa etária;
- execução dos notebooks textual e tabular;
- geração e publicação dos resultados como artifact.

### Workflow visual

- 60 imagens únicas no experimento binário;
- pixels em tons de cinza, 64 × 64 e intervalo 0–1;
- ausência de hash repetido entre treino e teste;
- arquitetura Keras com entrada e saída corretas;
- treinamento da MLP;
- execução do notebook;
- geração e publicação de modelo, métricas, previsões e gráficos.

### Testes adicionais da revisão

- 491 hashes originais e derivados únicos;
- 142 imagens normais e 349 anormais;
- pixels em tons de cinza, 96 × 56 e intervalo 0–1;
- quatro classes originais presentes em treino, validação e teste;
- ausência de hash repetido entre os três conjuntos;
- execução determinística do treinamento ampliado;
- sondagem textual com negação, caixa, paráfrase e entradas fora do vocabulário;
- cinco testes do portal e build Vite de produção.

## Condição para declarar 100%

A implementação de código está completa quando os dois workflows finais estiverem verdes. A entrega acadêmica só poderá ser declarada 100% após:

1. criação do repositório separado do portal;
2. autorização para publicar novamente nomes e RMs nesse repositório;
3. gravação e publicação do vídeo ou dos vídeos exigidos;
4. inclusão dos links no README;
5. auditoria final e merge.
