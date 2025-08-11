import numpy as np
import logging

def generate_qam_constellation(M):
        """
        Generates a square Quadrature Amplitude Modulation (QAM) constellation.

        Parameters
        ----------
        M : int
            Modulation order. Must be a perfect square.

        Returns
        -------
        np.array
            QAM constellation as complex values.
        """
        side_length = int(np.sqrt(M) - 1)

        # generate 1D PAM constellation
        one_d_constellation = np.arange(-side_length, side_length + 1, 2)
        one_d_constellation = np.array([one_d_constellation])

        # generate complex square M-QAM constellation
        constellation = np.tile(one_d_constellation, (side_length + 1, 1))
        constellation = constellation + 1j * np.flipud(constellation.T)

        for idx in np.arange(1, side_length + 1, 2):
            constellation[idx] = np.flip(constellation[idx], 0)

        return constellation

def generate_pam_constellation(M):
        """
        Generates a Pulse Amplitude Modulation (PAM) constellation.

        Parameters
        ----------
        M : int
            Modulation order (number of symbols).

        Returns
        -------
        np.array
            PAM constellation values (real).
        """
        return np.arange(-int(M - 1), int(M - 1) + 1, 2)

def gray_mapping(config, M = None, modulation_type = None):
        """
        Generates Gray-coded constellation for the specified modulation type.

        Parameters
        ----------
        config : ModulationConfig
            Modulation configuration parameters.

        Returns
        -------
        np.array
            Complex or real constellation symbols ordered by Gray code.
        """

        if M == None:
            M = config["constellation_size"]
        if modulation_type == None:
            modulation_type = "pam"

        bits_per_symbol = int(np.log2(M))
        gray_code = generate_gray_code(bits_per_symbol)
        constellation = generate_pam_constellation(M)

        constellation = constellation.reshape(M, 1)
        sorted_constellation = np.zeros((M, 2), dtype=complex)

        for idx in range(M):
            sorted_constellation[idx, 0] = constellation[idx, 0]  # complex constellation symbol
            sorted_constellation[idx, 1] = int(gray_code[idx], 2)  # mapped bit sequence (as integer decimal)

        # sort complex symbols column according to their mapped bit sequence (as integer decimal)
        constellation = sorted_constellation[sorted_constellation[:, 1].real.argsort()]
        constellation = constellation[:, 0]

        if modulation_type in ["pam", "ook"]:
            constellation = constellation.real

        return constellation

def generate_gray_code(n):
        """
        Generates Gray code of length 2^n.

        Parameters
        ----------
        n : int
            Number of bits per symbol.

        Returns
        -------
        list[str]
            Binary Gray code strings.
        """
        gray_code = []

        for i in range(1 << n):
            value = i ^ (i >> 1)
            s = bin(value)[2::]
            gray_code.append(s.zfill(n))
        return gray_code

def normalize_power(signal):
    """
    Normalizes the average power of the input signal to 1.

    Parameters
    ----------
    signal : np.array
        Complex or real-valued input signal.

    Returns
    -------
    np.array
        Signal with normalized average power (per component).
    """
    power = np.mean(signal * np.conj(signal)).real
    return signal / np.sqrt(power)