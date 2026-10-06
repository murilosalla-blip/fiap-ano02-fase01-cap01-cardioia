# ECGs derivados para a revisão ampliada

Esta pasta contém somente imagens derivadas da versão 2 da base pública
**ECG Images dataset of Cardiac Patients**, DOI `10.17632/gwbz3fsgp8.2`.
Os arquivos originais não são versionados aqui.

As 491 imagens são recuperadas e geradas localmente pelo script para evitar
versionar a base médica inteira. `exemplos/` mantém uma miniatura sanitizada de
cada classe para inspeção direta no GitHub; o inventário completo permite
reproduzir e auditar o conjunto usado no treinamento.

O script `fase2/src/preparar_visual_ampliado.py`:

- valida o SHA-256 informado pela fonte;
- elimina cópias exatas antes do experimento;
- remove o cabeçalho administrativo e o rodapé com data/hora;
- converte o traçado para tons de cinza;
- preserva a proporção em uma tela de 384 × 224 pixels;
- grava nomes formados apenas pelo hash do conteúdo original.

O inventário auditável está em
`fase2/auditoria/inventario_visual_ampliado.json`. A fonte não oferece uma chave
confiável de paciente: hashes impedem repetição exata de arquivos, mas não
garantem que dois exames diferentes pertençam a indivíduos distintos.

As classes originais são mantidas em subpastas e transformadas em alvo binário
apenas durante o treinamento: `normal` = 0; todas as demais = 1. A distribuição
da amostra é experimental e não representa prevalência clínica.
