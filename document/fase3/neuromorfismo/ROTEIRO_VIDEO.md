# 🎬 Vídeo do Ir Além 2 — roteiro para até quatro minutos

Preparamos este roteiro para apresentar resultados e análise crítica. A gravação e a publicação ainda estão pendentes; este documento não substitui o link de um vídeo real.

## Antes de gravar

1. Concluir os passos do [guia](README.md) e abrir o HTML executado.
2. Deixar visíveis as seções de divisão, métricas, matrizes e atividade LIF. Usar zoom legível.
3. Abrir o README raiz e o relatório comparativo para alternar durante a apresentação.
4. Preparar captura de tela com microfone; fazer teste curto e conferir áudio. Evitar exibir e-mails, outras abas e dados particulares.
5. Ensaiar para terminar em cerca de **3min40s**, mantendo margem para o limite de quatro minutos.

## Sequência sugerida de narração e tela

- **0:00–0:25 | Objetivo e continuidade.** “Somos o Grupo Aura e desenvolvemos o CardioIA. Na Fase 2 trabalhamos com classificadores; na Fase 3 acrescentamos IoT. Neste desafio comparamos uma regressão logística com uma rede LIF em séries temporais sintéticas de BPM.” Mostrar título e integrantes.
- **0:25–1:00 | Dados e divisão.** “Geramos 240 sessões de dez minutos, com leituras a cada cinco segundos. Os rótulos representam oscilação lenta ou rápida do gerador, sem diagnóstico. Separamos sessões em 144 de treino, 48 de validação e 48 de teste antes de criar janelas. Assim, não compartilhamos uma sessão entre treino e teste.” Mostrar contagens e sinais.
- **1:00–1:45 | Modelos funcionais.** “No tradicional extraímos oito atributos, incluindo diferenças sucessivas e autocorrelação. Na rede LIF usamos 24 neurônios recorrentes com fuga, limiar, disparo, reset e refratariedade. Os pesos internos são fixos; treinamos a saída logística sobre 120 atributos da atividade. Escolhemos a regularização somente na validação.” Mostrar código resumido, gráfico de potencial e raster de spikes. Explicar que o relógio LIF difere do relógio da série.
- **1:45–2:35 | Comparação.** “Nos mesmos 48 casos, acertamos 44 com o tradicional e 35 com o LIF: acurácia balanceada de 91,7% e 72,9%, respectivamente. O F1 macro foi 0,9165 e 0,7262. O tradicional errou três sessões regulares e uma oscilante; o LIF errou nove e quatro. Agregamos as nove janelas pela média das probabilidades.” Mostrar as duas matrizes e os números.
- **2:35–3:15 | Análise crítica.** “Os atributos temporais explícitos foram mais úteis neste experimento. Não concluímos que o LIF seja sempre inferior. Comparamos representações de tamanhos distintos, em uma semente e dados artificiais. O intervalo da diferença favoreceu o tradicional neste teste; não medimos energia nem usamos um chip neuromórfico. Esses resultados não validam diagnóstico.” Mostrar limites e intervalo bootstrap.
- **3:15–3:40 | Reprodução e conclusão.** “Disponibilizamos código, dependências, notebook executado, resultados e relatório de duas páginas. O guia mostra como rodar a comparação, executar o notebook inteiro e conferir nove testes. A execução pode ser feita sem Wokwi ou servidores.” Mostrar comandos e caminhos do guia, com texto legível.

## Depois de gravar

1. Assistir ao vídeo inteiro: conferir áudio, legibilidade, cortes, números e duração **até 4:00**.
2. Publicar no YouTube como **não listado**, conforme o enunciado.
3. Abrir o link em janela sem autenticação e conferir se reproduz.
4. Inserir o link real na seção de vídeo da Fase 3 no README raiz. Preservar o vídeo da Fase 2.
5. Atualizar checklist e roteiro somente após conferir a publicação.

Podemos adaptar a fala ao grupo, mantendo os resultados efetivamente observados e a distinção entre experimento sintético e aplicação clínica.
