import time

from assets.fastgraphs import graph
from assets.graphIO import loadgraph
from assets.graphfunctions import disjointunion


def refine(G, D, I):
    V = G.V()
    alpha_list = []
    initial_list = []
    result_list = []
    if len(D) == 0:
        for i in V:
            initial_list.append(i)
            i.colornum = 0
        result_list.append(initial_list)
    else:
        VList = []
        VList.extend(V)
        VList = [item for item in VList if (item not in D and item not in I)]
        for i in VList:
            initial_list.append(i)
            i.colornum = 0
        result_list.append(initial_list)

        for i in range(len(D)):
            D[i].colornum = i + 1
            I[i].colornum = i + 1
            next_list = [D[i], I[i]]
            result_list.append(next_list)

    while alpha_list != result_list:
        alpha_list = result_list
        print(str(alpha_list) + " with length: " + str(len(alpha_list)))
        result_list = []
        for color_list in alpha_list:
            initial_list = [color_list[0]]
            result_list.append(initial_list)
            index = result_list.index(initial_list)
            # result_list[index][0].colornum = index
            for k in range(1, len(color_list)):
                v = color_list[k]
                if not same_color(color_list[0], v):
                    no_list_found = True

                    for i in result_list:
                        if same_color(i[0], v):
                            # v.colornum = result_list.index(i)
                            i.append(v)

                            no_list_found = False

                    if no_list_found:
                        # v.colornum = len(result_list)
                        new_color = [v]
                        result_list.append(new_color)

                else:
                    # v.colornum = index
                    result_list[index].append(v)


        for color_list in result_list:
            for vertex in color_list:
                vertex.colornum = result_list.index(color_list)
    return alpha_list


def individual_refinement(G, D, I):
    return refine(G, D, I)


def countIsomorphism(GH, G, H, D, I, findSingleIso=False):
    # print("Begin individual Refinement with " + str(D) + " and " + str(I))
    alpha1 = individual_refinement(GH, D, I)
    if not balanced(alpha1):
        return 0
    if bijection(alpha1):
        return 1

    color = None
    # found = False
    for color_list in alpha1:
        if len(color_list) >= 4:
            color = color_list
            # found = True
    x = color[0]
    # print("List found: " + str(found))
    num = 0
    for index in range(len(color) // 2, len(color)):
        nD = []
        nD.extend(D)
        nD.append(x)
        nI = []
        nI.extend(I)
        nI.append(color[index])
        num = num + countIsomorphism(GH, G, H, nD, nI, findSingleIso)
        if findSingleIso and num > 0:
            return num
    return num


def same_color(u, v):
    S = []
    T = []
    for vertex in u.nbs():
        S.append(vertex.colornum)
    for vertex in v.nbs():
        T.append(vertex.colornum)
    S.sort()
    T.sort()
    #     print("Two sets with vertices: " + str(u) +" and " + str(v))
    #     print(str(u) + " with set: " + str(S))
    #     print(str(v) + " with set: " + str(T))
    return S == T


def balanced(alpha):
    even = True
    for colorlist in alpha:
        if len(colorlist) % 2 == 1:
            even = False

    return even


def bijection(alpha):
    more = True
    for color_list in alpha:
        if len(color_list) >= 4:
            more = False
    return more


L = loadgraph("../graphs/colorref_smallexample_4_7.grl", graphclass=graph, readlist=True)
# L = loadgraph("../graphs/torus24.grl", graphclass=graph, readlist=True)
# L = loadgraph("../graphs/threepaths160.gr", graphclass=graph)
G = L[0][1]
H = L[0][3]
GH = disjointunion(G, H)

t1 = int(round(time.time() * 1000))
# alpha1 = refine(L, [], [])
numberofIso = countIsomorphism(GH, G, H, [], [])
print("Number of Isomorphisms: " + str(numberofIso))
print("Time runned: " + str((int(round(time.time() * 1000)) - t1) // 1000) + "s")
# print("Graph is balanced: " + str(balanced(alpha1)))
# print("Graph is bijection: " + str(bijection(alpha1)))
# writeDOT(GH, "examplegraph.dot")
