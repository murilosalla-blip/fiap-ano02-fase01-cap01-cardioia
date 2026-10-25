# Fase 3 — requisitos, evidências e pendências

Acompanhamos separadamente implementação, teste, documentação e submissão. Reavaliamos este checklist em **25/10/2026**, com os textos fornecidos, o enunciado Word arquivado e suas duas imagens. O prazo informado é **04/11/2026, às 23h59**. Os documentos e as evidências de testes abaixo não representam submissão concluída.

## Critérios da atividade obrigatória — 10 pontos

| Critério do enunciado | Pontos | Como avaliar e localizar | Situação |
|---|---:|---|---|
| Leitura de sensores | 2 | ESP32 com DHT22 (um sensor) e botão de pulsos (segunda entrada simulada); código comentado em `src/fase3/firmware/`; projetos públicos identificados no [guia](README.md) | Implementamos e validamos no Wokwi |
| Resiliência offline | 2 | Chave booleana, coleta offline, fila FIFO de 2.000 amostras, sincronização e perdas contabilizadas; [resultados Edge](../other/fase3/evidencias/2026-10-24/RESULTADOS.md) | Validamos recuperação, limite, botão segurado e reinício; documentamos volatilidade da RAM |
| MQTT e broker | 2 | Firmware `cardioia_mqtt`, broker real, consumidor SQLite e ACK; [resultados MQTT](../other/fase3/evidencias/2026-10-24/mqtt/RESULTADOS.md) | Validamos transmissão, persistência, reenvio e recuperação |
| Dashboard e alertas | 2 | [Export Node-RED](../../src/fase3/node-red/flows.json), gráfico de BPM, gauge ambiental e alertas; [capturas](../../assets/fase3/evidencias/) e [validação guiada](../other/fase3/evidencias/2026-10-24/dashboard/validacao_guiada/RESULTADOS.md) | Validamos gráfico, temperatura, entrada e retorno dos alertas e estabilidade |
| Documentação clara: código e relatórios | 2 | README e guias de execução, C++ comentado, relatório Edge **≥1 página** e relatório MQTT/dashboard **≥2 páginas** | Revisamos os guias; **os dois relatórios finais continuam pendentes** |

Não atribuímos nota antecipada a esta matriz. A avaliação pertence à FIAP; a implementação testada não dispensa os relatórios ou a entrega na plataforma.

## Conferência detalhada dos artefatos

| Requisito | Entrega | Evidência prevista | Estado |
|---|---:|---|---|
| ESP32 no Wokwi e dois sensores distintos, incluindo DHT22 | 1 | Sketch, diagrama e projeto público | Compilamos, conferimos no simulador e concluímos a revisão da primeira entrega |
| Coleta periódica e conectividade booleana | 1 | Firmware e demonstração Serial | Conferimos no Wokwi e salvamos registros em `document/other/fase3/evidencias/` |
| Resiliência offline e armazenamento limitado | 1–2 | Fila, testes e cenário de recuperação | Testamos o núcleo C++ e conferimos no Wokwi recuperação Serial, fila cheia, botão segurado e reinício; também implementamos MQTT, confirmamos reenvio e recuperação após reiniciar o consumidor |
| C++ comentado e link Wokwi | 1 | `src/fase3/firmware/cardioia_edge/` e https://wokwi.com/projects/478054573982428161 | Comentamos o código, publicamos o link e reorganizamos o circuito durante nossa revisão |
| Relatório Edge mínimo uma página | 6 | PDF final | Ainda precisamos concluir |
| Transmissão MQTT e broker | 2 | Firmware compilado, consumidor, eventos de rede e projeto https://wokwi.com/projects/478772789361460225 | Confirmamos a troca real do ESP32 pelo broker, a confirmação após persistência e a recuperação após reiniciar o consumidor; também conferimos falha controlada do endpoint, recuperação ordenada e retorno à fila vazia |
| Dashboard Node-RED com gráfico, gauge e alerta | 3 | `src/fase3/node-red/flows.json` e `document/other/fase3/evidencias/2026-10-24/dashboard/` | Implementamos e testamos regras, rede e recebimento do ESP32; concluímos a revisão visual guiada com entrada e retorno dos dois alertas |
| Relatório MQTT/dashboard mínimo duas páginas | 6 | PDF final | Ainda precisamos concluir |
| Ir Além 1 cliente REST envia e recebe | 4 | Python e teste HTTP | Ainda precisamos concluir |
| Ir Além 1 regras de risco e e-mail simulado | 4 | Código, teste e e-mail demonstrativo | Ainda precisamos concluir |
| Ir Além 1 relatório de uma a duas páginas | 4 | PDF final | Ainda precisamos concluir |
| Ir Além 2 classificador tradicional e LIF/FHN | 5 | Notebook executado e resultados | Ainda precisamos concluir |
| Ir Além 2 repositório público, código e README | 5–6 | Código da comparação, notebook e reprodução | O repositório já é público; ainda precisamos implementar e publicar os artefatos específicos do desafio |
| Ir Além 2 relatório comparativo de duas páginas | 5 | PDF final | Ainda precisamos concluir |
| Ir Além 2 vídeo até quatro minutos não listado | 5 | YouTube e link README | Ainda precisamos concluir |
| Clareza, organização e revisão de evidências | Todas | Roteiro e pacote final | Estamos acompanhando as evidências |

