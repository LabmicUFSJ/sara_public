###  Coletando Tweets.

Ative o ambiente virtual e digite:

``` shell
(saraEnv)$: python sara_coletor.py <termo_a_ser_coletado> <limite_coleta> <colecao> <banco>
```

- termo_a_ser_coletado : Refente a hastag ou termo a ser monitorado.
- limite_coleta: referente ao número de tweets a ser coletado, para não estabelecer um limite digite 0
- colecao: A coleção onde os dados serão salvos no banco de dados.
- banco: O nome do banco onde os dados serão salvos.

### Gerando Núvem de palavras dos Tweets coletados(Conteúdo)

``` shell
(saraEnv)$: python sara_conteudo.py <banco> <colecao>
```

Caso ocorra algun erro , verifique se você executou o processo de pós-instalação.

No final do processo será gerada uma nuvem de palavras.

### Gerando Rede de Retweets(Estrutural)

``` shell
(saraEnv)$: python saraEstrutural.py <nome_rede> <nome_base> <nome_colecao> <True||False> <limite>
```
- nome_rede: Nome a ser utilizado para salvar a rede gerada.
- nome_base: Nome do banco de dados onde os tweets baixados estão presente.
- nome_colecao: Nome da coleção onde estão os dados.
- True ou False: Se true gera uma rede direcionada.
- limite: Número de tweets utilizados para geração da rede, para usar todos defina como 0.

A rede gerada sera salva na pasta redes, a ser gerada após a execução.
### Centralidade (Importância)

Para realização desta etapa é necessário que se tenha um grafo gerado.

Nesta etapa é gerada uma lista de nós ordernada por importância quanto a centralidade, que pode ser utilizada na detecção de comunidades.

``` shell
(saraEnv)$: python sara_centralidade.py <banco> <colecao> <grafo>
```

Entrada: grafo.gml

saída: Um ranking gravado na pasta resultados_importancia

### Sara Sentimento(Leia)

``` shell
(saraEnv)$: python sara_sentimento.py <banco> <colecao>
```

Nesta etapa é gerada um gráfico simples da análise de sentimento.
