# Guia de execução de scripts

Este guia apresenta o modo de excecução dos scripts que acompanham o framework.
Novos scripts podem ser criados utilizando o framework.

###  Coletando Tweets.

Ative o ambiente virtual e digite:

``` shell
(saraEnv)$: python sara_stream.py <termo_a_ser_coletado> <limite_coleta> <colecao> <banco>
```

- termo_a_ser_coletado : Refente a hastag ou termo a ser monitorado.
- limite_coleta: referente ao número de tweets a ser coletado, para não estabelecer um limite digite 0
- colecao: A coleção onde os dados serão salvos no banco de dados.
- banco: O nome do banco onde os dados serão salvos.


### Gerando Rede (Estrutural)

``` shell
(saraEnv)$: python sara_network.py <nome_rede> <nome_colecao> <database> <True|False> <limite> <r|m>
```
- nome_rede: Nome a ser utilizado para salvar a rede gerada.
- nome_base: Nome do banco de dados onde os tweets baixados estão presente.
- nome_colecao: Nome da coleção onde estão os dados.
- True ou False: Se true gera uma rede direcionada.
- limite: Número de tweets utilizados para geração da rede, para usar todos defina como 0.
- r|m : r - Gera rede utilizando retweets, m - Gera a rede utilizando menções (@)

A rede gerada sera salva na pasta redes, a ser gerada após a execução.

### Gerando Rede com Peso nas Arestas (Estrutural)

``` shell
(saraEnv)$: python sara_network_weighted.py <nome_rede> <nome_colecao> <nome_base> <True|False> <limite> <r|m>
```
- nome_rede: Nome a ser utilizado para salvar a rede gerada.
- nome_base: Nome do banco de dados onde os tweets baixados estão presente.
- nome_colecao: Nome da coleção onde estão os dados.
- True ou False: Se true gera uma rede direcionada.
- limite: Número de tweets utilizados para geração da rede, para usar todos defina como 0.
- r|m : r - Gera rede utilizando retweets, m - Gera a rede utilizando menções (@)

A rede gerada sera salva na pasta redes, a ser gerada após a execução.

### Centralidade (Importância)

Para realização desta etapa é necessário que se tenha um grafo gerado.

Nesta etapa é gerada uma lista de nós ordernada por importância quanto a centralidade, que pode ser utilizada na detecção de comunidades.

``` shell
(saraEnv)$: python sara_centrality.py <grafo>
```

Entrada: grafo.gml

saída: Um ranking gravado na pasta resultados_importancia

### Gerando Núvem de palavras dos Tweets coletados (Conteúdo)

``` shell
(saraEnv)$: python sara_content.py <banco> <colecao>
```

Caso ocorra algun erro, verifique se você executou o processo de pós-instalação.

No final do processo será gerada uma nuvem de palavras.

### Detecção de bots

A detecção de contas automatizada (BOTS) é realizada por meio do SaraBotTagger.
Em um console, com o ambiente virtual instalado execute:

``` console
python sarabottagger.py <collection> <database> <number_of_users>
```

- database: A base de dados a ser utilizada.
- collection: A coleção a ser utilizada.
- number_of_users: O número de usuários a ser avaliado, caso não seja definido
como 0, a base inteira é avaliada.
