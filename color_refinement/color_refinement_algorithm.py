from assets.fastgraphs import graph


def refine(g):
    V = g.V()

    for i in range(len(V)):
        g[i].colornum = 1


