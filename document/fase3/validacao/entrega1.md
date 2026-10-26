# Validação da Parte 1 — Edge e recuperação Serial

## Escopo desta demonstração

Implementamos e validamos o circuito ESP32 com DHT22, botão de pulsos e chave de conectividade no [Wokwi Serial](https://wokwi.com/projects/478054573982428161). Nesta variante, demonstramos a recuperação pela saída Serial, identificada como `serial_demo`. A integração real já está implementada separadamente no [Wokwi MQTT](https://wokwi.com/projects/478772789361460225), conforme o [guia MQTT](../mqtt/README.md).

Para reproduzir a montagem, criar um projeto ESP32, copiar `src/fase3/firmware/cardioia_edge/cardioia_edge.ino` para `sketch.ino`, criar a aba `edge_core.h`, substituir `diagram.json` e adicionar a biblioteca de `libraries.txt`, todos da mesma pasta. Alternativamente, executar diretamente o projeto público.

## Como reproduzir os cenários

Contar os intervalos pelo relógio do ESP32 simulado; manter o Wokwi visível para evitar desaceleração em segundo plano.

| Cenário | Ação | Resultado esperado |
|---|---|---|
| Coleta offline | Iniciar com a chave à esquerda e aguardar quatro coletas | Linhas `# coleta` a cada cinco segundos simulados; fila cresce, sem JSON de envio |
| Pulsos | Pressionar e soltar B seis vezes dentro de uma janela de cinco segundos | Aproximadamente 72 BPM naquela janela |
| Botão segurado | Segurar B por vários segundos | Um pulso por pressão, sem repetição automática |
| Temperatura | Alterar a temperatura no DHT22 | Nova leitura incorpora o valor após até uma janela |
| Recuperação | Mover a chave à direita | JSONs antigos saem em ordem, preservando o tempo de coleta; fila esvazia |
| Nova queda | Voltar a chave à esquerda | Coleta continua; envio para e pendências voltam a crescer |
| Fila cheia | Definir `CARDIOIA_QUEUE_CAPACITY` como 3 antes do bloco `#ifndef` e reiniciar offline | A quarta amostra é rejeitada; perdas aumentam e antigas permanecem |
| Reinício | Parar e reiniciar com pendências | Nova sessão; fila em RAM anterior é perdida |

Após testar fila cheia, restaurar a capacidade padrão de 2.000 leituras. Salvar logs reais separadamente dos exemplos de contrato. Conferir os registros preservados com `python scripts/fase3/validar_cenarios_edge.py` a partir da raiz; consultar os argumentos em `--help`.

## Limites da implementação

- A fila ocupa RAM e não sobrevive ao reinício; a compilação confirma o uso total de memória.
- Serial confirma escrita local. O consumidor e seu ACK confirmam persistência somente na variante MQTT.
- O botão usa polling e exige estado estável por 25 ms; pulsos elétricos curtos não são o objetivo do protótipo.
- A janela de cinco segundos produz resolução de aproximadamente 12 BPM por pulso. Não validamos monitoramento clínico.
- DHT22 representa temperatura do sensor/ambiente, não temperatura corporal validada.
- Não implementamos relógio UTC sincronizado nem persistência externa no ESP32.

## Resultados preservados

Concluímos os cenários ampliados em 24/10/2026, incluindo fila cheia, botão segurado e reinício, e restauramos a capacidade padrão. Preservamos os [resultados e logs](../../other/fase3/evidencias/2026-10-24/RESULTADOS.md) e identificamos o [primeiro ensaio](../../other/fase3/evidencias/entrega1_resultados.md) como histórico. Produzimos o [relatório Edge de duas páginas](../CardioIA_Fase3_Relatorio_Edge.pdf) e conferimos sua paginação. A revisão final do grupo permanece indicada na [matriz de requisitos](../CHECKLIST_ENUNCIADO.md).

## Referências técnicas

- https://docs.wokwi.com/parts/wokwi-dht22
- https://docs.wokwi.com/parts/wokwi-pushbutton
- https://docs.wokwi.com/parts/wokwi-slide-switch
- https://docs.wokwi.com/diagram-format
