from assets.fastgraphs import graph
from assets.graphIO import loadgraph, writeDOT


def refine(G):
    V = G.V()

    alphalist = []
    initiallist = []
    resultlist = []
    for i in V:
        initiallist.append(i)
        i.colornum = 0
    resultlist.append(initiallist)

    while alphalist != resultlist:
        alphalist = resultlist
        print(str(alphalist) + " with length: " + str(len(alphalist)))
        resultlist = []
        for colorlist in alphalist:
            initiallist = []
            initiallist.append(colorlist[0])
            resultlist.append(initiallist)
            for k in range(len(colorlist) - 1):
                if not same_color(colorlist[k], colorlist[k+1]):
                    nolistfound = True
                    v = colorlist[k + 1]
                    # print("Vertex " + str(v))
                    for i in resultlist:
                        if i != colorlist:
                            if same_color(i[0],v):
                                i.append(v)
                                nolistfound = False
                    if nolistfound:
                        newcolor = [v]
                        resultlist.append(newcolor)
                else:
                    v = colorlist[k + 1]
                    for i in resultlist:
                        if i != colorlist:
                            if same_color(i[0], v):
                                i.append(v)
        for colorlist in resultlist:
            for vertex in colorlist:
                vertex.colornum = resultlist.index(colorlist)

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

    # print("Two sets with vertices: " + str(u) +" and " + str(v))
    # print(str(u) + " with set: " + str(S))
    # print(str(v) + " with set: " + str(T))

    return S == T


L = loadgraph("../graphs/colorref_largeexample_4_1026.grl", graphclass=graph, readlist=True)
G = L[0][2]
G = refine(G)
writeDOT(G, "examplegraph.dot")