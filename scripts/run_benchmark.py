# Subproject IV (b): time the naive and SPIMI-inspired indexers on 10,000 term-docID pairings.
# Output: results/benchmark/spimi_benchmark.txt

from pathlib import Path

from src.preprocessing import iter_documents
from src.benchmark import limit_documents, benchmark_indexers


def main():

    print("Preparing 10,000 term-docID pairings...")

    documents = list(iter_documents())

    limited_documents = limit_documents(
        documents,
        10000
    )

    naive_time, spimi_time, speedup, same_index = benchmark_indexers(
        limited_documents,
        runs=20
    )

    result = (
        "Benchmark results (20 runs)\n"
        f"Average Naive time: {naive_time:.6f} seconds\n"
        f"Average SPIMI time: {spimi_time:.6f} seconds\n"
        f"SPIMI speedup: {speedup:.2f}x\n"
        f"Indexes identical: {same_index}\n"
    )

    print("\n" + result)

    output_dir = Path("results/benchmark")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "spimi_benchmark.txt"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(result)

    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    main()