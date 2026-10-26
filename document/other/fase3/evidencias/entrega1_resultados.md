# Evidências da primeira entrega

> Registro histórico da etapa inicial. Preservamos o contexto e os resultados da época; para executar a versão atual, consultar o [guia da Fase 3](../../../fase3/README.md).

Executamos as verificações em 16/10/2026. Salvamos o projeto público em: https://wokwi.com/projects/478054573982428161.

## Verificação local

- Testamos o núcleo C++ compartilhado com o firmware: FIFO, armazenamento offline, fila cheia, contagem de perdas, ACK incorreto/repetido, reutilização do buffer, BPM e debounce incluindo rollover. Obtivemos sucesso com o compilador portátil Zig 0.13.0 e C++11.
- Executamos os quatro testes Python do contrato com Python 3.12 e jsonschema 4.25.1; todos passaram.
- Compilamos o firmware ESP32 com sucesso usando Arduino CLI 1.5.2-rc.1, pacote esp32 2.0.17, DHTesp 1.19.0 e placa `esp32:esp32:esp32doit-devkit-v1`.
- Registramos o uso de flash: 266.741 de 1.310.720 bytes, 20%. Variáveis globais: 101.536 de 327.680 bytes, 30%; 226.144 bytes disponíveis para variáveis locais.
- Medimos 40 bytes por estrutura de leitura. A fila de 2.000 ocupa 80.016 bytes no ESP32, conforme Serial. O teste Windows apresentou 80.024 bytes por diferenças de tamanho/alinhamento da plataforma.

No Windows, usamos um mapeamento temporário de caminho curto devido ao comprimento do caminho das ferramentas. Configuramos a remoção automática desse mapeamento ao terminar. Mantivemos ferramentas e saídas locais fora do versionamento Git.

## Execução real no simulador

Registramos o estado da interface durante a execução em `wokwi_entrega1_estado.txt`. Extraímos desse registro 15 mensagens JSON, validamos todas contra o contrato e salvamos em `wokwi_entrega1_telemetria.jsonl`. Preservamos as mensagens produzidas pelo simulador.

- Iniciamos offline e conferimos a coleta e o acúmulo das sequências 1 a 4.
- Ativamos a chave e conferimos a emissão das quatro leituras em ordem, com backlog 4, 3, 2 e 1 e preservação dos tempos de coleta.
- Pressionamos o botão seis vezes e conferimos a contagem: duas na janela da sequência 10 e quatro na sequência 11. Correspondem a 24 e 48 bpm por janela de cinco segundos. A divisão entre janelas é esperada e não altera o total de seis eventos.
- Conferimos a temperatura inicial de 24 °C e alteramos o controle do DHT22 para 39 °C. Verificamos esse valor na sequência 13 e umidade de 40% nas mensagens.
- Identificamos todas as mensagens como `simulated=true` e `transport=serial_demo`.

## Revisão visual

Reorganizamos o diagrama: separamos os sensores verticalmente, posicionamos os textos fora dos componentes, acrescentamos instruções da chave e definimos rotas para os fios. Desviamos o terra cinza para o contorno inferior, liberando a área do botão. Salvamos a disposição atualizada em `wokwi_layout_organizado.png`.

## Ainda pendente

- Vamos concluir a revisão final da primeira entrega.
- Concluímos em 24/10/2026 os cenários ampliados no simulador: fila cheia com capacidade reduzida, botão segurado e reinício. Registramos a execução e a restauração da capacidade padrão em `2026-10-24/RESULTADOS.md`.
- Vamos implementar MQTT, confirmação do consumidor, dashboard e desafios extras nas próximas entregas.
- Criamos o workflow de validação localmente; ainda não verificamos sua execução no GitHub.
