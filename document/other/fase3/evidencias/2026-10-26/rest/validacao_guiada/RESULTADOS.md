# Validação guiada do Ir Além 1 - 26/10/2026

Executamos o cliente contra o serviço HTTP local e consultamos cinco leituras da sessão `9ed8af36461d489c`. Preservamos a saída original em [resultado_demonstracao.json](resultado_demonstracao.json).

- Confirmamos os e-mails das leituras 2 e 5: [primeiro alerta](alerta-0001.eml) e [segundo alerta](alerta-0002.eml).
- Conferimos a permanência do episódio na leitura 3 sem novo e-mail e o encerramento na leitura 4.
- Repetimos a leitura 5 e recebemos `duplicate: true`, com o mesmo identificador de e-mail 2.
- Encerramos e reiniciamos o serviço. Na consulta apresentada durante a validação guiada, as cinco leituras permaneceram na ordem 5 a 1, com os horários originais e referências aos e-mails 1 e 2. Essa observação provém da saída de terminal compartilhada na validação; o JSON anexado acima corresponde à demonstração inicial.
- Inspecionamos os dois arquivos: endereços fictícios, assunto de simulação, sessão correta, 132 BPM artificiais e temperatura ambiente de 31 °C.

Não enviamos e-mail externo. Os valores foram gerados pelo cenário sintético do cliente, sem novas coletas do Wokwi. A raiz `/` retorna rota inexistente; utilizamos `/saude` e `/leituras` no navegador.

Concluímos a validação guiada funcional. Produzimos o relatório de duas páginas, ainda sujeito à revisão final do grupo; não registramos publicação ou submissão como concluídas.
