# 🌐 Ir Além 1 — REST e e-mail simulado

Desenvolvemos um serviço HTTP local e um cliente Python que enviam e consultam leituras no formato já utilizado na Fase 3. Aplicamos regras didáticas e geramos mensagens `.eml` em uma caixa de saída local. Não utilizamos SMTP nem enviamos mensagens reais.

## 🎯 O que demonstramos

O cliente envia uma leitura por `POST /leituras`; o serviço valida o contrato, persiste a leitura e avalia os limites. Consultamos as últimas 100 leituras por `GET /leituras`, da mais recente para a mais antiga. `GET /saude` permite verificar se a API está disponível.

Reutilizamos os campos de telemetria sem alterar o firmware: `transport` continua identificando a origem do registro (`serial_demo` ou `mqtt`). A transferência desta cópia entre cliente e serviço ocorre por HTTP. O modo de demonstração produz dados sintéticos próprios, identificados por `device_id: cardioia-rest-demo` e uma nova sessão a cada execução; não afirmamos que são novas medições do Wokwi.

## ▶️ Como executar, do início ao fim

### Passo 1 — Preparar o computador e localizar o projeto

1. Se é a primeira execução, concluir os passos 1 a 4 da [preparação da Fase 3](../README.md#como-reproduzir--preparação). Ali explicamos instalação, PowerShell, download, pasta e criação de `.venv`.
2. Se já executou o painel, reutilizar a mesma cópia e o mesmo ambiente Python. Encerrar o painel antes de seguir para manter os terminais fáceis de identificar.
3. Abrir um PowerShell, entrar na pasta do projeto e chamar essa janela de **terminal A**.
4. Conferir:

```powershell
Test-Path .\README.md
.\.venv\Scripts\python.exe --version
```

- **Esperado:** `True` e Python `3.12.x`.
- **Se falhar:** voltar à preparação. Não iniciar a API com o Python de outro ambiente.
- **O que não precisa estar aberto:** Wokwi, Node-RED e consumidor MQTT. Esta demonstração gera suas próprias leituras fictícias.

### Passo 2 — Instalar as bibliotecas e iniciar a API

1. No terminal A, executar:

```powershell
.\.venv\Scripts\python.exe -m pip install -r config/fase3/requirements-mqtt.txt
```

2. Aguardar a instalação terminar sem erro. Se indicar que já está instalado, seguir normalmente.
3. Executar:

```powershell
.\.venv\Scripts\python.exe src/fase3/python/servico_rest.py
```

- **Esperado:** uma linha começando com `API local: http://127.0.0.1:8765`, seguida do local dos e-mails.
- **O terminal fica ocupado:** manter a janela aberta e não digitar outro comando nela agora.
- **Se a porta estiver ocupada:** encerrar a instância anterior do próprio serviço; não iniciar duas cópias na mesma porta. As opções ao final explicam como usar outra porta.

### Passo 3 — Verificar a resposta no navegador

1. Abrir [verificação do serviço](http://127.0.0.1:8765/saude).
2. Conferir a resposta `{"status": "ok", "simulated": true}`. Isso indica que a API está atendendo.
3. Abrir [consulta das leituras](http://127.0.0.1:8765/leituras).
4. Em uma primeira execução, esperar `{"readings": []}`: a lista está vazia porque ainda não enviamos dados. Se já houve testes, as leituras anteriores aparecem.

**Atenção ao endereço:** a raiz `http://127.0.0.1:8765/` retorna `{"error": "Rota inexistente"}`. Usar os links completos acima. Esta etapa apresenta texto JSON, não um painel com gráficos.

### Passo 4 — Abrir outro terminal e enviar as leituras

1. Deixar o terminal A rodando.
2. Abrir outro PowerShell, que chamaremos de **terminal B**.
3. No Explorador de Arquivos, abrir a pasta do projeto e copiar seu caminho da barra de endereços.
4. No terminal B, digitar `Set-Location -LiteralPath`, seguido do caminho copiado entre aspas. Por exemplo, se seguiu a pasta sugerida:

```powershell
Set-Location -LiteralPath 'C:\projetos\fiap-ano02-fase03-cardioia'
```

5. Confirmar `Test-Path .\README.md`: deve retornar `True`.
6. Executar a demonstração **uma vez**:

```powershell
.\.venv\Scripts\python.exe src/fase3/python/cliente_rest.py --demonstrar --saida .tools/runtime/fase3/rest/resultado_demonstracao.json
```

- **Esperado:** texto JSON longo com `sent`, `repeated` e `received`; o terminal B volta a aceitar comandos.
- **O que aconteceu:** enviamos cinco leituras, repetimos a última para testar duplicação e consultamos os dados pela API.
- **Se aparecer API indisponível:** conferir se o terminal A continua aberto e se `/saude` responde; não repetir instalações sem analisar o erro.
- **Não copiar as chaves/valores como comandos:** o JSON é o resultado para leitura.

### Passo 5 — Interpretar o resultado

1. Localizar `session_id` e guardar o valor: identifica esta execução. Ele será diferente do exemplo do grupo.
2. No campo `sent`, conferir a leitura `sequence: 1`: 72 BPM, 24 °C e `email_id: null` (nenhum e-mail).
3. Conferir a leitura 2: 132 BPM e 31 °C, com número em `email_id`.
4. Conferir a leitura 3: 144 BPM e 32 °C, mas `email_id: null`. O mesmo alerta continua ativo, sem nova mensagem.
5. Conferir a leitura 4: 72 BPM e 24 °C, com `active_episodes: []`. Os alertas foram encerrados.
6. Conferir a leitura 5: 132 BPM e 31 °C, com outro número em `email_id`, pois começou um novo episódio.
7. No campo `repeated`, conferir `duplicate: true`: o reenvio não criou outra leitura nem outro e-mail.
8. No campo `received`, conferir cinco leituras da sessão, da sequência 5 até a 1.

**Não comparar números fixos de e-mail:** na primeira execução normalmente são 1 e 2; depois continuam aumentando. Cada nova demonstração gera outra sessão e dois novos arquivos, preservando os anteriores.

### Passo 6 — Consultar sem enviar novos dados

1. No terminal B, executar:

```powershell
.\.venv\Scripts\python.exe src/fase3/python/cliente_rest.py --consultar
```

2. Conferir as mesmas leituras. Esta consulta retorna até 100 registros e pode incluir sessões anteriores.
3. Atualizar a página `/leituras` no navegador para visualizar o mesmo histórico em JSON.

**Esperado:** nenhuma nova leitura ou mensagem criada apenas por consultar.

### Passo 7 — Abrir os e-mails simulados

1. No terminal B, abrir a pasta com:

```powershell
explorer.exe "$PWD\.tools\runtime\fase3\rest\emails"
```

2. Localizar os arquivos `alerta-NNNN.eml` correspondentes aos números `email_id` das leituras 2 e 5.
3. Abrir com duplo clique. Se o Windows não tiver um leitor de e-mail, usar **Abrir com → Bloco de Notas**. Se necessário, abrir o Bloco de Notas, escolher Arquivo → Abrir e selecionar “Todos os arquivos”.
4. Conferir assunto `[SIMULACAO]`, sessão, número da leitura, 132 BPM artificiais, temperatura **ambiente** de 31 °C e os dois motivos de alerta.
5. Se o texto bruto mostrar sequências como `=C3`, isso pode ser a codificação do arquivo de e-mail. Um leitor de e-mail apresenta o texto decodificado; não indica falha de geração.

**Esperado:** dois novos arquivos nesta demonstração. Nenhuma mensagem é enviada pela internet; remetente e destinatário `example.invalid` são fictícios.

### Passo 8 — Reiniciar e confirmar que os dados ficaram salvos

1. No terminal A, pressionar **Ctrl+C** e esperar o prompt retornar.
2. No mesmo terminal A, iniciar novamente:

```powershell
.\.venv\Scripts\python.exe src/fase3/python/servico_rest.py
```

3. No terminal B, executar **somente a consulta**:

```powershell
.\.venv\Scripts\python.exe src/fase3/python/cliente_rest.py --consultar
```

4. Comparar a sessão guardada no passo 5: as cinco leituras e suas referências aos e-mails devem permanecer.
5. Conferir que a pasta mantém os mesmos arquivos, sem novos e-mails pela consulta.

**Não executar `--demonstrar` neste passo:** isso criaria outra sessão e atrapalharia a comparação.

### Passo 9 — Encerrar e guardar a conferência

1. No terminal A, pressionar Ctrl+C. Agora é possível fechar os dois PowerShell.
2. Preservar `.tools/runtime/fase3/rest/`: contém banco, e-mails e o resultado JSON salvo no passo 4. Não apagar essa pasta para “limpar” o teste.
3. Marcar como concluído somente o que foi observado: cinco leituras, dois e-mails, reenvio reconhecido e persistência após reinício.
4. Se alguma etapa falhar, registrar o número do passo, comando, saída e resultado esperado para revisão. Os arquivos locais não são enviados automaticamente ao GitHub.

No Linux/macOS, utilizar a preparação específica do [guia principal](../README.md), substituir o executável por `.venv/bin/python` e abrir a pasta de e-mails pelo gerenciador de arquivos do sistema.

### Opções de execução

Para enviar manualmente o exemplo, usar no terminal do cliente:

```powershell
.\.venv\Scripts\python.exe src/fase3/python/cliente_rest.py --enviar config/fase3/contratos/exemplo_telemetria.json
```

Esse comando acrescenta a sessão do exemplo ao histórico; a demonstração de cinco leituras é filtrada por sua própria sessão. Se a porta 8765 estiver ocupada, encerrar o próprio serviço anterior ou iniciar uma instância alternativa no **primeiro terminal**:

```powershell
.\.venv\Scripts\python.exe src/fase3/python/servico_rest.py --porta 8766 --dados .tools/runtime/fase3/rest-alternativo
```

No **segundo terminal**, usar o endereço correspondente:

```powershell
.\.venv\Scripts\python.exe src/fase3/python/cliente_rest.py --url http://127.0.0.1:8766 --consultar
```

Nessa pasta alternativa, a consulta inicialmente retorna uma lista vazia. Para gerar dados, executar o cliente com `--demonstrar` e o mesmo `--url`. Não executar a consulta no terminal ocupado pelo servidor.

## 🧠 Regras e limites

Geramos alerta quando os pulsos artificiais ultrapassam **120 BPM** ou a temperatura **ambiente** ultrapassa **30 °C**. Encerramos cada episódio ao retornar a até **108 BPM** ou **28 °C**, respectivamente. Um novo motivo gera uma mensagem; permanecer no mesmo episódio não gera outra. Neste cliente avaliamos uma leitura elegível, enquanto o painel Node-RED exige duas leituras consecutivas. Essa escolha torna explícito o fluxo de automação do desafio.

Leituras marcadas como recuperadas, com idade no envio superior a dez segundos ou fila maior que uma posição ficam registradas sem acionar ou encerrar episódios. Sensor inválido não encerra um alerta de temperatura. Zero pulsos representa ausência de acionamentos do botão, sem interpretação clínica. Os exemplos de risco do enunciado não nos autorizam a chamar temperatura ambiente de febre.

A API recebe cópias fornecidas pelo cliente, sem assinatura de horário de coleta real; sua avaliação é uma demonstração sobre os metadados informados, não um monitor clínico do presente. Não existe encaminhamento automático MQTT → REST nesta etapa. Não cruzamos esses dados com pacientes das fases anteriores.

Persistimos leituras, episódios e conteúdo das mensagens em SQLite antes de exportar `.eml`. Ao reiniciar, reconstruímos arquivos ausentes e preservamos a supressão de duplicatas. Exigimos sequência crescente por dispositivo/sessão e rejeitamos identidade repetida com conteúdo diferente. O serviço é local, de uma requisição por vez, sem autenticação ou TLS; não se destina à publicação na internet. A retenção em disco não é limitada nesta demonstração.

## 🧪 Testes e situação

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s src/fase3/tests -p test_rest.py -v
```

Conferimos sete testes em 26/10/2026, com HTTP local real: envio e consulta, normalização e novo episódio, duplicatas, conflitos, dados inválidos, leituras históricas, sensor inválido, persistência após reinício, reconstrução de e-mail e falhas HTTP/conexão. Preservamos a [saída da demonstração](../../other/fase3/evidencias/2026-10-26/rest/resultado_demonstracao.json).

Concluímos a implementação, os testes locais e a [validação guiada](../../other/fase3/evidencias/2026-10-26/rest/validacao_guiada/RESULTADOS.md), incluindo consulta após reinício. Produzimos o [relatório de duas páginas](../CardioIA_Fase3_Relatorio_REST_Email.pdf), com revisão final do grupo pendente. O desafio de comparação de modelos permanece na próxima etapa do [roteiro](../ROTEIRO_ENTREGA.md).
