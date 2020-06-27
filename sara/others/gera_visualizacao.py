# coding:utf8
import igraph
from random import randint
import sys
import uuid


def _plot(g, membership=None):
    if membership is not None:
        gcopy = g.copy()
        edges = []
        edges_colors = []
        for edge in g.es():
            if membership[edge.tuple[0]] != membership[edge.tuple[1]]:
                edges.append(edge)
                edges_colors.append("gray")
            else:
                edges_colors.append("black")
        gcopy.delete_edges(edges)
        layout = gcopy.layout("kk")
        g.es["color"] = edges_colors
    else:
        layout = g.layout("kk")
        g.es["color"] = "gray"
    visual_style = {}
    visual_style["vertex_label_dist"] = 0
    visual_style["vertex_shape"] = "circle"
    visual_style["edge_color"] = g.es["color"]
    visual_style["bbox"] = (4000, 2500)
    visual_style["vertex_size"] = 30
    visual_style["layout"] = layout
    # visual_style["bbox"] = (1024, 768)
    visual_style["margin"] = 40
    # visual_style["edge_label"] = g.es["label"]
    for vertex in g.vs():
        # Label do nó.
        # vertex["label"] = vertex.index
        vertex["label"] = vertex["label"]
    if membership is not None:
        colors = []
        for i in range(0, max(membership) + 1):
            colors.append('%06X' % randint(0, 0xFFFFFF))
        for vertex in g.vs():
            vertex["color"] = str('#') + colors[membership[vertex.index]]
        visual_style["vertex_color"] = g.vs["color"]
    igraph.plot(g, **visual_style).save(
        "comunidade_" + str(uuid.uuid4()) + ".png"
    )
    # igraph.save(g)


def plotagem(nome_grafo):
    pass


if __name__ == "__main__":
    # nome=sys.argv[1]
    # carrega o grafo..
    g = igraph.Graph.Read_GML("digrafo_incendiomuseu.gml")
    g.to_undirected()
    # print(g)
    # exit()
    cl = g.community_fastgreedy()
    # um recorte completo do grafo
    membership = cl.as_clustering().membership
    # separa as comunidades em subgrafos.
    subgrafos = cl.as_clustering().subgraphs()
    # tamanho minimo de vértices no grafo
    limiar = 1000
    # contador utilizado na geração dos nomes.
    print("Numero de comunidades", len(subgrafos))
    for i in subgrafos:
        if len(i.vs()) > limiar:
            print("Salvando a comunidade:", len(i.vs()))
            print(len(i.vs()))
            _plot(i)
# _plot(g,membership)
