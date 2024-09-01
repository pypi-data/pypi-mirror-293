import xxhash


def generate_unique_hash(ids: list[int]) -> str:
    return xxhash.xxh128(''.join(map(str, ids)).encode()).hexdigest()
