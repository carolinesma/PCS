import matplotlib.pyplot as plt
import numpy as np
from Huffman_Code import HuffmanShaping, GeometricHuffmanCode, kl_divergence
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
        self.v_dist_huffman_shaping = []
        self.v_dist_geometric_huffman = []

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
        p_hs = huffman_shaping.true_distribution
        results_obj.huffman_shaping.append(p_hs)
        results_obj.kl_div_huffman_shaping.append(huffman_shaping.kl_div)
        results_obj.v_dist_huffman_shaping.append(
            variacional_distance_calculation(p, p_hs))
        
        p_ghc = GeometricHuffmanCode(s, p).dyadic_distribution
        results_obj.geometric_huffman.append(p_ghc)
        kl_div_ghc = entropy(np.array(p_ghc, dtype=float), np.array(p, dtype=float), base=2)
        results_obj.kl_div_geometric_huffman.append(kl_div_ghc)
        results_obj.v_dist_geometric_huffman.append(
            variacional_distance_calculation(p, p_ghc))
        
    return results_obj

def variacional_distance_calculation(t, t_approx):
    """
    Calcula a distância variacional entre duas distribuições.
    t: distribuição original
    t_approx: distribuição aproximada
    """
    t = np.array(t, dtype=float)
    t_approx = np.array(t_approx, dtype=float)
    return np.sum(np.abs(t - t_approx))

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

def plot_single_distribution(results, idx, title_prefix=''):
    """
    Plota as distribuições para uma posição específica do vetor de resultados.
    
    Parameters:
    -----------
    results : results object
        Objeto contendo os resultados do shaping
    idx : int
        Índice da posição específica a ser plotada (0-indexed)
    title_prefix : str
        Prefixo para o título do gráfico
    """
    if idx >= len(results.constellation_size) or idx < 0:
        print(f"Erro: Índice {idx} fora do range válido (0 a {len(results.constellation_size)-1})")
        return
    
    N = results.constellation_size[idx]
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

    plt.figure()
    plt.semilogy(x, y_huff, 'o-', label='Huffman Shaping', color="navy")
    plt.semilogy(x, y_geo, 's--', label='Geometric Huffman', color="darkolivegreen")
    plt.xlabel('Constellation Size')
    plt.ylabel('KL Divergence')
    #plt.title(f'KL Divergence for {title_prefix}')
    plt.grid(True, linestyle='-', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"kl_div_{title_prefix}.png", dpi=300, bbox_inches='tight')
    plt.show()

def plot_v_dist_constellation_size(results, title_prefix=''):
    x = results.constellation_size
    y_huff = results.v_dist_huffman_shaping
    y_geo = results.v_dist_geometric_huffman

    plt.figure()
    plt.semilogy(x, y_huff, 'o-', label='Huffman Shaping', color="navy")
    plt.semilogy(x, y_geo, 's--', label='Geometric Huffman', color="darkolivegreen")
    plt.xlabel('Constellation Size')
    plt.ylabel('Variational Distance')
    #plt.title(f'Variational Distance for {title_prefix}')
    plt.grid(True, linestyle='-', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"v_dist_{title_prefix}.png", dpi=300, bbox_inches='tight')
    plt.show()


def plot_kl_vs_constellation_size_two_distributions(results_binomial, results_gaussian):
    x_bin = results_binomial.constellation_size
    y_huff_bin = results_binomial.kl_div_huffman_shaping
    y_geo_bin = results_binomial.kl_div_geometric_huffman

    x_gau = results_gaussian.constellation_size
    y_huff_gau = results_gaussian.kl_div_huffman_shaping
    y_geo_gau = results_gaussian.kl_div_geometric_huffman

    plt.figure()

    # Distribuição Binomial
    plt.semilogy(x_bin, y_huff_bin, 'o-', label='Binomial - Huffman Shaping', color='navy')
    plt.semilogy(x_bin, y_geo_bin, 's--', label='Binomial - Geometric Huffman', color='darkolivegreen')

    # Distribuição Gaussian Hermite
    plt.semilogy(x_gau, y_huff_gau, 'd-', label='Gaussian Hermite - Huffman Shaping', color='mediumorchid')
    plt.semilogy(x_gau, y_geo_gau, 'x--', label='Gaussian Hermite - Geometric Huffman', color='crimson')

    plt.xlabel('Constellation Size')
    plt.ylabel('KL Divergence')
    plt.grid(True, linestyle='-', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig("kl_div_two_distributions.png", dpi=300, bbox_inches='tight')
    plt.show()

def plot_v_dist_two_distributions(results_binomial, results_gaussian):
    x_bin = results_binomial.constellation_size
    y_huff_bin = results_binomial.v_dist_huffman_shaping
    y_geo_bin = results_binomial.v_dist_geometric_huffman

    x_gau = results_gaussian.constellation_size
    y_huff_gau = results_gaussian.v_dist_huffman_shaping
    y_geo_gau = results_gaussian.v_dist_geometric_huffman

    plt.figure()

    # Distribuição Binomial
    plt.semilogy(x_bin, y_huff_bin, 'o-', label='Binomial - Huffman Shaping', color='navy')
    plt.semilogy(x_bin, y_geo_bin, 's--', label='Binomial - Geometric Huffman', color='darkolivegreen')

    # Distribuição Gaussian Hermite
    plt.semilogy(x_gau, y_huff_gau, 'd-', label='Gaussian Hermite - Huffman Shaping', color='mediumorchid')
    plt.semilogy(x_gau, y_geo_gau, 'x--', label='Gaussian Hermite - Geometric Huffman', color='crimson')

    plt.xlabel('Constellation Size')
    plt.ylabel('Variational Distance')
    plt.grid(True, linestyle='-', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig("v_dist_two_distributions.png", dpi=300, bbox_inches='tight')
    plt.show()

def constellation_variance(symbols, probs=None):
    symbols = np.array(symbols, dtype=float)
    if probs is None:  # equiprovável
        probs = np.ones(len(symbols)) / len(symbols)
    else:
        probs = np.array(probs, dtype=float)

    variance = np.sum(probs * np.abs(symbols)**2)
    return variance