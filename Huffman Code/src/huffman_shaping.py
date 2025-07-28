from typing import Dict, Optional, List, Tuple
from utils import OrderedQueue, Node
from huffman_code import HuffmanTree
import copy

class HuffmanShaping:
    def __init__(self, symbols, frequencies, suffixes: List[str] = None):
        self.huffman_tree = HuffmanTree(symbols, frequencies)
        self.suffixes = suffixes or ['00', '01', '10', '11']
        self.expanded_codebook = []
        self._inverse_codebook = None
        self._expand_codebook()
    
    def get_inverse_codebook(self):
        if self._inverse_codebook is None:
            self._inverse_codebook = {node.code: node.symbol for node in self.expanded_codebook}
        return self._inverse_codebook
    
    def _expand_codebook(self):
        base_codebook = self.huffman_tree.get_codebook()
        N = len(base_codebook)
        
        for node in base_codebook:
            for i, suffix in enumerate(self.suffixes):
                new_symbol = node.symbol + i * N
                new_code = node.code + suffix
                new_node = copy.deepcopy(node)
                new_node.symbol = new_symbol
                new_node.code = new_code
                self.expanded_codebook.append(new_node)
    
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
    
    def decode_base(self, bitstream):
        return self.huffman_tree.decode_with_codebook(bitstream)
    
    def get_tree_root(self):
        return self.huffman_tree.root
    
    def is_prefix_free(self):
        return self.huffman_tree.is_prefix_free(self.expanded_codebook)