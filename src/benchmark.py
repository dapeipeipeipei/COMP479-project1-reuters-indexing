"""
Timing of the naive indexer vs the SPIMI-inspired indexer.

Both indexers are timed on the same input, stopping after the first
10,000 term-docID pairs.
"""

import time
from statistics import mean

from src.naive_indexer import build_naive_index
from src.spimi_indexer import build_spimi_index




def limit_documents(documents, limit):
    limited_documents = []
    count = 0

    for doc_id, tokens in documents:
        remaining = limit - count

        if remaining <= 0:
            break

        selected_tokens = tokens[:remaining]

        limited_documents.append(
            (doc_id, selected_tokens)
        )

        count += len(selected_tokens)

    return limited_documents


def benchmark_indexers(documents, runs=20):

    naive_times = []
    spimi_times = []

    same_index = True

    for _ in range(runs):

        # Naive
        start = time.perf_counter()

        naive_index = build_naive_index(documents)

        naive_time = time.perf_counter() - start

        naive_times.append(naive_time)


        # SPIMI
        start = time.perf_counter()

        spimi_index = build_spimi_index(documents)

        spimi_time = time.perf_counter() - start

        spimi_times.append(spimi_time)


        if naive_index != spimi_index:
            same_index = False


    average_naive = mean(naive_times)
    average_spimi = mean(spimi_times)

    speedup = average_naive / average_spimi

    return (
        average_naive,
        average_spimi,
        speedup,
        same_index
    )