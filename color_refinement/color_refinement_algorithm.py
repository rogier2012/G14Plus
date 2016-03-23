import sys
import time

from assets.fastgraphs import graph, colorclass
from assets.graphIO import loadgraph, writeDOT
from assets.graphfunctions import disjointunion
from color_refinement.branch_algorithms import *


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
    # print("Initialisation time: " + str(time2 // 1000) + "s")
    partTime = 0
    coloringTime = 0
    while alpha_list != result_list:
        alpha_list = result_list
        # print(str(alpha_list) + " with length: " + str(len(alpha_list)))
        result_list = []
        part1 = timeMs()
        for color_list in alpha_list:
            initial_list = []
            new_list = []
            nbslist = listOfNodeNeighbourhoods(color_list)
            for k in range(len(nbslist)):
                if k == 0 or same_color(nbslist[0], nbslist[k]):
                    initial_list.append(color_list[k])
                else:
                    found = False
                    for l in new_list:
                        if same_color(neighbourhood(l[0]), nbslist[k]):
                            l.append(color_list[k])
                            found = True
                    if not found:
                        new_list.append([color_list[k]])

            result_list.append(initial_list)
            result_list.extend(new_list)
        partTime = partTime + (timeMs() - part1)
        coloring1 = timeMs()
        for colornumber in range(len(result_list)):
            for vertexnum in range(len(result_list[colornumber])):
                result_list[colornumber][vertexnum].colornum = colornumber
        coloringTime = coloringTime + (timeMs() - coloring1)

    time3 = timeMs() - time1
    # print("Loop time: " + str(time3 // 1000) + "s")
    # print("Partitioning time: " + str(partTime // 1000) + "s")
    # print("Coloring time: " + str(coloringTime // 1000) + "s")
    return alpha_list


def individual_refinement(G, D, I):
    return refine(G, D, I)


def timeMs():
    return int(round(time.time() * 1000))


def listOfNodeNeighbourhoods(color_list):
    result = []
    for u in color_list:
        result.append(neighbourhood(u))
    return result


def countIsomorphism(GH, G, H, D, I, branching_rule, findSingleIso=False):
    alpha1 = individual_refinement(GH, D, I)
    if not balanced(alpha1):
        return 0
    if bijection(alpha1):
        return 1

    color = None
    if branching_rule == 1:
        color = branchingrule1(alpha1)
    elif branching_rule == 2:
        color = branchingrule2(alpha1)
    elif branching_rule == 3:
        color = branchingrule3(alpha1)




    x = color[0]
    num = 0
    for index in range(len(color) // 2, len(color)):
        nD = []
        nD.extend(D)
        nD.append(x)
        nI = []
        nI.extend(I)
        nI.append(color[index])
        num = num + countIsomorphism(GH, G, H, nD, nI, branching_rule, findSingleIso)
        if findSingleIso and num > 0:
            return num
    return num


def same_color(S, T):
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


def pathsBench():
    t1 = timeMs()
    L = loadgraph("../graphs/threepaths640.gr", graphclass=graph)

    refine(L, [], [])
    print("Time runned: " + str((timeMs() - t1) // 1000) + "s")
    writeDOT(L, "example.dot")


def countAutomorphisms(findSingleIso=False, writeDot=False):
    # L = loadgraph("../graphs/colorref_smallexample_4_7.grl", graphclass=graph, readlist=True)


    L = loadgraph("../graphs/colorref_largeexample_4_1026.grl", graphclass=graph, readlist=True)
    G = L[0][0]
    H = L[0][1]
    GH = disjointunion(G, H)

    t1 = timeMs()

    numberofIso = countIsomorphism(GH, G, H, [], [], 1, findSingleIso)
    print("Number of Isomorphisms: " + str(numberofIso))
    print("Time runned: " + str((timeMs() - t1)) + "ms")
    if writeDot:
        writeDOT(GH, "examplegraph.dot")


def branching_rules(findSingleIso=False, writeDot=False):
    # L = loadgraph("../graphs/colorref_smallexample_4_7.grl", graphclass=graph, readlist=True)
    branching_rules = {0, 1, 2, 3}
    for rule in branching_rules:

        L = loadgraph("../graphs/products72.grl", graphclass=graph, readlist=True)
        G = L[0][4]
        H = L[0][7]
        GH = disjointunion(G, H)

        t1 = timeMs()

        numberofIso = countIsomorphism(GH, G, H, [], [], rule, findSingleIso)
        print("Number of Isomorphisms: " + str(numberofIso))
        print("Time runned: " + str((timeMs() - t1)) + "ms for branching rule: " + str(rule))
        if writeDot:
            writeDOT(GH, "examplegraph.dot")


def fast_partitioning(G):
    color_list = dict()
    queue = list()

    # *** INITIALISATIE ***
    for vertex in G.V():
        if not vertex.deg() in color_list.keys():
            color_list[vertex.deg()] = colorclass(vertex.deg())

        color_list[vertex.deg()].addvertex(vertex)

    for w in sorted(color_list, key=color_list.get):
        queue.append(color_list[w])

    queue.pop(len(queue) - 1)

    # ***
    for color_entry in queue:
        relative_color_list = list(color_list.values())
        relative_color_list.remove(color_entry)

        relative_vertices = list()

        for color in relative_color_list:
            relative_vertices += color.getvertices()

        refine_partitioning(color_entry, relative_vertices)


def refine_partitioning(color_entry, relative_vertices):
    color_vertices = color_entry.getvertices()
    neighbour_list = dict()

    for vertex in relative_vertices:
        vertex_neighbours = vertex.nbs()
        key = len(set.intersection(set(vertex_neighbours), set(color_vertices)))

        if key in neighbour_list:
            neighbour_list[key].append(vertex)
        else:
            neighbour_list[key] = [vertex]

    print(neighbour_list)


    # test initialisatie
    # for color in color_list.keys():
    #     print(color_list[color], color_list[color]._vertices)


# pathsBench()
# countAutomorphisms(True)
# branching_rules()

L = loadgraph("../graphs/colorref_smallexample_4_7.grl", graphclass=graph, readlist=True)
G = L[0][1]

fast_partitioning(G)
