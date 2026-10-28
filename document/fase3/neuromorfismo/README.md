# 🧠 Ir Além 2 — séries temporais e rede LIF

Comparamos uma **regressão logística sobre atributos temporais** com uma **rede recorrente de 24 neurônios LIF e saída logística treinada**. Desenvolvemos o experimento em Python/NumPy e preservamos o [notebook comentado e executado](../../../src/fase3/notebooks/comparacao_temporal_lif.ipynb), o [código](../../../src/fase3/neuromorfismo/experimento.py) e os [resultados da referência](../../../assets/fase3/resultados/neuromorfismo/).

Damos sequência aos classificadores da Fase 2 e à coleta temporal da Fase 3. As bases anteriores não são séries longitudinais de sinais vitais; por isso, geramos sessões sintéticas próprias. Não ordenamos pacientes da base Cleveland para simular tempo, não reutilizamos imagens de ECG como leituras do ESP32 e não classificamos os testes manuais do botão como diagnóstico.

**Situação:** concluímos a implementação e os testes locais. Produzimos o [relatório comparativo de duas páginas](../CardioIA_Fase3_Relatorio_Neuromorfismo.pdf), com revisão técnica concluída em 28/10/2026. Concluímos a validação guiada em 28/10/2026: instalação, comparação, três gráficos, notebook completo, HTML e seis testes com `OK`. Na revisão técnica, acrescentamos e aprovamos três testes de exportação, totalizando nove. A gravação, a publicação do vídeo não listado e a inclusão do link no README raiz permanecem pendentes. Alterações locais só estarão disponíveis em um novo clone depois de publicadas no GitHub.

## 🎯 O que classificamos

- Geramos **240 sessões**, com 120 leituras de BPM artificial a cada cinco segundos: dez minutos por sessão.
- Usamos duas classes balanceadas: `regular_simulado` e `oscilante_simulado`. São nomes dos regimes do gerador, não diagnósticos.
- Sorteamos a mesma faixa de média, amplitude, ruído e deriva para as duas classes. A diferença é o período da oscilação: 35–65 amostras na classe regular e 9–18 na oscilante.
- Fixamos a semente em **42** e registramos o SHA-256 dos sinais e rótulos. Não precisamos baixar dados externos, ligar o Wokwi ou iniciar servidores.
- Uma leitura pode ter BPM acima de 120 em qualquer classe. O rótulo não corresponde ao alerta didático do painel.

## 🔬 Como fizemos uma comparação verificável

1. Separamos **sessões completas**: 144 para treino, 48 para validação e 48 para teste, com metade de cada classe em cada conjunto.
2. Criamos nove janelas de 24 amostras por sessão, com passo de 12. Há sobreposição dentro da sessão, sem compartilhar sessões entre partições.
3. Extraímos oito atributos tradicionais, incluindo autocorrelação e diferenças sucessivas; ajustamos normalização e regressão logística no treino.
4. Alimentamos a rede LIF com nível e variação do sinal normalizados pelo treino. Simulamos fuga, limiar, disparo, reset, recorrência e refratariedade; extraímos 120 atributos e treinamos a saída logística.
5. Selecionamos a regularização `C` de cada saída pelo F1 macro das **sessões de validação**, com quatro valores previamente definidos. O teste não seleciona parâmetros.
6. Calculamos a média das probabilidades das nove janelas para classificar cada sessão. Usamos decisão em 0,5 para ambos os métodos.
7. Avaliamos os mesmos 48 casos de teste, com métricas e matrizes de confusão por sessão. Mantemos métricas por janela como resultado secundário.
8. Estimamos incerteza com 2.000 reamostragens estratificadas de sessões, incluindo a diferença pareada entre os métodos. Não tratamos 432 janelas sobrepostas como 432 sessões independentes.

**O que é treinado no LIF:** os pesos internos do reservatório são fixos pela semente; treinamos a saída logística sobre a atividade da rede. Não alegamos STDP, treinamento de sinapses internas ou execução em chip neuromórfico. Os dois métodos terminam em regressão logística; comparamos representações diferentes, não algoritmos de saída diferentes.

## ▶️ Como reproduzir — começar aqui

### Passo 1 — Entrar na pasta certa

