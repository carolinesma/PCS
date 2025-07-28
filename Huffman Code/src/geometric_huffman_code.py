import numpy as np # type: ignore
from utils import OrderedQueue, Node

class GeometricHuffmanCode:
    def __init__(self, frequencies):
        self.cut_tree = np.zeros(len(frequencies), dtype=bool)
        self.root = self._build_tree(frequencies)
        self.codebook = []
        self.dyadic_distribution = []
        self._generate_codes(self.root, "")
        self._generate_distribution()

    def _build_tree(self, frequencies):
        queue = OrderedQueue()
        for symbol, freq in enumerate(frequencies):
            queue.insert_sorted(Node(freq, symbol))

        for k in range(len(queue)-1):   
            left = queue.pop()
            right = queue.pop()
            
            if 2 * np.sqrt(left.frequency * right.frequency) <= right.frequency:
                queue.push_front(right)
                self.cut_tree[k] = True
            else:
                merged = Node(2 * np.sqrt(left.frequency * right.frequency), 0)
                merged.left = left
                merged.right = right
                queue.push_front(merged)
        
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
            self._generate_codes(node.left, codeword + "1")
            self._generate_codes(node.right, codeword + "0")

    def _generate_distribution(self):
        for node in self.codebook:
            self.dyadic_distribution.append(node.frequency)
        if np.any(self.cut_tree):
            indices = np.where(self.cut_tree)[0]
            for idx in sorted(indices, reverse=True):
                self.dyadic_distribution.insert(idx, 0)