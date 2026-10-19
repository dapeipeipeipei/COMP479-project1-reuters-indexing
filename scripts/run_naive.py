from src.preprocessing import iter_documents
from src.naive_indexer import build_naive_index


def main():
    print("Building Naive index...")

    index = build_naive_index(iter_documents())

    print(f"Number of terms: {len(index)}")

    print(f"cocoa: {index.get('cocoa', [])}")
    print(f"bahia: {index.get('bahia', [])}")
    print(f"review: {index.get('review', [])}")


if __name__ == "__main__":
    main()