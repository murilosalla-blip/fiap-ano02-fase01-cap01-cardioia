# Verificações da Fase 3

Reunimos os testes de contrato, fila, confirmações, persistência e painel, além dos validadores das evidências existentes. Para avaliar os sensores e a demonstração completa, seguir também o [guia de reprodução](../README.md). Testes automatizados não substituem a execução do Wokwi nem os relatórios obrigatórios.

Executar os comandos na raiz do repositório. Os exemplos Python abaixo usam o ambiente `.venv` no Windows; no Linux/macOS, substituir `.\.venv\Scripts\python.exe` por `./.venv/bin/python`. Para os testes C++, utilizar um terminal com compilador `g++` compatível com C++11; a instalação desse compilador é opcional para quem avalia diretamente pelo Wokwi.

## Contratos, persistência e preservação

```powershell
.\.venv\Scripts\python.exe -m pip install -r config/fase3/requirements-mqtt.txt -r config/fase3/requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest discover -s src/fase3/tests -p 'test_*.py' -v
.\.venv\Scripts\python.exe -m unittest discover -s scripts/tests -p 'test_*.py' -v
.\.venv\Scripts\python.exe scripts/validar_organizacao.py
.\.venv\Scripts\python.exe scripts/fase1/verificar_preservacao.py
```

Resultado esperado: 16 testes Python da Fase 3 e seis testes de proteção aprovados; integridade e links locais válidos. Conferimos persistência antes do ACK, reenvio, duplicatas, conflitos, falhas e migração sem sobrescrever dados anteriores. O exemplo JSON validado é uma referência do contrato, não uma saída de sensor.

## Regras e fluxo Node-RED

```powershell
npm ci --prefix src/fase3/node-red --ignore-scripts --no-audit --no-fund
node --test src/fase3/tests/test_dashboard.cjs
```

Resultado esperado: 19 testes aprovados, incluindo confirmação dos alertas em duas janelas, histerese, recuperação, falta de atualização, identidade, deduplicação e limite do histórico. Para regenerar o export após uma alteração intencional do fluxo, consultar o [guia Node-RED](../node-red/README.md).

## Núcleos C++ compartilhados com o firmware

```sh
python -c "from pathlib import Path; Path('.tools/tmp').mkdir(parents=True, exist_ok=True)"
g++ -std=c++11 -Wall -Wextra -Werror src/fase3/tests/test_edge_core.cpp -o .tools/tmp/test_edge_core.exe
./.tools/tmp/test_edge_core.exe
g++ -std=c++11 -Wall -Wextra -Werror src/fase3/tests/test_mqtt_delivery.cpp -o .tools/tmp/test_mqtt_delivery.exe
./.tools/tmp/test_mqtt_delivery.exe
```

Usar nesse primeiro comando o mesmo executável Python do ambiente. A extensão `.exe` permite manter os nomes dos comandos no Windows; os mesmos nomes também podem ser executados em Linux/macOS. Gravamos os executáveis fora do versionamento.

Resultado esperado: mensagens `PASS` para FIFO, funcionamento offline, overflow, perdas, ACK incorreto/repetido, rollover, BPM e debounce; depois `PASS` para confirmação, timeout e reenvio. Os testes incluem os mesmos cabeçalhos usados pelo ESP32.

## Registros preservados dos cenários no Wokwi

```powershell
.\.venv\Scripts\python.exe scripts/fase3/validar_cenarios_edge.py
.\.venv\Scripts\python.exe scripts/fase3/validar_cenarios_mqtt.py document/other/fase3/evidencias/2026-10-24/mqtt
```

Os verificadores leem as capturas existentes e atualizam seus arquivos de resultado. Conferimos ordem, perdas, pulso único, reinício, capacidade restaurada, ACK omitido, reenvio, deduplicação e recuperação. Resultado esperado: cenários aprovados. Essa execução não gera dados de sensores nem representa nova simulação manual.

## Compilação local opcional das duas variantes ESP32

Com Arduino CLI instalado e disponível no terminal:

```sh
arduino-cli core update-index --additional-urls https://espressif.github.io/arduino-esp32/package_esp32_index.json
arduino-cli core install esp32:esp32@2.0.17 --additional-urls https://espressif.github.io/arduino-esp32/package_esp32_index.json
arduino-cli lib install "DHT sensor library for ESPx@1.19.0"
arduino-cli lib install "PubSubClient@2.8.0"
arduino-cli lib install "ArduinoJson@6.21.5"
arduino-cli compile --fqbn esp32:esp32:esp32doit-devkit-v1 src/fase3/firmware/cardioia_edge
arduino-cli compile --fqbn esp32:esp32:esp32doit-devkit-v1 src/fase3/firmware/cardioia_mqtt
```

Resultado esperado: compilação das duas variantes sem erros e relatório do uso de memória. Fixamos as versões utilizadas na compilação validada; executar a simulação pelos projetos públicos continua dispensando a instalação local do Arduino CLI.
