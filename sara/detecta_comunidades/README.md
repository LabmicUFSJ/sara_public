# Overlap Detection
https://iopscience.iop.org/article/10.1088/1367-2630/11/3/033015

Versão 0.3 Carlos Magno

## Help Config

Padrão
> "sementes_predefinidas":false,
> "nome_arq_sementes":"sementes_karate",
> "tamanho_maximo_exibicao":20,
> "tamanho_maximo_nodes_plot":100
> "salvar_todas_comunidas":false


sementes_predefinidas: Caso o mesmo seja marcado como True( verdadeiro) é necessário configurar o nome_arq_semente que contém a ordem das sementes a serem utilizadas. O arquivo de sementes deve refletir os vértices da rede.
nome_arq_sementes: Contém o nome do arquivo de sementes a ser utilizado.
limiar_exibicao: Define o limiar maximo do número de comunidades encontradas a serem exibidas no terminal.
tamanho_maximo_nodes_plot: Tamanho máximo do número de vérices do grafo a ser plotado.
salvar_todas_comunidades: Caso marcado como True é salvo um arquivo de texto com todas as comunidades encontradas.

## Dependências

networkx
matplotlib
