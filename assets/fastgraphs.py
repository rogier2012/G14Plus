from assets.basicgraphs import graph, edge, GraphError, vertex


class vertex(vertex):
    def __init__(self, graph, label=0):
        self._graph = graph
        self._label = label
        self._inclist = []
        # incl = []
        # for e in self._graph._E:
        #     if e.incident(self):
        #         incl.append(e)

    def addedge(self, edge):
        self._inclist.append(edge)

    def deleteedge(self, edge):
        self._inclist.remove(edge)

    def inclist(self):
        return self._inclist


class graph(graph):
    def deletevertext(self, vertex):
        edgelist = vertex.inclist
        for edge in edgelist:
            self.deleteedge(edge)
        self._V.remove(vertex)

    def deleteedge(self, edge):
        edge.head().deleteedge(edge)
        edge.tail().deleteedge(edge)
        self._E.remove(edge)


    def addvertex(self, label=-1):
        """
        Add a vertex to the graph.
        Optional argument: a vertex label (arbitrary)
        """
        if label == -1:
            label = self._nextlabel
            self._nextlabel += 1
        u = vertex(self, label)
        self._V.append(u)
        return u


    def addedge(self, tail, head):
        if self._simple:
            if tail == head:
                raise GraphError('No loops allowed in simple graphs')
            for e in self._E:
                if (e._tail == tail and e._head == head):
                    raise GraphError(
                        'No multiedges allowed in simple graphs')
                if not self._directed:
                    if (e._tail == head and e._head == tail):
                        raise GraphError(
                            'No multiedges allowed in simple graphs')
        if not (tail._graph == self and head._graph == self):
            raise GraphError(
                'Edges of a graph G must be between vertices of G')
        e = edge(tail, head)
        tail.addedge(e)
        head.addedge(e)
        self._E.append(e)
        return e


    def adj(self, u, v):
        """
        Returns True iff vertices <u> and <v> are adjacent.
        """
        return v in u.inclist.head() or v in u.inclist.tail()


class coloring():
    def __init__(self, ordered_list):
        self._i = 1
        self._colorlist = dict()
        self._queue = dict()

        for tup in ordered_list:
            label = tup[0]
            degree = tup[1]

            if degree in self._colorlist:
                self._colorlist[degree].append(label)
            else:
                self._colorlist[degree] = [label]

    def __getitem__(self, item):
        if item in self._colorlist:
            return self._colorlist[item]
        else:
            return None

    def __len__(self):
        return len(self._colorlist)

    def getcolors(self):
        return list(self._colorlist.keys())

    def addtoqueue(self, color):
        if not color in self._queue:
            self._queue[color] = 0
        else:
            return False

    def removefromqueue(self, color):
        if color in self._queue:
            self._queue.pop(color)
        else:
            return False

    def inqueue(self, color):
        if color in self._queue:
            return True
        else:
            return False