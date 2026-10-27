# Conferência de reprodução da Fase 3 - 27/10/2026

## Cópia de avaliação e preparação

Clonamos o repositório público no commit `2db8a63996cc6b9caf0b111fbc9777ff2eadad0a` em uma pasta temporária curta. Aplicamos a revisão local ainda não publicada nessa cópia, incluindo o REST e os guias atualizados. Criamos um novo `.venv` com Python 3.12 e instalamos os requisitos da Fase 3. Instalamos o painel com `npm.cmd ci --prefix src/fase3/node-red --ignore-scripts --no-audit --no-fund`, usando Node.js 24.19.0. As instalações concluíram com saída zero.

Não reaproveitamos os ambientes ou os bancos da cópia de desenvolvimento. A validação refere-se ao clone com a revisão local aplicada; um clone da main pública ainda não contém essa revisão.

## Parte 1 - execução observada no Wokwi

Abrimos o projeto Serial público sem login. Observamos capacidade de 2.000 posições, quatro leituras acumuladas offline e recuperação das sequências 1 a 4 em ordem ao mover a chave à direita. A sequência 4 preservou temperatura de 31 °C e um pulso, equivalente a 12 BPM; não apresentamos esse acionamento único como teste de seis pulsos. As leituras seguintes continuaram sendo coletadas e enviadas, sem perdas informadas.

- [Valores observados no Monitor Serial](edge_serial.json).
- [Captura da recuperação](edge_recuperacao.png).

## Parte 2 - integração MQTT e painel

Iniciamos painel e consumidor pelo comando documentado, com o Python do ambiente novo. Conferimos conexão e assinaturas no broker, gravação, retorno de ACK no Serial e atualização do painel local. Na sessão `d563998d74168c20`, persistimos 14 medições, sequências 1 a 14; o gráfico recebeu pulsos de 12, 48 e 60 BPM durante os acionamentos. Outra sessão da tentativa de retomada registrou duas medições. A [consulta de persistência](mqtt_persistencia.json) registra esses totais.

A tentativa de repetir todos os passos visuais de alerta e recuperação pelo Wokwi não foi concluída: o controle do navegador sofreu timeouts e uma interrupção de proteção ao verificar a janela no Windows. Não registramos essa reexecução integral como aprovada. Mantemos as [evidências guiadas anteriores do painel](../../2026-10-24/dashboard/validacao_guiada/RESULTADOS.md), sem alterar sua data ou origem.

Para conferir o painel instalado com uma fonte controlada, executamos o roteiro de rede já documentado em namespace separado, porta 1881, com publicador Python e broker real. Aprovamos os 12 cenários: leitura atual, reenvio, rejeição de inconsistência, primeira janela de limite, alerta confirmado, permanência, dado recuperado, retorno à faixa, sensor indisponível, interrupção, reconexão e falta de dados recentes.

- [Resultado do ensaio de rede](painel_broker/resultado.json).
- [Entrada dos dois alertas](painel_broker/05_alerta_confirmado.json).
- [Retorno à faixa](painel_broker/08_saida_alerta.json).
- [Interrupção](painel_broker/10_offline.json), [reconexão](painel_broker/11_reconectado.json) e [falta de atualização](painel_broker/12_sem_dados_recentes.json).

Esse ensaio valida a integração do broker com as regras do painel; sua origem é explicitamente um publicador Python, sem ESP32. Não equivale a mover a chave física simulada nem substitui os registros anteriores do firmware.

## Ir Além 1 - REST completo após reinício

Iniciamos a API pelo comando do PDF, conferimos `/saude` no navegador, executamos o cliente e consultamos as cinco leituras. Geramos dois arquivos locais de e-mail. Encerramos a API, iniciamos novamente e repetimos somente `--consultar`. Comparamos os JSONs antes e depois: as cinco leituras, horários, sessão e referências aos e-mails permaneceram idênticos, sem gerar outra mensagem.

- [Resultado inicial da demonstração](resultado_demonstracao.json).
- [Consulta antes do reinício](consulta_antes_reinicio.json) e [consulta após reinício](consulta_apos_reinicio.json).
- [Primeiro e-mail](alerta-0001.eml) e [segundo e-mail](alerta-0002.eml), com assunto de simulação, destinatário fictício e motivos correspondentes.

## Testes adicionais e ajuste das instruções

Aprovamos os 23 testes Python da Fase 3 e os 19 testes das regras do painel nessa cópia. Esses testes complementam a reprodução; não representam novas leituras de sensores.

Identificamos e corrigimos uma ambiguidade nos guias e no PDF MQTT: a linha inicial `Painel: ...` anuncia o endereço antes de o Node-RED terminar de carregar. Agora orientamos aguardar `Server now running` e `Started flows` antes de abrir a página. Também explicitamos que, no teste Serial offline, os valores dos sensores são conferidos nos JSONs recuperados após reconectar.

Mantivemos os relatórios com duas páginas em Edge, quatro em MQTT/dashboard e duas em REST/e-mail. Conferimos a renderização dos PDFs alterados e a preservação dos arquivos anteriores. A revisão não comprova instalação em outro sistema operacional, disponibilidade futura dos serviços externos, publicação dos novos arquivos ou submissão na FIAP.

## Complemento - repetição visual acompanhada concluída

Concluímos posteriormente os passos visuais com operação acompanhada no Wokwi. Na sessão `66d5bec5f7007c6a`, verificamos entrada e retorno dos alertas de pulsos e temperatura, interrupção pela chave e recuperação. Conferimos 41 medições únicas, sem lacunas e com zero perdas; o Serial confirmou fila zero a partir da recuperação na sequência 39. A [validação guiada](validacao_guiada/RESULTADOS.md) preserva as capturas, os dados e os resultados de cada passo. Assim encerramos a pendência visual descrita na primeira tentativa, sem reclassificar os ensaios Python como dados do ESP32.
