import numpy as np # type: ignore
from .utils import OrderedQueue, Node

class GeometricHuffmanCode:
    def __init__(self, symbols, distribution):
        self.cut_tree = np.zeros(len(distribution), dtype=bool)
        self.root = self._build_tree(symbols, distribution)
        self.codebook = []
        self.dyadic_distribution = []
        self._generate_codes(self.root, "")
        self._generate_distribution()

    def _build_tree(self, symbols, distribution):
        queue = OrderedQueue()
        for symbol, freq in zip(symbols, distribution):
            queue.insert_sorted(Node(freq, symbol))

        for k in range(len(queue)-1):   
            x_m = queue.pop()
            x_m1 = queue.pop()
            
            if 2 * np.sqrt(x_m.frequency * x_m1.frequency) <= x_m1.frequency:
                queue.push_front(x_m1)
                self.cut_tree[k] = True
            else:
                merged = Node(2 * np.sqrt(x_m.frequency * x_m1.frequency), 0)
                merged.left = x_m
                merged.right = x_m1
                queue.insert_sorted(merged)
        
        return queue.pop()
    
    def _generate_codes(self, node, codeword):
        if node is None:
            return
        if node.is_leaf():
            node.code = codeword
            node.L = len(codeword)
            node.frequency = pow(2,-node.L)
            self.codebook.append(node)
        else:
            self._generate_codes(node.left, codeword + "0")
            self._generate_codes(node.right, codeword + "1")

    def _generate_distribution(self):
        for node in self.codebook:
            self.dyadic_distribution.append(node.frequency)
        if np.any(self.cut_tree):
            indices = np.where(self.cut_tree)[0]
            for idx in sorted(indices, reverse=True):
                self.dyadic_distribution.insert(idx, 0)