SPIFFS e hardware físico não são obrigatórios segundo o enunciado fornecido; Grafana é opcional. A implementação Serial da primeira entrega não satisfaz, sozinha, a Parte 2 de MQTT.

## Exigências, exemplos e escolhas do grupo

- **Obrigatórios:** dois sensores/entradas distintos, incluindo DHT22; coleta periódica e conectividade booleana; armazenamento limitado na ordem de milhares de amostras, com estratégia explícita; sincronização; código comentado e link Wokwi; MQTT com broker; Node-RED com gráfico, gauge e alerta; relatórios com os mínimos de páginas.
- **Opcionais:** SPIFFS no simulador, hardware físico, microSD e Grafana. Não apresentamos SPIFFS como realizado.
- **Escolhas da implementação:** cinco segundos simulados por coleta, 2.000 posições, descarte da amostra nova quando a fila enche, reenvio em três segundos, dado atual por 15 segundos reais, histerese e confirmação em duas janelas. Sete segundos no teste de botão segurado foi uma duração de ensaio, não um critério da FIAP.
- **Limites de alerta:** >120 BPM para pulsos artificiais e >30 °C para temperatura ambiente. O >38 °C citado no enunciado é exemplo, não obrigação de medir temperatura corporal. Zero pulsos indica ausência de acionamentos, não ausência de atividade cardíaca.
- **Ir Além 1:** o cliente Python precisa **enviar e receber** por REST, verificar risco e simular e-mail. O endpoint de consulta do painel não satisfaz sozinho esse requisito. O relatório deve ter **uma a duas páginas**.
- **Ir Além 2:** classificador tradicional comparado a LIF ou FHN em séries temporais, notebook comentado, código e README públicos, relatório de **duas páginas** e vídeo de **até quatro minutos**, não listado no YouTube, com link no README raiz. Ainda não temos esse vídeo; o link da Fase 2 não o substitui.

## Aceite antes da submissão

- [ ] Concluir e conferir a paginação dos dois relatórios obrigatórios e dos dois relatórios Ir Além.
- [ ] Executar o cliente REST, a simulação de e-mail e os dois modelos comparáveis, preservando suas evidências.
- [ ] Publicar o vídeo específico do Ir Além 2 e inserir o link no README raiz.
- [ ] Reproduzir a entrega em cópia nova, incluindo instalação e cenários com resultado esperado.
- [ ] Conferir acesso sem autenticação obrigatória aos links públicos, dados e vídeo; preservar também os links das fases anteriores.
- [ ] Conferir integrantes/RMs no pacote e cadastro do grupo na plataforma antes do envio. O recorte fornecido da Fase 3 lista apenas um participante; precisamos conferir o cadastro efetivo, sem alterar a identificação coletiva do projeto com base nesse recorte.
- [ ] Conferir o arquivo correto, enviar pela plataforma com antecedência e reabrir/baixar o arquivo enviado para confirmar o conteúdo. A imagem de orientação avisa que não é possível substituir o arquivo após o fechamento da entrega ou a correção.
- [ ] Registrar o envio efetivamente confirmado, sem confundir merge no GitHub com submissão na FIAP.
