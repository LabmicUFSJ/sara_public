# Guia Agendamento de Coleta

A Sara suporta coleta agendadas. Para tal somente é necessário executar o
`scripts/sara_scheduled_stream.py` como apresentado a seguir:

> Lembre-se que o ambiente virtual deve estar ativo e o SARA instalado.

``` console
(ENV) python sara_scheduled_stream.py <termo> <colecao> <banco_de_dados>

```

Após esta etapa será solicitado que você informe a duração da coleta e o intervalo
entre as coletas.

Por exemplo:

``` console
Duração da coleta: 10
Intervalo entre coletas: 30
```

Portanto, no exemplo apresentado as coletas irão ocorrer por 10 minutos a cada 30 minutos.
