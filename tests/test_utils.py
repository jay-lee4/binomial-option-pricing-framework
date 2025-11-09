import pytest
from src.utils import n_choose_k

def test_n_choose_k_base_cases():
    assert n_choose_k(5, 0) == 1
    assert n_choose_k(5, 5) == 1
    assert n_choose_k(1, 1) == 1
    assert n_choose_k(1, 0) == 1

def test_n_choose_k_common_cases():
    assert n_choose_k(5, 2) == 10
    assert n_choose_k(4, 2) == 6
    assert n_choose_k(10, 3) == 120
    assert n_choose_k(10, 7) == 120 # nCk == nC(n-k)

def test_n_choose_k_edge_cases():
    assert n_choose_k(0, 0) == 1
    assert n_choose_k(5, -1) == 0
    assert n_choose_k(5, 6) == 0
