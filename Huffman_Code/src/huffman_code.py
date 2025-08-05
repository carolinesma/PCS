from .utils import OrderedQueue, Node
import warnings

class HuffmanTree:
    def __init__(self, symbols, distribution):
        self.root = self._build_tree(symbols, distribution)
        self.codebook = []
        self._inverse_codebook = None
        self._generate_codes(self.root, "")
        
    def _build_tree(self, symbols, distribution):
        queue = OrderedQueue()
        for symbol, freq in zip(symbols, distribution):
            queue.insert_sorted(Node(freq, symbol))

        while len(queue) >= 2:
            left = queue.pop()
            right = queue.pop()
            merged = Node(left.frequency + right.frequency)
            merged.left = left
            merged.right = right
            queue.insert_sorted(merged)

        return queue.pop()

    def _generate_codes(self, node, codeword):
        if node is None:
            return
        if node.is_leaf():
            node.code = codeword
            node.L = len(codeword)
            self.codebook.append(node)  # Armazena na lista
        else:
            self._generate_codes(node.left, codeword + "1")
            self._generate_codes(node.right, codeword + "0")

    def get_codebook(self):
        return self.codebook
        
    def encode(self, bitstream):
        encoded_symbols = []
        node = self.root

        for bit in bitstream:
            if bit == 1:
                node = node.left
            elif bit == 0:
                node = node.right
            else:
                raise ValueError(f"Invalid bit: {bit}")

            if node.is_leaf():
                encoded_symbols.append(node.symbol)
                node = self.root

        return encoded_symbols
    
    def print_codebook(self, codebook=None):
        if codebook is None:
            codebook = self.codebook
        codebook.sort(key=lambda node: node.symbol)
        for c in codebook:
            print(f"{c.symbol} | {c.frequency:.5f} | {c.code}")

    def is_prefix_free(self, codebook):
        codes = [entry.code for entry in codebook]
        for i, code1 in enumerate(codes):
            for j, code2 in enumerate(codes):
                if i != j and code2.startswith(code1):
                    warnings.warn(f"The code '{code1}' is a prefix of '{code2}', so it is not prefix-free.")
                    return False, code1, code2
        return True, None, None