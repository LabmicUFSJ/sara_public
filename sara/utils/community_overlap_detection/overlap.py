# -*- coding: utf-8 -*-
#!/usr/bin/env python3

"""

Refatoração do código de detecção de comunidades em sobreposicao

Detecção de comunidade com sobreposição.
Utilizando abordagem do Santo Furtunato.
v 0.3
Carlos Magno
UFSJ
Licença MIT

Para executar digite python3 dcs.py <nome_rede> <flag>
Atualmente suporta redes no formato gml, edgelist
"""

import json
import os
import re
import secrets
import sys

import matplotlib.pyplot as plt
import networkx as nx


class OverlapCommunity(object):
    """docstring for detect community in overlap."""

    def __init__(self):
        self.comunidade_negativa = []
        self.presentes = []
        self.nome_rede = ""
        self.alfa = 1
        self.sementes_predefinidas = []
        self.cont_semente = 0
        # predefinida hardcode
        self.predefinida = False
        self.recalculo = False
        self.nome_arq_sementes = ""
        # limiar harcode
        self.limiar = 10
        self.limiar_max_plot = 10
        self.carrega_config()

        self.path_comunidades = "comunidades/"

    def get_key(self, item):
        """return a key from item."""
        return item[0]

    def carrega_config(self):
        """carrega o arquivo de configuracao"""
        try:
            file = open("config.json", "r")
            dados_json = json.load(file)
            self.nome_arq_sementes = dados_json['nome_arq_sementes']
            self.limiar = dados_json['tamanho_maximo_exibicao']
            self.predefinida = dados_json['sementes_predefinidas']
            self.limiar_max_plot = dados_json['tamanho_maximo_nodes_plot']
            self.salvar_tudo = dados_json['salvar_todas_comunidades']
            file.close()
        except Exception as e:
            print("erro", e)
            print("erro ao carregar o config, usando configurações padrao")

    def carrega_sementes(self):
        """carrega as sementes para uma lista"""
        arq = open(self.nome_arq_sementes, "r")
        for i in arq:
            self.sementes_predefinidas.append(i.split('\n')[0])
        # print(self.sementes_predefinidas)

    def escolha_semente(self):
        """Escolhe a semente de uma lista predefinida"""
        semente = self.sementes_predefinidas[self.cont_semente]
        self.cont_semente += 1
        return semente

    def formata_saida(self, listas, compartilhados):
        """
        Formata a lista para plotagem.
        format the output
        """
        cor = 0
        comunidades = {}
        for i in listas:
            for elemento in i:
                if elemento in compartilhados:
                    comunidades[elemento] = -1
                else:
                    comunidades[elemento] = cor
            cor += 1
        return comunidades

    def detecta_compartilhados(self, lista):
        """
        Find nodes shared in the communities.
        Encontra os nós que estão presente em mais de uma comunidade.
        """
        j = 1
        compartilhados = []
        for i in lista:
            for j in lista:
                if i is not j:
                    # print(i,j)
                    comp = set(i).intersection(set(j))
                    if len(comp) > 0 and comp not in compartilhados:
                        compartilhados.append(comp)
        l_compartilhados = []
        for i in compartilhados:
            for j in list(i):
                if j not in l_compartilhados:
                    l_compartilhados.append(j)
        return l_compartilhados

    def fitness_no(self, no, modulo, grafo):
        """Realiza o calculo do fitness do no"""
        if no in modulo:
            # o no já esta no modulo.
            return 0
        # fitness do no
        sem_no = modulo
        com_no = modulo + [no]
        # print("Sem o Nó")

        fitness_sem_no = self.calcula_fitness_v2(sem_no, grafo)
        # print("-----\nCom o Nó")
        fitness_com_no = self.calcula_fitness_v2(com_no, grafo)
        # print("-------\n")
        return fitness_com_no - fitness_sem_no

    def calcula_fitness_v2(self, modulo, grafo):
        """V2 do calculo de fitness"""
        sub_grafo = grafo.subgraph(modulo)
        k_interno = sub_grafo.number_of_edges()
        # print("\nV2 K interno",k_interno)
        # print(modulo)
        k_externo = 0
        for i in modulo:
            diferenca = set(grafo.adj[i]).difference(set(modulo))
            k_externo += len(diferenca)
        # print("V2 K-externo",k_externo)
        try:
            return k_interno / (pow(k_externo + k_interno, self.alfa))
        except Exception as e:
            return k_interno / (pow(k_externo + k_interno, self.alfa))

    def calcula_fitness(self, modulo, grafo):
        """
        This function calculates the fitness value.
        Calcula o fitness de um conjunto de nós.
        """
        # print(modulo,no)
        # considerando o grau como nao direcionado,
        # portanto entrada e saida são iguais.
        grau = 0
        # modulo=[17,6,7]
        # print("Modulo",modulo)
        dicio_interno = {}
        k_interno = 0
        K_externo = 0
        if len(modulo) > 1:
            # calcula o k_interno
            for j in range(0, len(modulo)):
                # print("p",modulo[j])
                for k in range(j + 1, len(modulo)):
                    # print("p2",modulo[j],modulo[k])
                    k_interno += grafo.number_of_edges(modulo[j], modulo[k])
            # print("K_interno",k_interno)

            for i in modulo:
                diferenca = set(grafo.adj[i]).difference(set(modulo))
                K_externo += len(diferenca)
            # print("V1 K interno", k_interno)
            # print("V1K externo",K_externo)
            return k_interno / (pow(K_externo + k_interno, self.alfa))
        else:
            # print("V1 K interno", k_interno)
            # print("V1K externo",K_externo)
            return 0.00

    def recalculo(self, comunidade, grafo):
        """
        verify if a node have negative weightself.
        Realiza o recalculo dos pesos verificando se algum nó possui
        peso negativo.
        """
        # print("Recalculo...")
        # realiza uma copia da lista
        comunidade_aux = comunidade.copy()
        for i in comunidade:
            # print("Removendo",i)
            # print("comunidade_aux antes",comunidade_aux)
            comunidade_aux.remove(i)
            fit = self.fitness_no(i, comunidade_aux, grafo)
            if fit < 0:
                # IV fitness have a negative value.
                # fit negativo, sem o nó com peso negativo
                # print("Negativo",fit,i,comunidade_aux)
                self.comunidade_negativa.append(i)
                print("RECALCULO")
                self.recalculo(comunidade_aux, grafo)
            # print("comunidade_aux depois",comunidade_aux,"Fit",fit)
            # restaura o estado da comunidade
            comunidade_aux = comunidade.copy()
        # print("COM",comunidade,"I",comunidade_aux)
        return comunidade
        # fitness_no(v,comunidade,grafo)

    def aux_detecta_comunidade(self, v, comunidade, grafo, maior):
        """
        This function auxility find communities
        Auxilia na detecção de comunidades.
        """
        # print("C",comunidade+[v])
        escolha = None
        adicionado = False
        if v not in comunidade:
            fit = self.fitness_no(v, comunidade, grafo)

            # print("No",v,"Fit",fit)
            if fit > maior and fit > 0:
                maior = fit
                escolha = v
            else:
                if fit < 0:
                    pass
                    # print("Menor que 0",fit)
        if escolha is not None:
            comunidade.append(escolha)
            self.presentes.append(escolha)
            adicionado = True
        # print("adicionado",adicionado,"Len comunidade",len(comunidade))
        return comunidade, adicionado

    def vizinhos_modulo(self, comunidade, grafo):
        """
        This function find the neighbors of module.
        Encontra os vizinhos do modulo.
        """
        vizinhos = []
        for i in comunidade:
            v_aux = grafo.neighbors(i)
            # print("V-aux",list(v_aux))
            for j in v_aux:
                if j not in vizinhos:
                    vizinhos.append(j)
        resultado = set(vizinhos) - set(comunidade)
        # print("SET",sorted(resultado))
        return sorted(resultado)

    def detecta_comunidade_natural(self, grafo, semente, comunidade):
        """
        Detecta a comunidade natural
        Find natural community.
        """
        maior = -999
        flag = True
        # comunidade = []
        if semente not in comunidade:
            comunidade.append(semente)
        # print("detectando comunidade natural da semente", semente)
        # repete para mapear todos os vizinhos, para quando não for possivel
        # realizar nenhuma nova adicao.
        while flag is True:
            vizinhos = self.vizinhos_modulo(comunidade, grafo)
            # cont=0
            for v in vizinhos:
                # print(cont,len(vizinhos))
                comunidade, flag = self.aux_detecta_comunidade(
                    v, comunidade, grafo, maior
                )
                if self.recalculo:
                    # recalcula o fitness na comunidades
                    comunidade = self.recalculo(comunidade, grafo)
                maior = -999
                # cont+=1
            if len(comunidade) == len(grafo.nodes()):
                break
        # recalculo do fitness
        # print("Comunidade",comunidade)
        return comunidade

    def entrada_dados(self):
        """
        This function read the parameters of input.
        Lê os parametros de entrada.
        """
        try:
            self.name_file = sys.argv[0]
            self.nome_rede = sys.argv[1]
            self.alfa = sys.argv[2]

            # self.lista_sementes=sys.argv[3]
            self.alfa = float(self.alfa)
        except Exception as e:
            print(
                "--HELP--\nError: Faltando parâmetros"
                "\nPara executar digite:\n python3 ",
                self.name_file,
                " <nome_rede> <alfa>\nOs formatos suportados são edgelist e GML",
            )
            print(f"Exception {e}")
            sys.exit()

        extensao = self.nome_rede.split(".")[1]
        if "edgelist" in extensao:
            grafo = nx.read_edgelist(self.nome_rede)
        elif "gml" in extensao:
            # tenta ler sem o id preservando as labels.
            try:
                grafo = nx.read_gml(self.nome_rede)
            except Exception as e:
                grafo = nx.read_gml(self.nome_rede, label="id")
            # converte os labels para string
        else:
            print("Formato inválido.")
            exit(-1)
        mapa = {}
        for i in grafo:
            mapa[i] = str(i)
        grafo = nx.relabel_nodes(grafo, mapa)
        print("Grafo sendo convertido para Unidirecional")
        grafo = grafo.to_undirected(grafo)
        return grafo

    def salvar_compartilhados(self, lista):
        """Salva comunidades compartilhadas"""
        arq = open(
            "elementos_compartilhados_"
            + self.nome_arq_sementes
            + "_"
            + self.nome_rede.split(".")[0]
            + ".txt",
            'w',
        )
        arq.write(str(lista) + ";")
        print("elementos compartilhados salvos!!")
        arq.close()

    def salvar_all_comunidades(self, lista):
        """Salva todas as comunidades"""
        try:
            arq = open(
                self.path_comunidades
                + "todas_comunidades_"
                + self.nome_arq_sementes
                + "_"
                + self.nome_rede.split(".")[0]
                + ".txt",
                'w',
            )
            for i in lista:
                arq.write(str(i) + ";")
                print("Todas comunidades foram  salvas!!")
            arq.close()
        except Exception as e:
            os.mkdir(self.path_comunidades)
            self.salvar_all_comunidades(lista)

    def main(self, grafo):
        """The main function."""
        # modulo se refere aos elementos na comunidade.
        modulo = []
        # se refere ao g'
        # se refere ao g''
        modulo2 = []
        comunidades = []

        print(nx.info(grafo), "alfa", self.alfa)

        nos = grafo.nodes()

        # escolha do nó
        # semente = secrets.choice(list(nos))
        if self.predefinida:
            semente = self.escolha_semente()
        else:
            print("Fora")
            semente = secrets.choice(list(nos))
        # print("Nó Escolhido semente", semente)
        # nós escolhidos, já utilizados como semente.
        escolhido = []
        # nós restantes, apos marcar como utilizado.
        possiveis = []
        # #forcando a semente

        comunidades = []

        # repete até todos os nós forem verificados.
        while len(escolhido) < len(nos):
            # comunidade natural
            # print("escolhido",len(escolhido),"Len nos",len(nos))
            if semente not in self.presentes:
                escolhido.append(semente)
                comunidade = self.detecta_comunidade_natural(
                    grafo, semente, [semente]
                )
                # print(comunidade)
                # exit()
                # print("COM Natural",comunidade)
                if comunidade not in comunidades:
                    comunidades.append(comunidade)
                else:
                    print("JA Adicionado")
                possiveis = nos - escolhido
                possiveis = possiveis - set(self.presentes)
                if len(possiveis) < 1:
                    break
                    # predefinida is true
                if self.predefinida:
                    semente = self.escolha_semente()
                else:
                    semente = secrets.choice(list(possiveis))
                    # print("getout semente")
                    # exit()

                # print("Nó Escolhido semente", semente)
            else:
                semente = self.escolha_semente()
                # print("out")
        print("N comunidades", len(comunidades), "N sementes", len(escolhido))
        if self.salvar_tudo:
            self.salvar_all_comunidades(comunidades)
        if len(comunidades) <= self.limiar:
            print("---Exibindo comunidades---\n")
            print("Número de comunidades menor ou igual", self.limiar)
            for i in comunidades:
                print("Tamanho comunidade", len(i))
                print(i)
                print("----------\n")
        compartilhados = self.detecta_compartilhados(comunidades)
        print("\n----------\nElementos compartilhados", compartilhados)
        print("Numero de elementos compartilhados", len(compartilhados))

        # --------------------------------------------------

        bigger = []
        for i in comunidades:
            bigger.append([len(i), i])
        bigger_ordenado = sorted(bigger, key=self.get_key, reverse=True)
        top = 10
        print("---\n As maiores comunidades foram salvas como subgrafos\n")
        print("TOP", top)
        try:
            arq = open(self.path_comunidades + "sumario_comunidades", "w")
        except Exception as e:
            os.mkdir(self.path_comunidades)
            arq = open(self.path_comunidades + "sumario_comunidades", "w")
        arq.write("TOP 10\n")
        for i in bigger_ordenado:
            print("___________")
            print("Tamanho", i[0], "Primeiros elementos", i[1][:3])
            arq.write(
                "Tamanho "
                + str(i[0])
                + "Primeiros nós "
                + str(i[1][:10])
                + "\n"
            )
            print(nx.info(grafo.subgraph(i[1])))
            sub_grafo = grafo.subgraph(i[1])
            nome_rede = (
                self.path_comunidades
                + "grafo_"
                + str(len(grafo))
                + "_"
                + str(top)
                + ".gml"
            )
            nx.write_gml(sub_grafo, nome_rede)
            print("rede", nome_rede, "Salva em:", self.path_comunidades)
            print("___________")
            if top == 1:
                break
            top -= 1
        arq.close()
        if len(grafo.nodes) < self.limiar_max_plot:
            comunidades_f = self.formata_saida(comunidades, compartilhados)
            cores = []
            for i in range(0, len(comunidades)):
                cores.append(i)
            # print("N cores", len(cores))
            #
            values = [comunidades_f.get(node) for node in grafo.nodes()]
            # #
            nx.draw_spring(
                grafo,
                cmap=plt.get_cmap('jet'),
                node_color=values,
                font_size=12,
                font_color='r',
                node_size=700,
                with_labels=False,
                label="cores",
                k=0.15,
            )
            plt.legend()
            plt.show()


if __name__ == '__main__':
    communities = OverlapCommunity()
    grafo = communities.entrada_dados()
    if communities.predefinida:
        communities.carrega_sementes()
        # print(communities.sementes_predefinidas)
    communities.main(grafo)
