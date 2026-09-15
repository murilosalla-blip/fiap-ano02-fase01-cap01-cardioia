# Bloco 2 — negação e regressão

Etapa parcial da revisão textual. Alterados apenas fase2/src/extrair_sintomas.py e fase2/tests/test_nlp.py.

## Verificação realizada

Suíte local executada com sucesso antes e depois da alteração. Acrescentados 12 casos de menções/negação, uma verificação integrada de relato negado, rejeição de entrada vazia e regressão da direção dos coeficientes. Os testes dos dez relatos, base textual, divisão por cenário e contrafactuais continuam passando.

A comparação da árvore Git após as alterações confirmou zero remoções e zero mudanças nos arquivos protegidos. Workflow remoto ainda não confirmado nesta etapa.

## Limites

A regra considera negações explícitas anteriores à menção dentro da oração, pontuação, adversativas e alguns verbos afirmativos. Não é um analisador linguístico completo: contexto de terceiros, hipóteses, negação posterior, expressões complexas e temporalidade permanecem limitados. Não equivale a validação clínica.

O classificador TF-IDF é independente do extrator: corrigir negação na extração não significa corrigir automaticamente suas previsões.

## Ainda pendente no bloco 2

Avaliação adicional com frases variadas, análise dos erros, atualização do notebook e da documentação geral, validação remota e integração da verificação de preservação aos testes da Fase 2. Não houve novo treinamento visual nem alteração da Fase 1.
