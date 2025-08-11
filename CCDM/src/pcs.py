import ccdm, modulation
import numpy as np
import math
import logging

def n_choose_ks_recursive_log2(n, k):
    """
    Computes log2(n! / product(k_i!)) using iterative binomial coefficients.

    Parameters
    ----------
    n : int
        Total number of items.
    k : list[int]
        List of counts for each symbol.

    Returns
    -------
    float
        Log base-2 of the multinomial coefficient.
    """
    out = 0
    #k_sorted = sorted(k)
    k_sorted = k

    for i in range(len(k_sorted) - 1):
        out += n_choose_k_iter_log(n, k_sorted[i])
        n -= k_sorted[i]
    return out

def n_choose_k_iter_log(n, k):
    """
    Computes log2 of binomial coefficient "n choose k".

    Parameters
    ----------
    n : int
        Total number of items.
    k : int
        Number of items chosen.

    Returns
    -------
    float
        log2(n choose k)
    """
    i = np.arange(1, k + 1)
    out = np.sum(np.log2((n - (k - i)) / i))
    
    return out

def initialize(p, n):
    """
    Initializes CCDM quantization given a probability vector and sequence length.

    Parameters
    ----------
    p : array-like
        Target symbol probabilities.
    n : int
        Length of output sequence.

    Returns
    -------
    p_quant : np.ndarray
        Quantized probability distribution.
    num_info_bits : int
        Maximum number of input bits.
    n_i : np.ndarray
        Absolute symbol frequencies.
    """
    n_i, p_quant = idquant(p, n)
    num_info_bits = math.floor(n_choose_ks_recursive_log2(n, n_i))

    return p_quant, num_info_bits, n_i


def idquant(p, n):
    """
    Performs type quantization of a probability vector.

    Parameters
    ----------
    p : array-like
        Target symbol probabilities.
    n : int
        Length of output sequence.

    Returns
    -------
    n_i : np.ndarray
        Absolute counts approximating the input distribution.
    p_quant : np.ndarray
        Quantized distribution.
    """
    m = len(p)
    t = np.zeros(m)
    n_i = np.zeros(m, dtype=int)  
    for i, p_value in enumerate(p):
        if p_value != 0:
            t[i] = np.log(1.0 / p_value)
        else: t[i] = np.inf
    p_quant = t.copy()  

    for k in range(n):
        index = np.argmin(p_quant)  
        cj = n_i[index] + 1
        n_i[index] = cj
        p_quant[index] = (cj + 1) * np.log(cj + 1) - cj * np.log(cj) + t[index]

    p_quant = n_i / n  
    return n_i, p_quant


def probabilistic_shaping_encode(bit_sequence, config):
    """
    Encodes a bit sequence using Constant Composition Distribution Matching (CCDM).

    Parameters
    ----------
    bit_sequence : list
        Input bits to encode.
    config : ModulationConfig
        Configuration containing constellation and symbol frequency.

    Returns
    -------
    tuple[np.array, list]
        Modulated signal (IQ symbols) and the index list of symbols.
    """
    #C = config["pcs_IQmap"]
    C = np.unique(np.abs(config["pcs_IQmap"]))
    n_i = config["pcs_symFreq"]
    bits_sinal_i = np.random.randint(0, 2, config["pcs_num_symbols"])
    bits_sinal_q = np.random.randint(0, 2, config["pcs_num_symbols"])
    
    bit_sequence_i, bit_sequence_q = np.array_split(bit_sequence, 2)

    i_TX = ccdm.encode(bit_sequence_i, n_i)
    q_TX = ccdm.encode(bit_sequence_q, n_i)
    i_TX_aux = np.array(i_TX) - 1
    q_TX_aux = np.array(q_TX) - 1
    I = C[i_TX_aux] * (1 - 2*bits_sinal_i) 
    Q = C[q_TX_aux] * (1 - 2*bits_sinal_q) * 1j
    txSyms = {"I": i_TX, "Q": q_TX}
    IQ = I+Q
    #Stx = IQ

    return IQ, txSyms

def probabilistic_shaping_config(config):
    """
    Computes the distribution and symbol frequencies for probabilistic shaping using CCDM.

    Parameters
    ----------
    config : ModulationConfig
        Configuration object to be updated in-place.
    """

    constelattion_unity = modulation.normalize_power(modulation.gray_mapping(config))
    lambda_param = config["lambda_param"]
    amplitudes = np.unique(np.abs(constelattion_unity))
    # maxwell-boltzman
    pOpt = np.exp(-lambda_param * amplitudes * (np.sqrt(config["constellation_size"]) - 1) / (np.sqrt(2) / 2))
    pOpt /= np.sum(pOpt)
    config["pcs_pOpt"] = pOpt
    config["pcs_IQmap"] = constelattion_unity
    
    p_quant, nBitsInfo, n_i = initialize(pOpt, config["pcs_num_symbols"])
    config["num_bits"] = nBitsInfo
    config["pcs_symFreq"] = n_i 
    config["pcs_symProb"] = p_quant

    return config