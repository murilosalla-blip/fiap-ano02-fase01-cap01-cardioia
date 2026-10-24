# Validação dos cenários ampliados do Edge

Executei estes testes em 24/10/2026 no [projeto CardioIA no Wokwi](https://wokwi.com/projects/478054573982428161). Usei o circuito reorganizado e o mesmo firmware da primeira entrega. Alterei temporariamente apenas a capacidade da fila no arquivo inicial da simulação, sem salvar essa alteração no projeto público.

## Botão segurado

Mantive o botão pressionado por sete segundos. Na recuperação das mensagens, conferi um único pulso na sequência 3, equivalente a 12 bpm na janela de cinco segundos, e nenhum pulso adicional nas demais mensagens capturadas. Confirmei que segurar o botão não produz contagem contínua e que soltá-lo não gera um novo pulso por repique.

## Fila cheia e recuperação

Defini `CARDIOIA_QUEUE_CAPACITY` como 3 no arquivo `sketch.ino` para atingir o limite sem esperar milhares de amostras. Iniciei com a chave offline e observei:

| Leitura | Resultado que conferi |
|---|---|
| Sequências 1 a 3 | Armazenei três leituras sem perdas |
| Sequência 4 | Conferi fila mantida em 3 e primeira perda contabilizada |
| Sequências 5 e 6 | Conferi o crescimento do contador até três perdas, sem substituir as pendências antigas |
| Reconexão | Recuperei as sequências 1, 2 e 3 em ordem |
| Nova coleta durante a recuperação | Conferi o armazenamento e envio da sequência 7 após liberar a primeira posição |
| Continuidade | Conferi o envio da sequência 8 e manutenção do contador em três perdas |

Preservei os registros em `fila_cheia_offline.txt` e `fila_cheia_recuperacao.txt`. Extraí cinco mensagens reais para `fila_cheia_recuperacao.jsonl` e validei todas contra o contrato. Conferi as sequências `[1, 2, 3, 7, 8]`: as lacunas 4, 5 e 6 correspondem às perdas registradas.

Observei que o backlog pode permanecer momentaneamente em três durante a recuperação, pois a coleta continua enquanto envio as pendências. Conferi a ordem dos dados e a capacidade da fila, sem exigir uma redução a cada mensagem quando há coleta concorrente no fluxo principal.

## Reinício com pendências

Voltei à condição offline e acumulei as sequências 12, 13 e 14. Antes do reinício, registrei a sessão `8138d6c080d852d7`, três leituras pendentes e o descarte da sequência 15 por fila cheia.

Reiniciei a simulação e conferi a nova sessão `9be268f5e539c9bd`. Observei a primeira leitura com sequência 1, fila 1 e perdas 0, seguida da leitura 2 com fila 2 e perdas 0. Confirmei que as leituras pendentes da sessão anterior não permaneceram na fila.

Registrei as observações em `antes_reinicio.txt`, `apos_reinicio.txt` e `reinicio.png`. Confirmei a limitação já documentada: mantenho a fila em RAM, portanto não preservo pendências após reiniciar. Minha resiliência nesta versão cobre interrupção da conectividade enquanto o dispositivo continua ligado.

## Restauração da configuração padrão

Removi a definição temporária de capacidade 3 e restaurei o conteúdo original de `sketch.ino`. Executei novamente e conferi no Serial `capacidade=2000`, `tamanho_amostra=40` e `bytes_fila=80016`. Observei dez leituras armazenadas offline sem perdas no registro `capacidade_restaurada.txt`.

Mantive a configuração pública original e não publiquei a variante de teste. Não alterei a lógica do firmware nem as ligações do circuito nesta execução.

## Conferência reproduzível

Criei `fase3/scripts/validar_cenarios_edge.py` para conferir os arquivos capturados. Executei:

```sh
python fase3/scripts/validar_cenarios_edge.py
```

Obtive aprovação das verificações de fila cheia, ordem, perdas, pulso único, troca de sessão, reinício da fila e restauração da capacidade. Registrei o resultado estruturado em `validacao_cenarios.json`.

## Situação da primeira entrega

Concluí a implementação e os testes técnicos previstos para a primeira entrega, incluindo os cenários ampliados. Ainda preciso concluir minha revisão final da entrega. Vou implementar transmissão MQTT e confirmação do consumidor na etapa seguinte; nesta etapa, validei exclusivamente a demonstração Serial local.