- Usar Windows com Git e Python **3.12**, conforme a [preparação da Fase 3](../README.md#como-reproduzir--preparação).
- Abrir o PowerShell pelo menu Iniciar. Não executar os comandos no editor do Wokwi nem no Monitor Serial.
- Se já possui o projeto, copiar o caminho da pasta no Explorador e executar `Set-Location -LiteralPath 'caminho copiado'`, substituindo o texto entre aspas. A pasta precisa conter `README.md`, `src` e `config`.
- Se vai baixar uma cópia nova, seguir os passos 2 e 3 da preparação. Preferir pasta curta, por exemplo `C:\projetos`, para evitar o limite de caminhos do Windows. Não apagar sua cópia atual.
- Conferir, uma linha por vez:

```powershell
python --version
Test-Path .\config\fase3\requirements-neuromorfismo.txt
Test-Path .\scripts\fase3\executar_neuromorfismo.py
```

**Esperado:** Python `3.12.x` e dois resultados `True`. Se retornar `False`, conferir a pasta e se a revisão baixada já contém o Ir Além 2. Não continuar com arquivos ausentes.

### Passo 2 — Preparar o Python desta pasta

1. Conferir se o ambiente já existe:

```powershell
Test-Path .\.venv\Scripts\python.exe
```

2. Se retornar `False`, criar e aguardar o prompt voltar:

```powershell
python -m venv .venv
```

3. Conferir e instalar as dependências específicas:

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip install -r config/fase3/requirements-neuromorfismo.txt
```

**Esperado:** Python `3.12.x`, instalação sem erro e retorno do prompt. Não precisamos ativar o ambiente. As dependências MQTT/REST sozinhas não incluem esta trilha; usar o arquivo acima. Se `python` só funcionar por `py -3.12`, criar o ambiente com `py -3.12 -m venv .venv`.

### Passo 3 — Executar a comparação

```powershell
.\.venv\Scripts\python.exe scripts/fase3/executar_neuromorfismo.py
```

- Aguardar o término; este programa termina sozinho, sem Ctrl+C.
- O resultado apresenta uma linha para `tradicional`, outra para `lif` e a pasta de saída.
- Na referência Windows/Python 3.12, encontramos F1 macro próximo de **0,9165** no tradicional e **0,7262** no LIF. Pontuação menor no LIF é o resultado observado, não uma falha de instalação.
- Os tempos variam conforme o computador; não precisam ser iguais aos nossos.
- Os novos arquivos ficam em `.tools/runtime/fase3/neuromorfismo/`. Não sobrescrevemos os resultados entregues em `assets/fase3/resultados/neuromorfismo/` por padrão.

### Passo 4 — Ver os gráficos

Executar uma linha por vez para abrir os arquivos no visualizador de imagens do computador:

```powershell
Invoke-Item .tools/runtime/fase3/neuromorfismo/series.png
Invoke-Item .tools/runtime/fase3/neuromorfismo/matrizes_confusao.png
Invoke-Item .tools/runtime/fase3/neuromorfismo/atividade_lif.png
```

- **Séries:** duas sessões artificiais, uma de cada regime; eixo horizontal em segundos da série.
- **Matrizes:** tradicional `[[21, 3], [1, 23]]`; LIF `[[15, 9], [4, 20]]` na referência. As linhas são classes reais e as colunas são previsões. Cada matriz soma 48 sessões.
- **Atividade LIF:** potencial de um neurônio com linha de limiar e pontos dos disparos dos 24 neurônios. Os milissegundos desse gráfico pertencem ao modelo LIF: cada 20 ms representa uma leitura IoT de cinco segundos.

### Passo 5 — Conferir os números e a separação dos dados

```powershell
Get-Content .tools/runtime/fase3/neuromorfismo/metricas.json -Encoding UTF8
Get-Content .tools/runtime/fase3/neuromorfismo/divisao.json -Encoding UTF8
```

- `metricas.json`: sementes, quantidade de sessões/janelas, métricas de teste, busca na validação, erros, parâmetros LIF, versões e limites.
- `divisao.json`: IDs das sessões em cada partição; um mesmo ID não pode aparecer em duas listas.
- `previsoes_teste.json`: rótulos e probabilidades das 48 sessões e 432 janelas de teste, permitindo conferir as matrizes.
- O hash esperado dos sinais/rótulos é `24a148963d5de011a00dde738f46687e62eca99e65a051590c5825a0b98d6683`. O hash não inclui tempos de processamento.

### Passo 6 — Executar o notebook inteiro sem precisar instalar um editor

```powershell
.\.venv\Scripts\python.exe scripts/fase3/executar_neuromorfismo.py --notebook
```

- Esse comando lê o notebook entregue e **executa todas as suas células novamente**, usando o mesmo Python do comando. Não se limita a abrir resultados antigos.
- Aguardar `Notebook executado sem erro` e `Visualização:`. Pode demorar mais que a execução simples.
- Abrir a versão de leitura no navegador:

```powershell
Invoke-Item .tools/runtime/fase3/neuromorfismo/comparacao_temporal_lif.html
```

- Ler objetivo, separação, modelos, métricas, gráficos e análise crítica, nessa ordem.
- A cópia executada `.ipynb` também fica nessa pasta. O notebook original em `src/fase3/notebooks/` continua preservado. Ajustamos os links locais na cópia exportada e no HTML para que o guia permaneça acessível a partir da pasta de saída.
- Os gráficos e JSON gerados pelas células ficam em uma pasta nova dentro de `.tools/runtime/fase3/neuromorfismo/notebooks/execucao-...` a cada execução. O notebook mostra o caminho. Isso evita regravar as imagens da comparação simples que ainda possam estar abertas no visualizador do Windows; o HTML incorpora os novos gráficos.
- Não é necessário manter o PowerShell aberto depois do término; não há servidor nesta etapa.
- Para editar interativamente, abrir o notebook em Jupyter ou VS Code e selecionar o Python `.venv/Scripts/python.exe`. Isso é alternativo ao comando já conferido, não um pré-requisito.

### Passo 7 — Rodar as verificações automáticas

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s src/fase3/neuromorfismo/tests -v
```

**Esperado:** nove testes e `OK`: seis dos modelos e três de exportação de links. Verificamos geração reproduzível, ausência de sessões compartilhadas, janelas corretas, disparo/reset/refratariedade, normalização restrita ao treino, agregação e atributos temporais.

### Passo 8 — Validar e encerrar

- [ ] Obtivemos as duas linhas de resultado sem erro.
- [ ] Abrimos os três gráficos e identificamos spikes reais na rede LIF.
- [ ] Conferimos 144/48/48 sessões e as duas matrizes de 48 casos.
- [ ] Executamos o notebook inteiro e abrimos o HTML com resultados.
- [ ] Conferimos os nove testes com `OK`.
- [ ] Entendemos por que o resultado sintético não é um diagnóstico nem uma medida de economia energética.

Esta lista é para quem reproduz preencher durante seu teste. Para a apresentação, seguir o [roteiro do vídeo](ROTEIRO_VIDEO.md); a gravação ainda precisa ser realizada e publicada.

## 🔎 Se algum passo falhar

- **Arquivo ausente:** confirmar a pasta e a versão do projeto. Não inventar um comando para um notebook que ainda não foi publicado.
- **`.venv` não encontrado:** voltar ao passo 2; não executar somente `pip` em outro Python.
- **`ModuleNotFoundError`:** repetir a instalação deste guia usando o mesmo `.venv/Scripts/python.exe`.
- **Caminho longo na instalação:** baixar uma cópia em pasta curta, como `C:\projetos`, e criar um ambiente novo ali. Não mover um `.venv` pronto entre pastas.
- **Erro de kernel:** executar pelo comando do passo 6; ele escolhe explicitamente o Python atual. Conferir instalação de `ipykernel` pelo arquivo de requisitos.
- **`Invalid argument` ao salvar `series.png`:** conferir se a revisão inclui a criação de uma pasta nova por execução do notebook. Na comparação simples, fechar os três gráficos antes de repetir o comando, pois o visualizador do Windows pode impedir sua regravação. Não apagar resultados para contornar o bloqueio.
- **Não abriu HTML/imagem:** confirmar que a execução terminou e localizar a pasta pelo Explorador; abrir o arquivo correspondente com navegador/visualizador. Não há endereço `localhost` para esta trilha.
- **Métricas diferentes:** conferir Python, versões, semente 42 e revisão do código. Preservar saída e hash; diferenças de tempo são esperadas. Não alterar rótulos, remover casos difíceis ou ajustar parâmetros com base no teste para alcançar os números de referência.
- **Ajuda por IA:** fornecer o número do passo, o comando, a saída completa e o resultado de `Get-Location`. Pedir a correção do erro antes de seguir.

No Linux/macOS, trocar o executável por `./.venv/bin/python`, criar com `python3.12 -m venv .venv` e abrir os arquivos com o aplicativo do sistema. A reprodução local registrada foi realizada no Windows; não afirmamos teste manual nesses outros sistemas.

## 📊 Resultados e análise crítica

No teste de 48 sessões, o tradicional acertou **44** e o LIF **35**. Obtivemos acurácia balanceada de **91,67% versus 72,92%**, F1 macro de **0,9165 versus 0,7262** e ROC-AUC de **0,9722 versus 0,7639**. O intervalo bootstrap de 95% da diferença de acurácia balanceada LIF menos tradicional foi de **−31,25 a −8,33 pontos percentuais**, restrito ao conjunto e ao protocolo sintéticos.

O tradicional apresentou três falsos positivos e um falso negativo da classe oscilante; o LIF, nove e quatro. Neste ensaio, os atributos temporais explícitos foram mais úteis que o reservatório aleatório. O LIF demonstra integração temporal e codificação por eventos, mas sua representação e seus pesos fixos podem perder informações úteis. Não ajustamos o experimento para fazê-lo vencer.

Limitamos a análise a uma semente e a dois regimes artificiais. Não controlamos igualmente a quantidade de atributos (8 versus 120). A amostragem de cinco segundos não representa resolução de ECG. O bootstrap não cobre mudanças de gerador, pacientes ou outras sementes. Tempos medidos em CPU não permitem concluir consumo energético, vantagem em hardware ou aplicação clínica.

## 📚 Referências

- Gerstner et al. — [Neuronal Dynamics, modelo LIF](https://neuronaldynamics.epfl.ch/online/Ch1.S3.html).
- Gerstner et al. — [Reservoir computing](https://neuronaldynamics.epfl.ch/online/Ch20.S1.html).
- Scikit-learn — [Prevenção de vazamento e ajuste do pré-processamento](https://scikit-learn.org/stable/common_pitfalls.html).

Adaptamos as equações para um exemplo próprio; não reproduzimos os experimentos do livro. O relatório de duas páginas e o notebook complementam este guia. O vídeo não listado e sua ligação no README raiz continuam necessários para concluir o desafio escolhido pelo grupo.
