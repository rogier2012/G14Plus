from assets.fastgraphs import graph
from assets.graphIO import loadgraph, writeDOT


def refine(G):
    V = G.V()

    alpha_list = []
    initial_list = []
    result_list = []

    for i in V:
        initial_list.append(i)
        i.colornum = 0
    result_list.append(initial_list)

    while alpha_list != result_list:
        alpha_list = result_list
        print(str(alpha_list) + " with length: " + str(len(alpha_list)))
        result_list = []
        for color_list in alpha_list:
            initial_list = [color_list[0]]
            result_list.append(initial_list)

            for k in range(len(color_list) - 1):
                if not same_color(color_list[k], color_list[k + 1]):
                    no_list_found = True
                    v = color_list[k + 1]
                    # print("Vertex " + str(v))

                    for i in result_list:
                        if same_color(i[0], v):
                                i.append(v)
                                no_list_found = False

                    if no_list_found:
                        new_color = [v]
                        result_list.append(new_color)

                else:
                    v = color_list[k + 1]
                    for i in result_list:
                        if same_color(i[0], v):
                                i.append(v)

        for color_list in result_list:
            for vertex in color_list:
                vertex.colornum = result_list.index(color_list)

    return alpha_list

#put k in new color in result list with same properties or create a new list inside result list


def same_color(u, v):
    S = []
    T = []
    for vertex in u.nbs():
        S.append(vertex.colornum)
    for vertex in v.nbs():
        T.append(vertex.colornum)
    S.sort()
    T.sort()
    # print("Two sets with vertices: " + str(u) +" and " + str(v))
    # print(str(u) + " with set: " + str(S))
    # print(str(v) + " with set: " + str(T))

    return S == T


L = loadgraph("../graphs/colorref_smallexample_4_7.grl", graphclass=graph, readlist=True)
G = L[0][2]
colorschemes = []
# for graph in L[0]:
#     colorschemes.append(refine(graph))

refine(G)
writeDOT(G, "examplegraph.dot")