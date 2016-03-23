class double_linked_list:
    first = None
    last = None

    def insert_beginning(self, node):
        self.first.head = node
        self.first = node

    def insert_ending(self, node):
        self.last.tail = node
        self.last = node

    def insert_before(self, node, newnode):
        newnode.head = node.head
        newnode.tail = node
        if node.head is None:
            self.first = newnode
        else:
            node.head.tail = newnode
        node.head = newnode

    def insert_after(self, node, newnode):
        newnode.head = node
        newnode.tail = node.tail
        if node.tail is None:
            self.last = newnode
        else:
            node.tail.head = newnode
        node.tail = newnode

    def remove(self, node):
        if node.head is None:
            self.first = node.tail
        else:
            node.head.tail = node.tail
        if node.tail is None:
            self.last = node.head
        else:
            node.tail.head = node.head

    def __str__(self):
        node = self.first
        result = "["
        while node is not None:
            result = result + str(node)
            if node.tail is not None:
                result = result + ", "
            node = node.tail
        return result

    def __len__(self):
        node = self.first
        result = 0
        while node is not None:
            result = result + 1
            node = node.tail
        return result

    def to_list(self):
        node = self.first
        result = []
        while node is not None:
            result.append(node)
            node = node.tail

        return result


class color_class_node:
    head = None
    tail = None
    list_vertices = None

    def __init__(self, list_vertices):
        self.list_vertices = list_vertices
