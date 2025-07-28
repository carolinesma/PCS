import numpy as np

def entropy(p):
    """ Calcula a entropia de uma distribuição de probabilidade.
        Equação: H(p) = -Σ p_i * log2(p_i)
    Parâmetros:
    p : np.array
        Distribuição de probabilidade dos símbolos.
    Retorna:
    float
        Entropia da distribuição de probabilidade.
    """
    return -np.sum(p * np.log2(p + 1e-12))  # adiciona termo pequeno p evitar log(0)

# Cálculo da energia média do símbolo
def average_energy(p, A_M):
    """ Calcula a energia média de um símbolo.
        Equação: E = Σ p_i * |A_i|^2
    Parâmetros:
    p : np.array
        Distribuição de probabilidade dos símbolos.
    A_M : np.array
        Valores dos símbolos (constelação).
    Retorna:
    float
        Energia média do símbolo.
    """
    return np.sum(p * np.abs(A_M)**2)

def PAM(M):
    A = []
    for i in range(0, M):
        A_i = -(M-1) + 2*i
        A.append(A_i)
    return A

def average_code_rate(M, K, L):
    """
    Calcula a taxa média de codificação.
    
    M: número de símbolos
    K: número de bits por símbolo
    L: lista de comprimentos dos códigos para cada símbolo
    """
    return sum(2**(-L[i]) * L[i] for i in range(M)) / K

def standard_deviation_rate(M, K, L, R_h):
    """
    Calcula o desvio padrão da taxa de codificação.
    
    M: número de símbolos
    K: número de bits por símbolo
    L: lista de comprimentos dos códigos para cada símbolo
    R_h: taxa média de codificação
    """
    return np.sqrt(sum(2**(-L[i]) * (L[i] - K*R_h)**2 for i in range(M)) / K)

def average_energy_dimension(A_M, L, K):
    """
    Calcula a dimensão de energia.
    
    A_M: constelação
    L: lista de comprimentos dos códigos para cada símbolo
    K: número de bits por símbolo
    """
    return sum(2**(-L[i]) * np.abs(A_M[i])**2 for i in range(len(A_M))) / K

def shaping_gain(R_h, E_h):
    """
    Calcula o ganho de shaping.
    
    R_h: taxa média de codificação
    E_h: energia média do código
    """
    return ((2**(2*R_h)) - 1) / (3 * E_h)