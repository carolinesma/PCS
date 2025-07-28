class Node:
    def __init__(self, frequency, symbol=None, code = ""):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None
        self.code = ""
        self.L = 0

    def __lt__(self, other):
        return self.frequency < other.frequency

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.frequency == other.frequency
        return False

    def is_leaf(self):
        return self.left is None and self.right is None

class OrderedQueue:
    def __init__(self):
        self.nodes = []

    def pop(self):
        if not self.nodes:
            raise IndexError("pop from empty list")
        return self.nodes.pop(0)
    
    def push_front(self, node):
        return self.nodes.insert(0, node)

    def insert_sorted(self, node):
        for i in range(len(self.nodes)):
            if self.nodes[i] > node:
                self.nodes.insert(i, node)
                return
        self.nodes.append(node)

    def __len__(self):
        return len(self.nodes)