# Revisão da Fase 2 — bloco 1: inventário e proteção

## Escopo e referência

Repositório: murilosalla-blip/fiap-ano02-fase01-cap01-cardioia.
Branch de trabalho: fase-2-machine-learning.
Commit auditado: f78dd97b19245f65a9b708e5fcde0505c7bba25f.
Referência de preservação: ee6b22dc40fa307c528b17b57856890fa264c20c.

A referência preserva o estado existente antes desta revisão, não reconstrói retroativamente a entrega original da Fase 1.

## Resultado da comparação

- 224 arquivos anteriores conferidos quanto à presença.
- 183 arquivos protegidos conferidos por hash Git e modo.
- Zero arquivos anteriores removidos.
- Zero arquivos protegidos alterados.
- 120 imagens permanecem em assets/imagens/ecg/.
- Árvore retornada pelo GitHub completa, sem truncamento.

Esta conferência foi feita comparando o inventário com a árvore Git; não representa uma nova inspeção visual dos exames.

## Restrições aprovadas

1. Não apagar qualquer arquivo anterior.
2. Não alterar arquivos fora de fase2/ e portal-cardioia/, incluindo README raiz, assets/, document/, scripts/ e workflows existentes.
3. Não modificar a Fase 1 nem integrar alterações à main nesta revisão.
4. Salvar dados e derivados ampliados separadamente dentro da Fase 2.
5. Preservar o experimento inicial visual e seus resultados como histórico.
6. Não aguardar novo repositório para revisar os modelos e o portal existente.
7. Solicitar a criação do repositório separado somente no bloco de publicação do portal.

## Evidências e limites dos testes atuais

Workflow principal aprovado no commit auditado:
https://github.com/murilosalla-blip/fiap-ano02-fase01-cap01-cardioia/actions/runs/34981731140

| Área | Cobertura observada | Lacuna a tratar |
|---|---|---|
| Preservação | Inventário e script verificar_preservacao.py; comparação da árvore realizada neste bloco | O workflow não chama o script; não há bloqueio automático de merge |
| Extração | Dez relatos, normalização e ausência de correspondência | Negação, fronteiras de palavras e casos ambíguos |
| NLP | Divisão por cenário, métricas e pares contrafactuais | Frases independentes dos padrões atuais, termos influentes e robustez |
| Visual | 60 imagens, formas dos pixels, hashes entre treino/teste e arquitetura | Base ampliada, grupos por exame/paciente, quase duplicatas e generalização |
| React | Dois testes: login/rota inicial e credenciais inválidas | Pacientes, agendamentos, persistência, logout, falhas e responsividade |
| Publicação | Código disponível no branch | Não foi repetido teste de interface no ambiente publicado neste bloco |

Testes técnicos aprovados não demonstram utilidade clínica nem ausência de erro metodológico.

## Próximos blocos e arquivos previstos

| Ordem | Trabalho | Destino previsto |
|---|---|---|
| 2 | Negação e robustez do extrator; regressão dos termos; avaliação textual | fase2/src/, fase2/tests/, fase2/dados/ e notebook textual |
| 3 | Recuperação e auditoria da mesma fonte visual da Fase 1 | fase2/auditoria/ e fase2/dados/visual_ampliado/ |
| 4 | Protocolo de avaliação antes de ajustar a MLP | fase2/auditoria/ |
| 5 | Pré-processamento e MLP revisados, preservando versão inicial | Novos módulos e notebook em fase2/ |
| 6 | Métricas, incerteza, erros e feedback demográfico | fase2/resultados/ e documentação da Fase 2 |
| 7 | Testes e revisão de Streamlit e portal existente | fase2/app.py, fase2/tests/ e portal-cardioia/ |
| 8 | Consolidação de evidências e preparação da publicação | fase2/README.md e documentos complementares |

A lista identifica áreas previstas, não alterações já executadas.

## Verificação de preservação nos próximos blocos

Executar explicitamente:
python fase2/tests/verificar_preservacao.py

Além disso, comparar a árvore Git antes/depois de cada bloco.
Como os workflows existentes são protegidos pelo inventário, não serão editados para acrescentar esse comando.
Pode-se integrar a chamada em um teste já executado de fase2/, com verificação antes de qualquer escrita em arquivos protegidos.
A checagem detecta alterações; ela não substitui controles de acesso do GitHub.

## Decisões que ainda dependem de auditoria

- A contagem de 491 imagens únicas é histórica e precisa ser reconfirmada.
- A utilidade dos identificadores originais para agrupar pacientes/exames ainda não foi comprovada.
- A resolução de entrada e a arquitetura final serão escolhidas no desenvolvimento, não pelo teste final.
- A ampliação visual e um novo resultado de desempenho ainda não foram executados.
- Os vídeos continuam pendentes no enunciado, fora da execução atual.

## Critério de encerramento deste bloco

Inventário conferido, preservação confirmada, lacunas registradas e escopo isolado da Fase 1.
Nenhum arquivo existente foi alterado por este bloco.
