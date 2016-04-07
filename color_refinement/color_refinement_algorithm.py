import time

from assets.fastgraphs import graph, colorclass
from assets.graphIO import loadgraph, writeDOT
from assets.GraphFunctions import disjointunion
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
    print("[REFINE] Execution time:", time3)
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
    if len(alpha1) == 2 and alpha1[1][0].oldgraph == H:
        return 0
    if not balanced(alpha1):
        return 0
    if bijection(alpha1, len(GH.V())/2):
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
    for color_list in alpha:
        if len(color_list) % 2 == 1:
            return False

    return True


def bijection(alpha, length):

    for color_list in alpha:
        if len(color_list) != 2:
            return False
        if len(color_list) == 2 and (color_list[0].get_label() > length or color_list[1].get_label() < length):
            return False
    return True


def pathsBench():
    t1 = timeMs()
    L = loadgraph("../graphs/threepaths640.gr", graphclass=graph)
    fast_partitioning(L, [], [])
    # refine(L, [], [])
    timing = (timeMs() - t1)
    print("Time runned: " + str(timing) + "ms")
    writeDOT(L, "example.dot")
    return timing


def countAutomorphisms(findSingleIso=False, writeDot=False):
    L = loadgraph("../graphs/cographs1.grl", graphclass=graph, readlist=True)
    G = L[0][0]
    H = L[0][3]

    GH = disjointunion(G, H)
    t1 = timeMs()
    numberofIso = countIsomorphism(GH, G, H, D, I, 1, findSingleIso)
    print("Number of Isomorphisms: " + str(numberofIso))
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
    timer = timeMs()
    color_list = dict()
    queue = list()

    # *** INITIALISATIE ***
    deg_id = dict()

    for v in G.V():
        if v not in D and v not in I:
            if v.deg() in deg_id.keys():
                color_list[deg_id[v.deg()]].addvertex(v)
                v.setColorClass(color_list[deg_id[v.deg()]])
            else:
                len1 = len(color_list) + 1
                color_list[len1] = colorclass(len1, [v])
                v.setColorClass(color_list[len1])
                deg_id[v.deg()] = len1

    for w in color_list:
        queue.append(color_list[w])
        color_list[w].inQueue()

    for index in range(len(D)):
        len1 = len(color_list) + 1
        next_color = colorclass(len1, [D[index], I[index]])
        color_list[len1] = next_color
        D[index].setColorClass(next_color)
        I[index].setColorClass(next_color)

    while len(queue) > 0:
        color_from_queue = queue.pop()

        d_counts = generate_d_counts_on_color(color_from_queue)

        for color_entry in d_counts:
            d_count = d_counts[color_entry]

            if len(d_count) > 1:
                color_pair = d_count.popitem()
                color_entry.setvertices(color_pair[1])
                new_color_list = list()
                max_size_color = color_entry

                for new_color_class in d_count:
                    new_color = colorclass(len(color_list) + 1, d_count[new_color_class])
                    if len(new_color.getvertices()) > len(max_size_color.getvertices()):
                        max_size_color = new_color

                    color_list[new_color.id] = new_color

                    for vertex in d_count[new_color_class]:
                        vertex.setColorClass(new_color)

                    new_color_list.append(new_color)
                    new_color.inQueue()

                if color_entry.in_queue:
                    queue.extend(new_color_list)
                else:
                    if max_size_color == color_entry:
                        queue.extend(new_color_list)
                    else:
                        queue.append(color_entry)
                        color_entry.inQueue()
                        new_color_list.remove(max_size_color)
                        max_size_color.notInQueue()
                        queue.extend(new_color_list)

        color_from_queue.notInQueue()

    total_list = list()
    for color_entry in color_list:
        total_list.append(color_list[color_entry].getvertices())

    timer2 = timeMs() - timer
    print("[FAST REFINE] Execution time:", timer2)

    return total_list


