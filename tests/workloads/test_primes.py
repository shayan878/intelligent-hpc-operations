from intelligent_hpc_operations.workloads.primes import (
    count_primes_in_range,
    is_prime,
    partition_range,
    primes_in_range,
)


def test_is_prime_handles_small_and_composite_values():
    assert not is_prime(-5)
    assert not is_prime(0)
    assert not is_prime(1)
    assert is_prime(2)
    assert is_prime(3)
    assert not is_prime(4)
    assert is_prime(97)
    assert not is_prime(121)


def test_primes_in_range_is_half_open():
    assert primes_in_range(1, 12) == [2, 3, 5, 7, 11]
    assert primes_in_range(11, 12) == [11]
    assert primes_in_range(12, 12) == []


def test_partition_range_is_balanced_and_disjoint():
    ranges = [partition_range(1, 11, rank, 3) for rank in range(3)]
    assert ranges == [(1, 5), (5, 8), (8, 11)]
    combined = [value for start, end in ranges for value in range(start, end)]
    assert combined == list(range(1, 11))


def test_partition_range_validation():
    import pytest

    with pytest.raises(ValueError):
        partition_range(10, 1, 0, 2)
    with pytest.raises(ValueError):
        partition_range(1, 10, 2, 2)
    with pytest.raises(ValueError):
        partition_range(1, 10, 0, 0)


def test_count_primes_in_range_matches_list():
    assert count_primes_in_range(1, 100) == len(primes_in_range(1, 100))
