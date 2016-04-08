class doubly_linked_list:

    def __init__(self):
        self.first = None
        self.last = None
        self.current = None
        self.length = 0


    def insert_beginning(self, node):
        self.first.heads = node
        self.first = node

        self.current = self.first
        self.length += 1

    def insert_ending(self, node):
        self.last.tails = node
        self.last = node
        self.length += 1

    def insert_before(self, node, newnode):
        newnode.heads = node.heads
        newnode.tails = node
        if node.heads is None:
            self.first = newnode
            self.current = self.first
        else:
            node.heads.tails = newnode
        node.heads = newnode
        self.length += 1

    def insert_after(self, node, newnode):
        newnode.heads = node
        newnode.tails = node.tails
        if node.tails is None:
            self.last = newnode
        else:
            node.tails.heads = newnode
        node.tails = newnode

        self.length += 1

    def append(self,node):
        if self.first is None:
            self.first = node
            self.current = self.first
        if self.last is None:
            self.last = node
        else:
            self.last.tails = node
            node.heads = self.last
            self.last = node
        self.length += 1

    def remove(self, node):
        if node.heads is None:
            self.first = node.tails
            self.current = self.first
        else:
            node.heads.tails = node.tails
        if node.tails is None:
            self.last = node.heads
        else:
            node.tails.heads = node.heads
        self.length -= 1
    def pop(self):

        node = self.last
        if node.heads is not None:
            new_last = node.heads
            new_last.tails = None
            self.last = new_last
        else:
            self.first = None
            self.last = None
        self.length -= 1
        return node

    def extend(self, linked_list):
        if self.first is None:
            self.first = linked_list.first
            self.current = self.first
            self.last = linked_list.last
            self.length = linked_list.length
        elif linked_list.first is not None:
            node = self.last
            node.tails = linked_list.first
            linked_list.first.heads = node
            self.last = linked_list.last
            self.length += linked_list.length

    def __str__(self):
        node = self.first
        result = "["
        while node is not None:
            result = result + str(node)
            if node.tails is not None:
                result = result + ", "
            node = node.tails
        result = result + "]"
        return result

    def __len__(self):
        return self.length

    def __iter__(self):
        return ListIterator(self)

    # def __next__(self):
    #     if self.current is None:
    #         self.current = self.first
    #         raise StopIteration()
    #     else:
    #         self.current = self.current.tails
    #     return self.current


    def to_list(self):
        node = self.first
        result = []
        while node is not None:
            result.append(node)
            node = node.tails


        return result


    def len_greater_than_zero(self):
        return self.first is not None

class ListIterator:
    # other stuff ...
    def __iter__(self,):
        while self._current:
            yield self._current
            self._current = self._current.next
        self._current = self.heads # Reset the current pointer


class color_node:
    heads = None
    tails = None
    color = 0
