"""Prime-number workload that partitions a half-open range across Slurm task ranks."""

from __future__ import annotations

import argparse
import json
import math
import os


def is_prime(number: int) -> bool:
    """Return whether number is prime using trial division up to its square root."""
    if number < 2:
        return False
    if number in {2, 3}:
        return True
    if number % 2 == 0 or number % 3 == 0:
        return False
    divisor = 5
    limit = math.isqrt(number)
    while divisor <= limit:
        if number % divisor == 0 or number % (divisor + 2) == 0:
            return False
        divisor += 6
    return True


def partition_range(start: int, end: int, rank: int, world_size: int) -> tuple[int, int]:
    """Split [start, end) into balanced, non-overlapping ranges."""
    if end < start:
        raise ValueError("end must be greater than or equal to start")
    if world_size < 1:
        raise ValueError("world_size must be at least 1")
    if rank < 0 or rank >= world_size:
        raise ValueError("rank must be in [0, world_size)")

    total = end - start
    base, remainder = divmod(total, world_size)
    local_start = start + rank * base + min(rank, remainder)
    local_length = base + (1 if rank < remainder else 0)
    return local_start, local_start + local_length


def primes_in_range(start: int, end: int) -> list[int]:
    """Return all primes in the half-open interval [start, end)."""
    if end < start:
        raise ValueError("end must be greater than or equal to start")
    return [value for value in range(max(2, start), end) if is_prime(value)]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", type=int, default=1, help="Inclusive range start")
    parser.add_argument("--end", type=int, default=1000, help="Exclusive range end")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.end < args.start:
        raise SystemExit("--end must be greater than or equal to --start")

    rank = int(os.getenv("SLURM_PROCID", "0"))
    world_size = int(os.getenv("SLURM_NTASKS", "1"))
    local_start, local_end = partition_range(args.start, args.end, rank, world_size)
    found = primes_in_range(local_start, local_end)
    result = {
        "rank": rank,
        "world_size": world_size,
        "range_start": local_start,
        "range_end_exclusive": local_end,
        "prime_count": len(found),
        "primes": found,
    }
    print(json.dumps(result, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
