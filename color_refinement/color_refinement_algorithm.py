import time

from assets.fastgraphs import graph
from assets.graphIO import loadgraph


def refine(G, D, I):
    time1 = timeMs()

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
    time2 = timeMs() - time1
    print("Initialisation time: " + str(time2 // 1000) + "s")
    partTime = 0
    coloringTime = 0
    while alpha_list != result_list:
        alpha_list = result_list
        # print(str(alpha_list) + " with length: " + str(len(alpha_list)))
        result_list = []
        part1 = timeMs()
        for color_list in alpha_list:
            initial_list = [color_list[0]]
            result_list.append(initial_list)
            index = result_list.index(initial_list)
            # result_list[index][0].colornum = index
            neighbourU = neighbourhood(color_list[0])
            for k in range(1, len(color_list)):
                v = color_list[k]
                neighbourV = neighbourhood(v)
                if not same_color(neighbourU, neighbourV):
                    no_list_found = True

                    for i in result_list:
                        neighbourI = neighbourhood(i[0])
                        if same_color(neighbourI, neighbourV):
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
        partTime = partTime + (timeMs() - part1)
        coloring1 = timeMs()
        for color_list in result_list:
            for vertex in color_list:
                vertex.colornum = result_list.index(color_list)
        coloringTime = coloringTime + (timeMs() - coloring1)

    time3 = timeMs() - time1
    print("Loop time: " + str(time3 // 1000) + "s")
    print("Partitioning time: " + str(partTime // 1000) + "s")
    print("Coloring time: " + str(coloringTime // 1000) + "s")
    return alpha_list


def individual_refinement(G, D, I):
    return refine(G, D, I)


def timeMs():
    return int(round(time.time() * 1000))


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


def same_color(S, T):
    # S = []
    # T = []
    # for vertex in u.nbs():
    #     S.append(vertex.colornum)
    # for vertex in v.nbs():
    #     T.append(vertex.colornum)
    # S.sort()
    # T.sort()
    #     print("Two sets with vertices: " + str(u) +" and " + str(v))
    #     print(str(u) + " with set: " + str(S))
    #     print(str(v) + " with set: " + str(T))
    return S == T


def neighbourhood(u):
    S = []
    for vertex in u.nbs():
        S.append(vertex.colornum)
    S.sort()
    return S


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


# L = loadgraph("../graphs/colorref_smallexample_4_7.grl", graphclass=graph, readlist=True)
# L = loadgraph("../graphs/products72.grl", graphclass=graph, readlist=True)
L = loadgraph("../graphs/threepaths640.gr", graphclass=graph)
# G = L[0][4]
# H = L[0][7]
# GH = disjointunion(G, H)

t1 = timeMs()
alpha1 = refine(L, [], [])
# numberofIso = countIsomorphism(GH, G, H, [], [], False)
# print("Number of Isomorphisms: " + str(numberofIso))
print("Time runned: " + str((timeMs() // 1000)) + "s")
# print("Graph is balanced: " + str(balanced(alpha1)))
# print("Graph is bijection: " + str(bijection(alpha1)))
# writeDOT(GH, "examplegraph.dot")
