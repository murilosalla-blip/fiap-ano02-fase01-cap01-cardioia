# Validação do painel Node-RED

Antes dos comandos, concluir a [preparação da Fase 3](../README.md#como-reproduzir--preparação), incluindo criação de `.venv` e instalação das dependências. Executar na raiz do repositório. Cada terminal novo precisa entrar nessa mesma pasta; o terminal do servidor permanece aberto durante os testes.

## Como reproduzir os cenários

No PowerShell, selecionar o interpretador antes de iniciar: `$env:CARDIOIA_PYTHON = (Resolve-Path .\.venv\Scripts\python.exe).Path`.

1. Iniciar painel e consumidor com `node scripts/fase3/iniciar_dashboard.js --com-consumidor` na raiz, após instalar as dependências do [guia da fase](../README.md). Utilizar apenas uma instância do consumidor no tópico.
2. Abrir `http://127.0.0.1:1880/dashboard/monitoramento` e conferir o estado inicial sem dados atuais.
3. Executar o [Wokwi MQTT](https://wokwi.com/projects/478772789361460225), mover a chave à direita e manter simulador e painel visíveis. Conferir leituras, temperatura, gráfico e última confirmação.
4. Acionar e soltar o botão mais de dez vezes por janela, em duas janelas de cinco segundos simulados. Conferir entrada do alerta acima de 120 BPM.
5. Deixar de acionar o botão e conferir retorno após duas leituras atuais até 108 BPM. Zero pulsos representa ausência de acionamentos do botão, não ausência de atividade cardíaca.
6. Alterar o DHT22 para 31 °C e aguardar duas leituras atuais. Ajustar para 28 °C ou menos e conferir o retorno em duas leituras.
7. Mover a chave à esquerda e manter a coleta. Conferir a interrupção e o último valor em cinza. Reconectar e conferir os pontos recuperados no histórico, sem disparar alertas atuais com leituras antigas.
8. Manter consumidor e painel ativos e parar o Wokwi. Conferir o estado MQTT e a indicação de falta de leitura atual após 15 segundos reais. A conexão do broker é independente da atualidade do dado.

Coletamos a cada cinco segundos do relógio simulado do ESP32. Uma simulação desacelerada pode demorar mais no relógio real; manter o Wokwi visível durante o teste.

## Resultados preservados

Concluímos a revisão funcional no Chrome, incluindo gráfico, gauge, entrada e retorno dos alertas de pulsos e temperatura e conferência de 27 medições únicas. Preservamos as capturas e resultados na [validação guiada](../../other/fase3/evidencias/2026-10-24/dashboard/validacao_guiada/RESULTADOS.md).

Na implementação inicial, aprovamos 15 testes locais; após a correção de estabilidade, aprovamos 19 testes. Mantemos os [12 cenários finais de rede](../../other/fase3/evidencias/2026-10-24/dashboard/RESULTADOS.md) separados das leituras produzidas pelo ESP32. Registramos a observação de 101 segundos e a separação entre conexão e atualidade na [validação de estabilidade](../../other/fase3/evidencias/2026-10-24/dashboard/estabilidade/RESULTADOS.md).

Para repetir as verificações locais, executar `node --test src/fase3/tests/test_dashboard.cjs`. Produzimos o [relatório MQTT/dashboard de quatro páginas](../CardioIA_Fase3_Relatorio_MQTT_Dashboard.pdf) e conferimos sua paginação. A revisão final do grupo e os desafios continuam identificados na [matriz de requisitos](../CHECKLIST_ENUNCIADO.md); a validação do painel não encerra toda a Fase 3.
