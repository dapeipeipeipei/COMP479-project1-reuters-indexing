"""Run the challenge queries, save results and timings to results/challenge/."""

import sys
import time
from pathlib import Path

from src.preprocessing import iter_documents
from src.naive_indexer import build_naive_index
from src.spimi_indexer import build_spimi_index
from src.query_processor import single_term_query, and_query


QUERIES = [
    "Carmark",
    "copper",
    "Chrysler and Bundesbank",
]

REPETITIONS = 10000


# Split a query string into operands; "and" is the Boolean operator.
def parse_query(query):
    return [word for word in query.split() if word.lower() != "and"]


def run_query(index, terms):
    if len(terms) == 1:
        return single_term_query(index, terms[0])
    return and_query(index, terms)


# Independent check: scan every (doc_id, tokens) document directly.
def scan_documents(documents, terms):
    normalized = [term.lower() for term in terms]
    result = []

    for doc_id, tokens in documents:
        token_set = set(tokens)
        if all(term in token_set for term in normalized):
            result.append(doc_id)

    return sorted(result)


def is_sorted_unique(doc_ids):
    return all(a < b for a, b in zip(doc_ids, doc_ids[1:]))


# Average time of one query call over many repetitions, in microseconds.
def time_query(index, terms, repetitions):
    start = time.perf_counter()
    for _ in range(repetitions):
        run_query(index, terms)
    elapsed = time.perf_counter() - start
    return elapsed / repetitions * 1_000_000


def main():
    errors = []

    # A. Corpus parsing / tokenization
    print("Reading and tokenizing Reuters-21578...")
    start = time.perf_counter()
    documents = list(iter_documents())
    preprocessing_time = time.perf_counter() - start

    # B. Index construction
    print("Building Naive index...")
    start = time.perf_counter()
    naive_index = build_naive_index(documents)
    naive_build_time = time.perf_counter() - start

    print("Building SPIMI index...")
    start = time.perf_counter()
    spimi_index = build_spimi_index(documents)
    spimi_build_time = time.perf_counter() - start

    indexes_identical = naive_index == spimi_index
    if not indexes_identical:
        errors.append("Full Naive and SPIMI indexes are not identical")

    # Query results and correctness checks
    result_lines = [
        "COMP 479/6791 Project 1 - 24-hour Challenge Results",
        "===================================================",
        "",
        f"Documents indexed: {len(documents)}",
        "Query terms are lowercased by single_term_query(); "
        "'and' is treated as the Boolean AND operator.",
        "",
    ]

    parsed_queries = []

    for number, query in enumerate(QUERIES, start=1):
        terms = parse_query(query)
        parsed_queries.append((query, terms))

        naive_result = run_query(naive_index, terms)
        spimi_result = run_query(spimi_index, terms)
        scan_result = scan_documents(documents, terms)

        same_result = naive_result == spimi_result
        naive_matches_scan = naive_result == scan_result
        spimi_matches_scan = spimi_result == scan_result
        naive_ordered = is_sorted_unique(naive_result)
        spimi_ordered = is_sorted_unique(spimi_result)

        if not same_result:
            errors.append(f"{query!r}: Naive and SPIMI results differ")
        if not naive_matches_scan:
            errors.append(f"{query!r}: Naive result differs from document scan")
        if not spimi_matches_scan:
            errors.append(f"{query!r}: SPIMI result differs from document scan")
        if not naive_ordered:
            errors.append(f"{query!r}: Naive docIDs not sorted/unique")
        if not spimi_ordered:
            errors.append(f"{query!r}: SPIMI docIDs not sorted/unique")

        result_lines.append(f"Query {number}: {query}")
        result_lines.append(f"Parsed terms: {terms}")
        result_lines.append(f"Naive results: {len(naive_result)}")
        result_lines.append(f"Naive DocIDs: {naive_result}")
        result_lines.append(f"SPIMI results: {len(spimi_result)}")
        result_lines.append(f"SPIMI DocIDs: {spimi_result}")
        result_lines.append(f"Naive and SPIMI identical: {same_result}")
        result_lines.append(f"DocIDs sorted and unique: Naive={naive_ordered}, SPIMI={spimi_ordered}")
        result_lines.append(f"Document scan results: {len(scan_result)}")
        if not (naive_matches_scan and spimi_matches_scan):
            result_lines.append(f"Document scan DocIDs: {scan_result}")
        result_lines.append(
            f"Match independent document scan: "
            f"Naive={naive_matches_scan}, SPIMI={spimi_matches_scan}"
        )
        result_lines.append("")

    result_lines.append(f"Full Naive and SPIMI indexes identical: {indexes_identical}")
    result_lines.append("")
    if errors:
        result_lines.append("CORRECTNESS CHECKS FAILED:")
        result_lines.extend(f"- {error}" for error in errors)
    else:
        result_lines.append("All correctness checks passed.")

    # C. Query execution time (query functions only)
    query_timings = []
    for query, terms in parsed_queries:
        naive_us = time_query(naive_index, terms, REPETITIONS)
        spimi_us = time_query(spimi_index, terms, REPETITIONS)
        query_timings.append((query, naive_us, spimi_us))

    timing_lines = [
        "COMP 479/6791 Project 1 - 24-hour Challenge Timings",
        "===================================================",
        "",
        f"Documents: {len(documents)}",
        f"Corpus preprocessing time (parse + tokenize, shared): {preprocessing_time:.3f} s",
        f"Naive index construction time: {naive_build_time:.3f} s",
        f"SPIMI index construction time: {spimi_build_time:.3f} s",
        f"Naive terms: {len(naive_index)}",
        f"SPIMI terms: {len(spimi_index)}",
        f"Full Naive and SPIMI indexes identical: {indexes_identical}",
        "",
        "Query timing method: time.perf_counter() around a loop of repeated calls",
        "to single_term_query() / and_query() on the already-built index;",
        "excludes index construction, document scanning, validation and file writes.",
        f"Repetitions per query and index: {REPETITIONS}",
        "",
        "Average query time (microseconds per query)",
        "-------------------------------------------",
    ]
    for query, naive_us, spimi_us in query_timings:
        timing_lines.append(f"{query}: Naive {naive_us:.3f} us, SPIMI {spimi_us:.3f} us")

    result_text = "\n".join(result_lines)
    timing_text = "\n".join(timing_lines)

    print("\n" + result_text)
    print("\n" + timing_text)

    output_dir = Path("results/challenge")
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / "challenge_results.txt", "w", encoding="utf-8") as file:
        file.write(result_text + "\n")
    with open(output_dir / "challenge_timings.txt", "w", encoding="utf-8") as file:
        file.write(timing_text + "\n")

    print(f"\nSaved to: {output_dir}")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
