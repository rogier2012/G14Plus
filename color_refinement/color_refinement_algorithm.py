from assets.fastgraphs import graph


def refine(g):
    V = g.V()

    alphalist = []
    initiallist = []
    resultlist = []
    for i in range(len(V)):
        initiallist.append(i)
        V[i].colornum = 0

    alphalist.append(initiallist)

    while alphalist != resultlist:
        resultlist = []
        for colorlist in range(len(alphalist)):
            for k in range(len(colorlist)):
                if k+1 <= len(colorlist):
                    if len(colorlist[k].nbs()) != len(colorlist[k+1]):
#                     put k in new color in result list with same properties or create a new list inside result list
                        pass
                    elif colorlist[k].nbs().colornum !=  colorlist[k+1].nbs().colornum:
#                     put k in new color in result list with same properties or create a new list inside result list
                        pass





