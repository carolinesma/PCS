import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

def plot_qam_constellation_3d(iq_symbols, probabilities):
    """
    Plots a 3D bar graph of a probabilistic QAM constellation.

    Parameters:
    - iq_symbols: np.ndarray, array of complex QAM symbols.
    - probabilities: np.ndarray, array of integer probabilities (counts).
    """
    # Extraindo coordenadas
    x = np.real(iq_symbols)
    y = np.imag(iq_symbols)
    z = np.zeros_like(x)  # Base do gráfico de barras
    dz = probabilities  # Altura das barras

    # Normalizar as probabilidades para um colormap
    norm_probs = (dz - dz.min()) / (dz.max() - dz.min() + 1e-6)  # Evita divisão por zero
    colors = plt.cm.viridis(norm_probs)  # Usando o colormap 'viridis'

    # Criando a figura 3D
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Plotando as barras 3D
    ax.bar3d(x, y, z, dx=0.15, dy=0.15, dz=dz, color=colors, shade=True)

    # Configurações do gráfico
    ax.set_xlabel("In-Phase (I)")
    ax.set_ylabel("Quadrature (Q)")
    ax.set_zlabel("Probability")
    ax.set_title("Probabilistic QAM Constellation")

    plt.tight_layout()

    plt.show()

def plot_pmf_gaussiana(iq_symbols, probabilities, variancia, mu):
    """
    Plota o gráfico de barras 1D dos símbolos complexos junto com a gaussiana para a mesma variância.

    """
    # Calcula a Gaussiana com a variância fornecida
    sigma = np.sqrt(variancia)
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 200)
    # Calcule a PDF da Gaussiana
    y = norm.pdf(x, mu, sigma)

     # Extraindo a parte imaginária dos símbolos QAM
    phase = np.real(iq_symbols)

    # Ajuste da escala da Gaussiana
    y_scaled = y * (np.max(probabilities) / np.max(y))
    
    plt.figure(figsize=(8, 4))
    plt.bar(phase, probabilities, width=0.1, color='purple', alpha=0.8, label='Probabilidade dos Símbolos')
    #plt.stem(phase, probabilities, basefmt=" ", label='PMF dos Símbolos')
    plt.plot(x, y_scaled, label=f'Gaussiana ($\mu$={mu}, $\sigma^2$={variancia:.4f})')
    plt.xlabel("Fase (I)")
    plt.ylabel("Probabilidade")
    plt.title("Histograma de Fase com Gaussiana Ajustada")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()