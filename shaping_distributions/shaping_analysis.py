import matplotlib.pyplot as plt
import numpy as np
from Huffman_Code import HuffmanShaping, GeometricHuffmanCode
from HuffmanMatching.utils import GaussHermiteModulation, RandomWalkModulation, DiscretisedGaussianModulation
from HuffmanMatching import HuffmanTree
from scipy.stats import entropy

class results:
    def __init__(self):
        self.constellation_size = []
        self.distribution = []
        self.huffman_shaping = []
        self.kl_div_huffman_shaping = []
        self.geometric_huffman = []
        self.kl_div_geometric_huffman = []

def generate_shaping_results(start, stop, step, variance=1, modulation_class=None):
    """
    Gera resultados de shaping para a modulação escolhida.
    modulation_class: classe de modulação (ex: GaussHermiteModulation, RandomWalkModulation, DiscretisedGaussianModulation)
    """
    results_obj = results()
    for N in range(start, stop+1, step):
        results_obj.constellation_size.append(N)
        mod = modulation_class(N, var = variance)
        p = mod.probas
        s = mod.alphas
        results_obj.distribution.append(p)
        huffman_shaping = HuffmanTree(p, s)
        results_obj.huffman_shaping.append(huffman_shaping.true_distribution)
        results_obj.kl_div_huffman_shaping.append(huffman_shaping.kl_div)
        p_ghc = GeometricHuffmanCode(s, p).dyadic_distribution
        results_obj.geometric_huffman.append(p_ghc)
        epsilon = 1e-12
        kl_div_ghc = entropy(np.array(p), np.array(p_ghc) + epsilon, base=2)
        results_obj.kl_div_geometric_huffman.append(kl_div_ghc)
        
    return results_obj


def plot_distributions(results, title_prefix=''):

    for idx, N in enumerate(results.constellation_size):
        p_orig = np.array(results.distribution[idx])
        p_huff = np.array(results.huffman_shaping[idx])
        p_huff_geo = np.array(results.geometric_huffman[idx])

        plt.figure(figsize=(6,4))
        plt.plot(p_orig, 'o-', linewidth=2.5, label='Original', color='black')
        plt.plot(p_huff, 's--', linewidth=1.5, label='Huffman Shaping', color='tab:blue')
        plt.plot(p_huff_geo, 'd--', linewidth=1.5, label='Huffman Geometric', color='tab:orange')
        
        plt.title(f'{N}-' + title_prefix)
        plt.xlabel('Symbol index')
        plt.ylabel('Probability')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.tight_layout()
        plt.show()

def plot_kl_vs_constellation_size(results, title_prefix=''):
    x = results.constellation_size
    y_huff = results.kl_div_huffman_shaping
    y_geo = results.kl_div_geometric_huffman

    plt.figure(figsize=(7,4))
    plt.plot(x, y_huff, 'o-', label='Huffman Shaping')
    plt.plot(x, y_geo, 's--', label='Geometric Huffman')
    plt.xlabel('Constellation Size')
    plt.ylabel('KL Divergence')
    plt.title(f'KL Divergence for {title_prefix}')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()

def constellation_variance(symbols, probs=None):
    symbols = np.array(symbols, dtype=float)
    if probs is None:  # equiprovável
        probs = np.ones(len(symbols)) / len(symbols)
    else:
        probs = np.array(probs, dtype=float)

    variance = np.sum(probs * np.abs(symbols)**2)
    return variance