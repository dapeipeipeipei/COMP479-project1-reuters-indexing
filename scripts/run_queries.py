# Subproject II: run the 3 single-term and 3 AND sample queries on the naive index.
# Output: results/queries/s2_queries.txt

from pathlib import Path

from src.preprocessing import iter_documents
from src.naive_indexer import build_naive_index
from src.query_processor import single_term_query, and_query


def main():

    print("Building naive index...")

    index = build_naive_index(iter_documents())

    single_queries = [
        "cocoa",
        "bahia",
        "review"
    ]

    and_queries = [
        ["cocoa", "bahia"],
        ["cocoa", "review"],
        ["bahia", "review"]
    ]

    lines = []

    lines.append("S2 Query Results")
    lines.append("================")
    lines.append("")

    # Single-term queries
    lines.append("Single-term queries")
    lines.append("-------------------")

    for term in single_queries:

        result = single_term_query(index, term)

        lines.append(f"Query: {term}")
        lines.append(f"Number of results: {len(result)}")
        lines.append(f"DocIDs: {result}")
        lines.append("")

    # AND queries
    lines.append("AND queries")
    lines.append("-----------")

    for terms in and_queries:

        result = and_query(index, terms)

        query_text = " AND ".join(terms)

        lines.append(f"Query: {query_text}")
        lines.append(f"Number of results: {len(result)}")
        lines.append(f"DocIDs: {result}")
        lines.append("")

    result_text = "\n".join(lines)

    print(result_text)

    output_dir = Path("results/queries")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "s2_queries.txt"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(result_text)

    print(f"\nSaved to: {output_file}")


if __name__ == "__main__":
    main()