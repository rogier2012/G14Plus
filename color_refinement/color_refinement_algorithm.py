from assets.fastgraphs import graph


def refine(g):
    V = g.V()

    alphalist = []
    initiallist = []
    resultlist = []
    for i in range(len(V)):
        resultlist.append(i)
        V[i].colornum = 0

    resultlist.append(initiallist)

    while alphalist != resultlist:
        alphalist = resultlist
        resultlist = []
        for colorlist in range(len(alphalist)):
            for k in range(len(colorlist) -1 ):
                if not same_color(colorlist[k], colorlist[k+1]):
                    nolistfound = True;
                    v = colorlist[k+1]
                    for i in resultlist:
                        if i != colorlist:
                            if same_color(i[0],v):
                                i.append(v)
                                nolistfound = False;
                    if nolistfound:
                        newcolor = [v]
                        resultlist.append(newcolor)

    return alphalist


def same_color(u,v):
    return len(u.nbs()) == len(v.nbs()) and u.nbs().colornum == v.nbs().colornum
#put k in new color in result list with same properties or create a new list inside result list