# Validação dos cenários ampliados do Edge

Executamos estes testes em 24/10/2026 no [projeto CardioIA no Wokwi](https://wokwi.com/projects/478054573982428161). Usamos o circuito reorganizado e o mesmo firmware da primeira entrega. Alteramos temporariamente apenas a capacidade da fila no arquivo inicial da simulação, sem salvar essa alteração no projeto público.

## Botão segurado

Mantivemos o botão pressionado por sete segundos. Na recuperação das mensagens, conferimos um único pulso na sequência 3, equivalente a 12 bpm na janela de cinco segundos, e nenhum pulso adicional nas demais mensagens capturadas. Confirmamos que segurar o botão não produz contagem contínua e que soltá-lo não gera um novo pulso por repique.

## Fila cheia e recuperação

Definimos `CARDIOIA_QUEUE_CAPACITY` como 3 no arquivo `sketch.ino` para atingir o limite sem esperar milhares de amostras. Iniciamos com a chave offline e observamos:

| Leitura | Resultado que conferimos |
|---|---|
| Sequências 1 a 3 | Armazenamos três leituras sem perdas |
| Sequência 4 | Conferimos fila mantida em 3 e primeira perda contabilizada |
| Sequências 5 e 6 | Conferimos o crescimento do contador até três perdas, sem substituir as pendências antigas |
| Reconexão | Recuperamos as sequências 1, 2 e 3 em ordem |
| Nova coleta durante a recuperação | Conferimos o armazenamento e envio da sequência 7 após liberar a primeira posição |
| Continuidade | Conferimos o envio da sequência 8 e manutenção do contador em três perdas |

Preservamos os registros em `fila_cheia_offline.txt` e `fila_cheia_recuperacao.txt`. Extraímos cinco mensagens reais para `fila_cheia_recuperacao.jsonl` e validamos todas contra o contrato. Conferimos as sequências `[1, 2, 3, 7, 8]`: as lacunas 4, 5 e 6 correspondem às perdas registradas.

Observamos que o backlog pode permanecer momentaneamente em três durante a recuperação, pois a coleta continua enquanto envio as pendências. Conferimos a ordem dos dados e a capacidade da fila, sem exigir uma redução a cada mensagem quando há coleta concorrente no fluxo principal.

## Reinício com pendências

Voltamos à condição offline e acumulamos as sequências 12, 13 e 14. Antes do reinício, registramos a sessão `8138d6c080d852d7`, três leituras pendentes e o descarte da sequência 15 por fila cheia.

Reiniciamos a simulação e conferimos a nova sessão `9be268f5e539c9bd`. Observamos a primeira leitura com sequência 1, fila 1 e perdas 0, seguida da leitura 2 com fila 2 e perdas 0. Confirmamos que as leituras pendentes da sessão anterior não permaneceram na fila.

Registramos as observações em `antes_reinicio.txt`, `apos_reinicio.txt` e `reinicio.png`. Confirmamos a limitação já documentada: mantemos a fila em RAM, portanto não preservamos pendências após reiniciar. Nossa resiliência nesta versão cobre interrupção da conectividade enquanto o dispositivo continua ligado.

## Restauração da configuração padrão

Removemos a definição temporária de capacidade 3 e restauramos o conteúdo original de `sketch.ino`. Executamos novamente e conferimos no Serial `capacidade=2000`, `tamanho_amostra=40` e `bytes_fila=80016`. Observamos dez leituras armazenadas offline sem perdas no registro `capacidade_restaurada.txt`.

Mantivemos a configuração pública original e não publicamos a variante de teste. Não alteramos a lógica do firmware nem as ligações do circuito nesta execução.

## Conferência reproduzível

Criamos `scripts/fase3/validar_cenarios_edge.py` para conferir os arquivos capturados. Executamos:

```sh
python scripts/fase3/validar_cenarios_edge.py
```

Obtivemos aprovação das verificações de fila cheia, ordem, perdas, pulso único, troca de sessão, reinício da fila e restauração da capacidade. Registramos o resultado estruturado em `validacao_cenarios.json`.

## Situação da primeira entrega

Concluímos a implementação e os testes técnicos previstos para a primeira entrega, incluindo os cenários ampliados. Ainda precisamos concluir nossa revisão final da entrega. Vamos implementar transmissão MQTT e confirmação do consumidor na etapa seguinte; nesta etapa, validamos exclusivamente a demonstração Serial local.
