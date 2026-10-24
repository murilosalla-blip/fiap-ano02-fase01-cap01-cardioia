# Validação da entrega 1

## O que está disponível

Compilei o firmware para ESP32 e executei o circuito no [projeto público Wokwi](https://wokwi.com/projects/478054573982428161), com DHT22, botão de batimentos e chave de conectividade simulada. Ainda não implementei MQTT. Registrei os resultados em `../../other/fase3/evidencias/entrega1_resultados.md`.

Para reproduzir a montagem no Wokwi, vou criar um projeto ESP32, copiar `cardioia_edge.ino` para `sketch.ino`, criar uma aba `edge_core.h`, substituir `diagram.json` e adicionar a biblioteca de `libraries.txt`. O DHT22 usa a biblioteca recomendada pela documentação Wokwi para ESP32.

## Meu plano de validação

| Cenário | Ação | Resultado esperado |
|---|---|---|
| Coleta offline | Vou iniciar com chave à esquerda e esperar 20 segundos | Linhas `# coleta` a cada cinco segundos; fila cresce; sem JSON de envio |
| Pulsos | Vou pressionar e soltar B seis vezes dentro de uma janela de cinco segundos | Aproximadamente 72 bpm naquela janela; depende da duração efetiva |
| Botão segurado | Vou segurar B por vários segundos | Apenas um pulso por pressão, sem repetição automática |
| Temperatura | Vou alterar temperatura no DHT22 | Nova leitura incorpora o valor após até uma janela |
| Recuperação | Vou mover chave à direita | JSONs antigos saem em ordem, preservando o tempo de coleta; fila esvazia |
| Nova queda | Vou voltar chave à esquerda | Coleta continua; envio para e pendências voltam a crescer |
| Fila cheia | Vou definir `CARDIOIA_QUEUE_CAPACITY` como 3 antes do bloco `#ifndef` e reiniciar offline | A quarta amostra é rejeitada, perdas aumentam e antigas permanecem |
| Reinício | Vou parar e reiniciar | Nova sessão; fila em RAM anterior é perdida, conforme limite documentado |

Após o teste de fila cheia, vou restaurar a capacidade padrão de 2.000. Vou salvar os logs reais em `evidencias/` e registrar o link Wokwi e o resultado de cada cenário. Vou manter o exemplo JSON do contrato separado das evidências de execução.

## Limites conhecidos

- A fila ocupa RAM e não sobrevive a reinício. O firmware informa `sizeof` ao iniciar; a compilação ESP32 deve confirmar o uso total.
- Serial confirma apenas escrita local. A etapa seguinte precisa MQTT e confirmação do consumidor.
- O botão usa polling e exige estado estável por 25 ms; pulsos elétricos curtos não são o objetivo deste protótipo.
- A resolução de uma janela de cinco segundos é de aproximadamente 12 bpm por pulso, suficiente para demonstração, não monitoramento clínico.
- DHT22 representa temperatura do sensor/ambiente, não temperatura corporal validada.
- Não há relógio UTC sincronizado nem persistência externa nesta entrega.

## Referências técnicas

- https://docs.wokwi.com/parts/wokwi-dht22
- https://docs.wokwi.com/parts/wokwi-pushbutton
- https://docs.wokwi.com/parts/wokwi-slide-switch
- https://docs.wokwi.com/diagram-format

## Minha revisão da entrega

Estou revisando a primeira entrega. Reorganizei os componentes, afastei os rótulos dos fios e acrescentei instruções da chave. Também desviei o fio que atravessava o botão. Salvei a nova disposição no projeto e no diagrama local. Em 24/10/2026, concluí os cenários ampliados e restaurei a capacidade padrão de 2.000 leituras. Registrei os resultados em `../../other/fase3/evidencias/2026-10-24/RESULTADOS.md`. Ainda preciso concluir minha revisão final.
