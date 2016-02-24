from assets.fastgraphs import graph


def createcompletegraph(n):
    G = graph(n)
    for n in G.V():
        for m in G.V():
            if n != m:
                G.addedge(n, m)
    return G


def createpath(G):
    for n in range(1, len(G.V())):
        G.addedge(G.V()[n - 1], G.V()[n])
    return G


def createcycle(G):
    for n in range(1, len(G.V())):
        G.addedge(G.V()[n - 1], G.V()[n])
    G.addedge(G.V()[len(G.V()) - 1], G.V()[0])
    return G


def disjointunion(G, H):
    K = graph()
    GMap = {}
    HMap = {}
    for n in G.V():
        value = K.addvertex()
        key = n
        GMap[key] = value
    for n in H.V():
        value = K.addvertex()
        key = n
        HMap[key] = value

    for n in G.E():
        K.addedge(GMap.get(n.tail()), GMap.get(n.head()))
    for n in H.E():
        K.addedge(HMap.get(n.tail()), HMap.get(n.head()))

    return K


G = createpath(graph(2))
# print(G)
H = createpath(graph(3))
# print(H)

F = disjointunion(G, H)
# print(F)

G = createcompletegraph(4)
# print(G)
