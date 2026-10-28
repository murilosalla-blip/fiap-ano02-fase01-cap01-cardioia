# Revisão técnica e conferência do pacote — 28/10/2026

Concluímos a revisão técnica dos quatro relatórios: conteúdo, passos de execução, integrantes/RMs, links, paginação e apresentação visual. Mantemos duas páginas em Edge, quatro em MQTT/dashboard, duas em REST/e-mail e duas na comparação tradicional/LIF. Relemos as dez páginas renderizadas e confrontamos parâmetros e resultados com código e evidências. Atualizamos a identificação da revisão técnica para 28/10, preservando as datas dos ensaios originais.

Conferimos Murilo Salla (RM568041), Elias da Silva de Souza (RM568500) e Julia Duarte de Carvalho (RM567816) no README e nos quatro relatórios. Essa revisão não comprova o cadastro efetivo de todos na plataforma da FIAP, que precisa ser verificado no fechamento.

## Requisitos e reprodução

Conferimos os firmwares C++ comentados, os dois diagramas Wokwi, o export Node-RED, o consumidor com ACK após persistência, os contratos, cliente/serviço REST, notebook comentado e executado, código LIF e resultados. Preservamos as fases anteriores e seus links. A comparação usa os mesmos 48 casos de teste: 44 acertos no tradicional e 35 no LIF; os rótulos são regimes sintéticos, sem diagnóstico.

Aprovamos 23 testes Python de contratos/MQTT/REST, 19 do painel e nove do Ir Além 2: seis dos modelos e três de exportação. Executamos o notebook inteiro e conferimos links tanto no HTML quanto na cópia `.ipynb`, mantendo código e saídas da origem preservados. Os resultados da CI devem ser consultados no PR desta revisão e no GitHub Actions, incluindo o novo job do notebook. Os resultados de teste registrados neste parágrafo são locais.

Os verificadores confirmaram os 372 destinos do mapa, 286 conteúdos protegidos e os 223 itens históricos: 212 presentes e 11 aulas recuperáveis por Git. Não removemos dados, código ou documentos das Fases 1 e 2.

## Acesso aos materiais públicos

Sem enviar credenciais, conferimos os dois Wokwi, as três pastas de dados da Fase 1 no Drive, os três repositórios, o repositório/portal da Julia e o vídeo da Fase 2. As consultas retornaram HTTP 200, títulos compatíveis e nenhum redirecionamento para login. Essa conferência de acesso não representa nova execução integral de cada aplicação ou reprodução completa do vídeo antigo.

O Streamlit inicialmente apresentou redirecionamento na consulta automática. No navegador, identificamos repouso por inatividade, acionamos a reativação e conferimos a página inicial CardioIA com suas abas, sem login. Duas tentativas de captura de tela excederam o tempo limite; registramos a conferência textual da página sem alegar uma captura disponível. Se a publicação voltar a repousar, utilizar o botão de reativação ou a execução local descrita no guia da Fase 2.

O endereço antigo do repositório continua preservado e redireciona ao nome atual. A origem, os resultados e os hashes dos quatro PDFs estão no arquivo `conferencia_entrega.json` desta pasta.

## Fechamento ainda necessário

- Gravar o vídeo próprio do Ir Além 2 com até quatro minutos, publicar como não listado no YouTube e inserir/conferir o link no README raiz. O roteiro e o vídeo da Fase 2 não substituem essa gravação.
- Conferir os integrantes no cadastro efetivo do grupo e os formatos/tamanhos aceitos pela plataforma FIAP.
- Preparar o arquivo de submissão conforme essas regras, enviar até o prazo registrado de 04/11/2026 às 23h59 e conferir o conteúdo baixado após o envio.

A revisão técnica e a publicação no GitHub não representam envio na FIAP. O pacote disponível no repositório ainda depende do vídeo para concluir todo o escopo dos dois desafios escolhido pelo grupo. Não atribuímos nota antecipada.
