from typing import Dict, Optional, List, Tuple
from .utils import OrderedQueue, Node
from .huffman_code import HuffmanTree
import copy
import warnings
import numpy as np # type: ignore

class HuffmanShaping:
    def __init__(self, symbols, distribution, suffixes: List[str] = None):
        self.huffman_tree = HuffmanTree(symbols, distribution)
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
                new_node = copy.deepcopy(node)
                new_node.symbol = new_symbol
                new_node.code = node.code + suffix
                new_node.L = len(new_node.code)
                new_node.frequency = pow(2,-new_node.L)
                self.expanded_codebook.append(new_node)
    
    def encode(self, bitstream):
        if not self.is_prefix_free():
            return
        if isinstance(bitstream, (np.ndarray, list, tuple)):
            bitstream = ''.join(bitstream.astype(str)) if isinstance(bitstream, np.ndarray) else ''.join(str(int(b)) for b in bitstream)
        
        inverse_codebook = self.get_inverse_codebook()
        encoded = []
        buffer = ""
        for bit in bitstream:
            buffer += bit
            if buffer in inverse_codebook:
                encoded.append(inverse_codebook[buffer])
                buffer = ""
        if buffer != "":
            warnings.warn(f"'{buffer}' (not decodable)", stacklevel=1)
            
        return encoded, len(buffer)

    def decode(self, symbols):
        bitstring = ''.join([self.expanded_codebook[i].code for i in symbols])
        return np.array(list(bitstring), dtype=int)
        
    def print_codebook(self):
        self.huffman_tree.print_codebook(self.expanded_codebook)

    def decode_base(self, bitstream):
        return self.huffman_tree.decode_with_codebook(bitstream)
    
    def get_tree_root(self):
        return self.huffman_tree.root
    
    def is_prefix_free(self):
        return self.huffman_tree.is_prefix_free(self.expanded_codebook)
    
    def get_output_distribution(self):
        N = len(self.huffman_tree.get_codebook())
        first_quadrant_frequencies = [node.frequency for node in self.expanded_codebook[:N]]
        return np.array(first_quadrant_frequencies)