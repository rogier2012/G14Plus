from assets.fastgraphs import graph
from assets.graphIO import loadgraph, writeDOT


def refine(g):
    V = g.V()

    alphalist = []
    initiallist = []
    resultlist = []
    for i in V:
        initiallist.append(i)
        i.colornum = 0

    resultlist.append(initiallist)
    while alphalist != resultlist:
        alphalist = resultlist
        resultlist = []
        for colorlist in alphalist:
            for k in range(len(colorlist) - 1):
                if not same_color(colorlist[k], colorlist[k+1]):
                    nolistfound = True
                    v = colorlist[k]
                    for i in resultlist:
                        if i != colorlist:
                            if same_color(i[0],v):
                                i.append(v)
                                v.colornum = resultlist.index(i)
                                nolistfound = False
                    if nolistfound:
                        newcolor = [v]
                        resultlist.append(newcolor)
                        v.colornum = resultlist.index(newcolor)

    return G


def same_color(u,v):
    return len(u.nbs()) == len(v.nbs()) and same_color_neighbour(u,v)
#put k in new color in result list with same properties or create a new list inside result list


def same_color_neighbour(u,v):
    S = set()
    T = set()
    for vertex in u.nbs():
        S.add(vertex.colornum)
    for vertex in v.nbs():
        T.add(vertex.colornum)
    return S == T

L = loadgraph("colorref_smallexample_4_7.grl",graphclass=graph,readlist=True)
G = L[0][0]
G = refine(G)
writeDOT(G, "examplegraph.dot")