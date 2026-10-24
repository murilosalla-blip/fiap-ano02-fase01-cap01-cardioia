# Verificações da entrega 1

Usei no teste C++ o mesmo `edge_core.h` incluído pelo firmware. Verifiquei armazenamento offline, ordem, fila cheia, perdas, confirmações incorretas/repetidas, reutilização do buffer e debounce na pressão/soltura, incluindo rollover de tempo.

Para reproduzir os testes com um compilador C++11, vou executar:

```sh
g++ -std=c++11 -Wall -Wextra -Werror fase3/tests/test_edge_core.cpp -o test_edge_core
./test_edge_core
```

Para verificar o contrato, vou executar:

```sh
python -m pip install -r fase3/requirements-dev.txt
python -m unittest discover -s fase3/tests -p 'test_*.py' -v
```

Esses testes não substituem execução de sensores no simulador ou transmissão MQTT. O exemplo JSON validado é uma mensagem de referência, não saída de um sensor.

Para compilar o firmware com Arduino CLI, vou executar:

```sh
arduino-cli core update-index --additional-urls https://espressif.github.io/arduino-esp32/package_esp32_index.json
arduino-cli core install esp32:esp32@2.0.17 --additional-urls https://espressif.github.io/arduino-esp32/package_esp32_index.json
arduino-cli lib install 'DHT sensor library for ESPx@1.19.0'
arduino-cli compile --fqbn esp32:esp32:esp32doit-devkit-v1 fase3/firmware/cardioia_edge
```

Fixei a versão do pacote ESP32 para reproduzir esta entrega. Isolei as ferramentas em `.tools/`, sem modificar o ambiente global.

## Evidências dos cenários ampliados

Conferi os registros reais do Wokwi com o comando abaixo. O verificador lê as capturas de 24/10/2026, confere as mensagens contra o contrato e verifica a ordem, as perdas, o pulso único, o reinício e a restauração da capacidade padrão. Não gera dados de sensores.

```sh
python fase3/scripts/validar_cenarios_edge.py
```
