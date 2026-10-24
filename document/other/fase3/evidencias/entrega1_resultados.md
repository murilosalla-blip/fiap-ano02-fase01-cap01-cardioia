# Evidências da primeira entrega

Executei as verificações em 16/10/2026. Salvei o projeto público em: https://wokwi.com/projects/478054573982428161.

## Verificação local

- Testei o núcleo C++ compartilhado com o firmware: FIFO, armazenamento offline, fila cheia, contagem de perdas, ACK incorreto/repetido, reutilização do buffer, BPM e debounce incluindo rollover. Obtive sucesso com o compilador portátil Zig 0.13.0 e C++11.
- Executei os quatro testes Python do contrato com Python 3.12 e jsonschema 4.25.1; todos passaram.
- Compilei o firmware ESP32 com sucesso usando Arduino CLI 1.5.2-rc.1, pacote esp32 2.0.17, DHTesp 1.19.0 e placa `esp32:esp32:esp32doit-devkit-v1`.
- Registrei o uso de flash: 266.741 de 1.310.720 bytes, 20%. Variáveis globais: 101.536 de 327.680 bytes, 30%; 226.144 bytes disponíveis para variáveis locais.
- Medi 40 bytes por estrutura de leitura. A fila de 2.000 ocupa 80.016 bytes no ESP32, conforme Serial. O teste Windows apresentou 80.024 bytes por diferenças de tamanho/alinhamento da plataforma.

No Windows, usei um mapeamento temporário de caminho curto devido ao comprimento do caminho das ferramentas. Configurei a remoção automática desse mapeamento ao terminar. Mantive ferramentas e saídas locais fora do versionamento Git.

## Execução real no simulador

Registrei o estado da interface durante a execução em `wokwi_entrega1_estado.txt`. Extraí desse registro 15 mensagens JSON, validei todas contra o contrato e salvei em `wokwi_entrega1_telemetria.jsonl`. Preservei as mensagens produzidas pelo simulador.

- Iniciei offline e conferi a coleta e o acúmulo das sequências 1 a 4.
- Ativei a chave e conferi a emissão das quatro leituras em ordem, com backlog 4, 3, 2 e 1 e preservação dos tempos de coleta.
- Pressionei o botão seis vezes e conferi a contagem: duas na janela da sequência 10 e quatro na sequência 11. Correspondem a 24 e 48 bpm por janela de cinco segundos. A divisão entre janelas é esperada e não altera o total de seis eventos.
- Conferi a temperatura inicial de 24 °C e alterei o controle do DHT22 para 39 °C. Verifiquei esse valor na sequência 13 e umidade de 40% nas mensagens.
- Identifiquei todas as mensagens como `simulated=true` e `transport=serial_demo`.

## Revisão visual

Reorganizei o diagrama: separei os sensores verticalmente, posicionei os textos fora dos componentes, acrescentei instruções da chave e defini rotas para os fios. Desviei o terra cinza para o contorno inferior, liberando a área do botão. Salvei a disposição atualizada em `wokwi_layout_organizado.png`.

## Ainda pendente

- Vou concluir a revisão final da primeira entrega.
- Concluí em 24/10/2026 os cenários ampliados no simulador: fila cheia com capacidade reduzida, botão segurado e reinício. Registrei a execução e a restauração da capacidade padrão em `2026-10-24/RESULTADOS.md`.
- Vou implementar MQTT, confirmação do consumidor, dashboard e desafios extras nas próximas entregas.
- Criei o workflow de validação localmente; ainda não verifiquei sua execução no GitHub.
