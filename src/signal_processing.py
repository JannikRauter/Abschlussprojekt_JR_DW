import numpy as np

def moving_average(arr: np.ndarray, window_size: int = 15) -> np.ndarray:
    """
    Glättet ein 1D-NumPy-Array mithilfe eines gleitenden Mittelwerts (Moving Average).

    Parameter:
    arr : np.ndarray
        Das zu glättende Array
    window_size : int
        Die Breite des Filterfensters
        
    Return:
    np.ndarray
        Das gefilterte Array mit derselben Länge wie das Eingangsarray
    """
    if len(arr) < window_size:
        return arr
        
    # Berechnet den gleitenden Mittelwert
    return np.convolve(arr, np.ones(window_size) / window_size, mode='same')