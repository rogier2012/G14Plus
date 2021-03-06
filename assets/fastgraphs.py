from assets.basicgraphs import graph, edge, GraphError, vertex


class vertex(vertex):
    def __init__(self, graph, label=0):
        self._graph = graph
        self._label = label
        self._inclist = []
        self._neighbourlist = []
        # self._neighbourclass = dict()
        self.colorclass = None
        self.oldgraph= None

    def addedge(self, edge):
        self._inclist.append(edge)
        self._neighbourlist.append(edge.otherend(self))

    def delete_edge(self, edge):
        self._inclist.remove(edge)
        self._neighbourlist.remove(edge.otherend(self))

    def inclist(self):
        return self._inclist

    def setColorClass(self, colorclass):
        self.colorclass = colorclass

    def nbs(self):
        return self._neighbourlist

    def get_label(self):
        return self._label


class graph(graph):
    def delete_vertex(self, vertex):
        if vertex in self._V:
            edgelist = []
            edgelist.extend(vertex.inclist())
            for edge in edgelist:
                self.delete_edge(edge)
            self._V.remove(vertex)

    def delete_edge(self, edge):
        edge.head().delete_edge(edge)
        edge.tail().delete_edge(edge)
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


class colorclass():
    head = None
    tail = None
    in_queue = False

    def __init__(self, id, vertices=list()):
        self._vertices = vertices
        self.id = id

    def getvertices(self):
        return self._vertices

    def addvertex(self, vertex):
        self._vertices.append(vertex)

    def __lt__(self, other):
        return len(self._vertices) < len(other._vertices)

    def __repr__(self):
        return "(ID = " + str(self.id) + ", V = " + str(self._vertices) + ")"

    def setvertices(self, vertices):
        self._vertices = vertices

    def inQueue(self):
        self.in_queue = True

    def notInQueue(self):
        self.in_queue = False


class dcounts():
    def __init__(self):
        self.total_dcounts = dict()

    def update(self, oldcolor, new_colors):
        pass

    def get_d_counts(self,color):
        return self.total_dcounts[color]

    def generate(self,color_list):
        pass