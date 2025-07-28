from utils import OrderedQueue, Node

class HuffmanTree:
    def __init__(self, symbols, frequencies):
        self.root = self._build_tree(symbols, frequencies)
        self.codebook = []
        self._inverse_codebook = None
        self._generate_codes(self.root, "")
        
    def _build_tree(self, symbols, frequencies):
        queue = OrderedQueue()
        for symbol, freq in zip(symbols, frequencies):
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
    
    def get_inverse_codebook(self):
        if self._inverse_codebook is None:
            self._inverse_codebook = {node.code: node.symbol for node in self.codebook}
        return self._inverse_codebook
    
    def decode(self, bitstream):
        decoded_symbols = []
        node = self.root

        for bit in bitstream:
            if bit == '1':
                node = node.left
            elif bit == '0':
                node = node.right
            else:
                raise ValueError(f"Invalid bit: {bit}")

            if node.is_leaf():
                decoded_symbols.append(node.symbol)
                node = self.root

        return decoded_symbols

    def decode_with_codebook(self, bitstream):
        inverse_codebook = self.get_inverse_codebook()
        decoded = []
        buffer = ""

        for bit in bitstream:
            buffer += bit
            if buffer in inverse_codebook:
                decoded.append(inverse_codebook[buffer])
                buffer = ""

        if buffer != "":
            raise ValueError(f"Invalid bitstream: unrecognized suffix '{buffer}' remaining after decoding")

        return decoded
    
    def is_prefix_free(self, codebook):
        codes = [entry.code for entry in codebook]
        for i, code1 in enumerate(codes):
            for j, code2 in enumerate(codes):
                if i != j and code2.startswith(code1):
                    return False, code1, code2
        return True, None, None