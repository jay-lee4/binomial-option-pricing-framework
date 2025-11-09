import math

def n_choose_k(n: int, k: int) -> int:
    """
    Calculates nCk (n choose k).
    """
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    if k > n // 2:
        k = n - k

    return math.comb(n, k)