def generate_d_counts_on_color(color_entry):
    neighbourhood_color_dict = dict()
    color_set = set()
    for vertex in color_entry.getvertices():
        for neighbour in vertex.nbs():
            if neighbour not in neighbourhood_color_dict:
                neighbourhood_color_dict[neighbour] = 1
            else:
                neighbourhood_color_dict[neighbour] += 1
            color_set.add(neighbour.colorclass)

    result = dict()

    for color in color_set:
        d_count = dict()
        for vertex in color.getvertices():
            if vertex in neighbourhood_color_dict:
                nbs_count = neighbourhood_color_dict[vertex]
            else:
                nbs_count = 0
            if nbs_count in d_count:
                d_count[nbs_count].append(vertex)
            else:
                d_count[nbs_count] = [vertex]

        if len(d_count) > 1:
            result[color] = d_count

    return result

def twins(graph):
    neighbourlist = dict()
    pointer = list()
    twinlist = list()

    for vertex in graph.V():
        nbs = vertex.nbs()
        nbs1 = []
        nbs1.extend(nbs)
        nbs1.append(vertex)

        if nbs in pointer:
            twinlist.append([vertex,neighbourlist.get(pointer.index(nbs))])

        elif nbs1 in pointer:
            twinlist.append([vertex, neighbourlist.get(pointer.index(nbs1))])

        else:
            neighbourlist[len(neighbourlist)] = vertex
            pointer.append(vertex.nbs())

    return twinlist

def gi_problem(graphlist):
    graphs = loadgraph("../graphs/" + graphlist + ".gr", graphclass=graph, readlist=True)[0]
    print("Sets of isomorphic graphs:")
    for i in range(len(graphs)):
        for j in range(i, len(graphs)):

            if i != j:
                G = graphs[i]
                H = graphs[j]
                GH = disjointunion(G, H)
                numIso = countIsomorphism(GH, G, H, [], [], 1, True)
                if numIso > 0:
                    print("[" + str(i) + ", " + str(j) + "]")

def aut_problem(graphlist):
    graphs = loadgraph("../graphs/" + graphlist + ".grl", graphclass=graph, readlist=True)[0]
    print("Sets of isomorphic graphs:   Number of automorphisms:")
    isomorphisms = []
    for i in range(len(graphs)):
        for j in range(i, len(graphs)):

            if i != j:
                G = graphs[i]
                H = graphs[j]
                GH = disjointunion(G, H)
                numIso = countIsomorphism(GH, G, H, [], [], 1, True)
                if numIso > 0:
                    isomorphisms.append([i,j])
    for k in isomorphisms:
        i = k[0]
        G = graphs[i]
        H = graphs[i]
        GH = disjointunion(G, H)
        numIso = countIsomorphism(GH, G, H, [], [], 1, False)
        if numIso > 0:
            print(str(k) + ":                      " + str(numIso))


def program():
    run = True
    while run:
        print("Choose your problem below:")
        print("     1. GI Problem")
        print("     2. AUT Problem")
        print("     3. Close")
        int1 = int(input("Enter your input: "))
        if int1 == 1:
            print("Enter the graphlist file:")

            str = input("Enter your input: ")
            print("")
            file_found = False
            while not file_found:
                try:
                    gi_problem(str)
                    file_found = True
                except FileNotFoundError:
                    print("File not found, please enter a valid filename")
                    print("Enter the graphlist file:")
                    str = input("Enter your input: ")
                    print("")


            print("")
        elif int1 == 2:
            print("Enter the graphlist file:")
            str = input("Enter your input: ")
            print("")
            file_found = False
            while not file_found:
                try:
                    aut_problem(str)
                    file_found = True
                except FileNotFoundError:
                    print("File not found, please enter a valid filename")
                    print("Enter the graphlist file:")
                    str = input("Enter your input: ")
                    print("")
            print("")

        elif int1 == 3:
            run = False


program()
# pathsBench()