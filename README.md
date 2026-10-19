# COMP 479/6791 – Project 1: Reuters-21578 indexing

Building an inverted index for the Reuters-21578 collection (NEWID = docID), with a naive indexer, query processing, a lossy compression experiment and a SPIMI-inspired indexer.

## Requirements

- **Subproject I – Naive indexer:** token stream → list F of term-docID pairs → sort → remove duplicates → postings lists.
- **Subproject II – Query processing:** single-term queries and AND queries (postings-list intersection). 3 single-term + 3 AND test queries.
- **Subproject III – Compression:** lossy dictionary compression, table of results, compare query results with the uncompressed index.
- **Subproject IV – SPIMI:** build postings lists directly, no compression. Timing against the naive indexer on 10,000 term-docID pairs.
- Challenge queries, project report, demo.

## Structure

```
src/            preprocessing, indexers, queries, compression, benchmark
scripts/        entry points for each part
tests/          pytest tests
manual_tests/   small scripts for checking things by hand (not run by pytest)
data/raw/       Reuters-21578 files (not in Git)
data/processed/ generated files (not in Git)
results/        query outputs, benchmark timings, challenge queries
experiments/    compression experiment tables
report/         project report
demo/           demo notes and screenshots
```

## Setup (Windows)

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -c "import nltk; nltk.download('punkt_tab')"
```

Download `reuters21578.tar.gz` from http://www.daviddlewis.com/resources/testcollections/reuters21578/ and extract it to `data/raw/reuters21578/` (the folder should contain `reut2-000.sgm` … `reut2-021.sgm`).

## Running

Run from the project root (the data path is relative):

```
.venv\Scripts\python -m scripts.run_naive              # Subproject I
.venv\Scripts\python -m scripts.run_queries            # Subproject II   -> results/queries/s2_queries.txt
.venv\Scripts\python -m scripts.run_compression        # Subproject III  -> experiments/compression/compression_table.tsv
.venv\Scripts\python -m scripts.run_query_comparison   # Subproject III  -> experiments/compression/query_comparison.tsv
.venv\Scripts\python -m scripts.run_spimi              # Subproject IV
.venv\Scripts\python -m scripts.run_benchmark          # Subproject IV   -> results/benchmark/spimi_benchmark.txt
.venv\Scripts\python -m scripts.run_challenge          # Challenge       -> results/challenge/
.venv\Scripts\python -m pytest
```

## Results

- Full index: 74,870 terms, naive and SPIMI indexes identical.
- Challenge: `Carmark` → 1 doc (19758), `copper` → 117 docs, `Chrysler and Bundesbank` → 0 docs, same on both indexes.
- Details in `report/project_report.md`, screenshots in `demo/demo.md`.

## Checklist

- [x] Preprocessing – `src/preprocessing.py`
- [x] Subproject I: naive indexer – `src/naive_indexer.py`, `scripts/run_naive.py`
- [x] Subproject II: queries – `src/query_processor.py`, `scripts/run_queries.py`, `results/queries/`
- [x] Subproject III: compression – `src/compression.py`, `experiments/compression/`, `report/compression_experiment.md`
- [x] Subproject IV: SPIMI – `src/spimi_indexer.py`, `scripts/run_spimi.py`
- [x] Naive vs SPIMI timing – `src/benchmark.py`, `scripts/run_benchmark.py`, `results/benchmark/`
- [x] Challenge queries – `scripts/run_challenge.py`, `results/challenge/`
- [x] Tests – `tests/`
- [ ] Report – `report/project_report.md` (AI use disclosure still to be written)
- [x] Demo – `demo/demo.md`
