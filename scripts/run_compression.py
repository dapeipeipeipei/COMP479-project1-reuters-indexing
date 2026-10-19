from src.compression import run_compression_experiment
from pathlib import Path


def main():
    results = run_compression_experiment()

    output_dir = Path("experiments/compression")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "compression_table.tsv"

    lines = []

    header = (
        "Stage\tTerms\tTerm Δ%\tTerm Cml%\t"
        "Postings\tPostings Δ%\tPostings Cml%"
    )

    lines.append(header)

    first_terms = results[0][1]
    first_postings = results[0][2]

    previous_terms = first_terms
    previous_postings = first_postings

    for i, (stage, terms, postings) in enumerate(results):

        if i == 0:
            term_delta = "-"
            term_cml = "-"
            postings_delta = "-"
            postings_cml = "-"

        else:
            # 30-stopword and 150-stopword experiments are both
            # compared against the case-folded collection.
            if stage == "150 stopwords":
                comparison_terms = results[2][1]
                comparison_postings = results[2][2]
            else:
                comparison_terms = previous_terms
                comparison_postings = previous_postings

            term_delta_value = (
                (terms - comparison_terms)
                / comparison_terms
                * 100
            )

            term_cml_value = (
                (terms - first_terms)
                / first_terms
                * 100
            )

            postings_delta_value = (
                (postings - comparison_postings)
                / comparison_postings
                * 100
            )

            postings_cml_value = (
                (postings - first_postings)
                / first_postings
                * 100
            )

            term_delta = f"{term_delta_value:.1f}%"
            term_cml = f"{term_cml_value:.1f}%"
            postings_delta = f"{postings_delta_value:.1f}%"
            postings_cml = f"{postings_cml_value:.1f}%"

        line = (
            f"{stage}\t"
            f"{terms}\t"
            f"{term_delta}\t"
            f"{term_cml}\t"
            f"{postings}\t"
            f"{postings_delta}\t"
            f"{postings_cml}"
        )

        lines.append(line)

        previous_terms = terms
        previous_postings = postings

    table = "\n".join(lines)

    print(table)

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(table)

    print(f"\nSaved to: {output_file}")


if __name__ == "__main__":
    main()