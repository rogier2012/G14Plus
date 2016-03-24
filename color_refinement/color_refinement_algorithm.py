import sys
import time

from assets.fastgraphs import graph, colorclass
from assets.graphIO import loadgraph, writeDOT
from assets.graphfunctions import disjointunion
from color_refinement.branch_algorithms import *
from assets.doubly_linked_list import *


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
    return fast_partitioning(G, D, I)


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
    for color_list in alpha:
        if len(color_list) % 2 == 1:
            even = False

    return even


def bijection(alpha):
    more = True
    for color_list in alpha:
        if len(color_list) != 2:
            more = False
    return more


def pathsBench():
    t1 = timeMs()
    L = loadgraph("../graphs/threepaths1280.gr", graphclass=graph)
    fast_partitioning(L,[],[])
    # refine(L, [], [])
    timing = (timeMs() - t1)
    # print("Time runned: " + str(timing) + "ms")
    writeDOT(L, "example.dot")
    return timing

def countAutomorphisms(findSingleIso=False, writeDot=False):
    # L = loadgraph("../graphs/colorref_smallexample_4_7.grl", graphclass=graph, readlist=True)


    L = loadgraph("../graphs/products72.grl", graphclass=graph, readlist=True)
    G = L[0][0]
    H = L[0][6]
    GH = disjointunion(G, H)

    t1 = timeMs()

    numberofIso = countIsomorphism(GH, G, H, [], [], 1, findSingleIso)
    # print("Number of Isomorphisms: " + str(numberofIso))
    timing = (timeMs() - t1)
    # print("Time runned: " + str(timing) + "ms")
    if writeDot:
        writeDOT(GH, "examplegraph.dot")
    return timing

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


def fast_partitioning(G, D, I):
    color_list = dict()
    queue = list()

    # # *** INITIALISATIE ***
    degID = dict()
    for v in G.V():
        if v not in D and v not in I:
            if v.deg() in degID.keys():
                color_list[degID[v.deg()]].addvertex(v)
                v.setColorClass(color_list[degID[v.deg()]])
            else:
                len1 = len(color_list) + 1
                color_list[len1] = colorclass(len1, [v])
                v.setColorClass(color_list[len1])
                degID[v.deg()] = len1



    for w in color_list:
        queue.append(color_list[w])
        color_list[w].inQueue()
    for i in range(len(D)):
        len1 = len(color_list) + 1
        newcolor = colorclass(len1, [D[i], I[i]])
        color_list[len1] = newcolor
        D[i].setColorClass(newcolor)
        I[i].setColorClass(newcolor)

    counter = 0
    while len(queue) > 0:
        # print(queue)
        color_entry = queue.pop()
        # Voor alle colors behalve color_entry
        neighbourhoodOfColor_dict = get_neighbourhood_color(color_entry)
        # print("Type: " + str(type(color_list.values())))
        color_set = set()
        for vertex in neighbourhoodOfColor_dict:
            color_set.add(vertex.colorclss)
        # print(str(color_entry) + " + lijst " + str(relative_color_list))
        # print("Current color: " + str(color_entry))
        for color in color_set:
            Dcount = generateDCount(color, neighbourhoodOfColor_dict)
            counter += 1
            # print(str(color) + " with Dcount: " + str(Dcount))
            if len(Dcount) > 1:
                # split
                colorPair = Dcount.popitem()
                color.setvertices(colorPair[1])
                newColorList = list()

                for new_color_class in Dcount:
                    newcolor = colorclass(len(color_list) + 1, Dcount[new_color_class])
                    color_list[newcolor._id] = newcolor
                    for vertex in Dcount[new_color_class]:
                        vertex.setColorClass(newcolor)
                    newColorList.append(newcolor)
                    newcolor.inQueue()

                if color.in_queue:
                    queue.extend(newColorList)
                else:
                    max_size_color = color
                    for color1 in newColorList:
                        if len(color1.getvertices()) > len(max_size_color.getvertices()):
                            max_size_color = color1
                    if max_size_color == color:
                        queue.extend(newColorList)
                    else:
                        queue.append(color)
                        color.inQueue()
                        newColorList.remove(max_size_color)
                        max_size_color.notInQueue()
                        queue.extend(newColorList)
                        # print("---------")
        color_entry.notInQueue()
    totallist = list()
    for color in color_list:
        totallist.append(color_list[color].getvertices())
    # print("time: " + str(t1))
    print(counter)
    return totallist


#       We now have the DCount array, so we can split.

def generateDCount(color, neighbourhoodOfColor_dict):
    Dcount = dict()
    # counter += 1
    for vertex in color.getvertices():
        if vertex in neighbourhoodOfColor_dict:
            nbscount = neighbourhoodOfColor_dict[vertex]
        else:
            nbscount = 0
        if nbscount in Dcount:
            Dcount[nbscount].append(vertex)
        else:
            Dcount[nbscount] = [vertex]
    return Dcount



def get_neighbourhood_color(colorentry):
    # result = []
    result_dict = dict()
    for vertex in colorentry.getvertices():
        for neighbour in vertex.nbs():
            # result.append(neighbour)
            if neighbour not in result_dict:
                result_dict[neighbour] = 1
            else:
                result_dict[neighbour] += 1
    return result_dict




L = loadgraph("../graphs/colorref_smallexample_4_7.grl", graphclass=graph, readlist=True)
G = L[0][1]
# refine(G, [], [])
writeDOT(G, "grpah.dot")
# fast_partitioning(G)

L = loadgraph("../graphs/colorref_smallexample_4_7.grl", graphclass=graph, readlist=True)
G = L[0][0]
H = L[0][2]
GH = disjointunion(G, H)
alpha1 = fast_partitioning(GH,[],[])
print("Balanced: " + str(balanced(alpha1)))
print("Bijective: " + str(bijection(alpha1)))


timer = 0
for i in range(0,10):
    # timer = timer + countAutomorphisms()
    timer = timer + pathsBench()
print("Average time over 10 rounds: " + str(timer//10))
# pathsBench()
