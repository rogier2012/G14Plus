class doubly_linked_list:
    first = None
    last = None
    current = None

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

    def append(self,node):
        if self.first is None:
            self.first = node
        if self.last is None:
            self.last = node
        else:
            self.last.tail = node
            node.head = self.last
            self.last = node

    def remove(self, node):
        if node.head is None:
            self.first = node.tail
        else:
            node.head.tail = node.tail
        if node.tail is None:
            self.last = node.head
        else:
            node.tail.head = node.head

    def pop(self):

        node = self.last
        if node.head is not None:
            new_last = node.head
            new_last.tail = None
            self.last = new_last
        else:
            self.first = None
            self.last = None
        return node

    def extend(self, linked_list):
        if linked_list.first is not None:
            node = self.last
            node.tail = linked_list.first
            linked_list.first.head = node
            self.last = linked_list.last



    def __str__(self):
        node = self.first
        result = "["
        while node is not None:
            result = result + str(node)
            if node.tail is not None:
                result = result + ", "
            node = node.tail
        result = result + "]"
        return result

    def __len__(self):
        node = self.first
        result = 0
        while node is not None:
            result = result + 1
            node = node.tail
        return result

    def __iter__(self):
        return self

    def __next__(self):
        if self.current == self.last:
            raise StopIteration
        elif self.current == None:
            self.current = self.first
        else:
            self.current = self.current.tail
        return self.current


    def to_list(self):
        node = self.first
        result = []
        while node is not None:
            result.append(node)
            node = node.tail

        return result


    def len_greater_than_zero(self):
        return self.first is not None


class color_node:
    head = None
    tail = None
    color = 0
