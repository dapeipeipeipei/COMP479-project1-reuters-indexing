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
data/raw/       Reuters-21578 files (not in Git)
data/processed/ generated files (not in Git)
results/        query outputs, benchmark timings, challenge queries
experiments/    compression experiment tables
report/         project report
demo/           demo notes
```

## Setup (Windows)

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

Download `reuters21578.tar.gz` from http://www.daviddlewis.com/resources/testcollections/reuters21578/ and extract it to `data/raw/reuters21578/` (the folder should contain `reut2-000.sgm` … `reut2-021.sgm`).

## Running

Not implemented yet. Planned commands:

```
.venv\Scripts\python -m scripts.run_naive
.venv\Scripts\python -m scripts.run_queries
.venv\Scripts\python -m scripts.run_spimi
.venv\Scripts\python -m scripts.run_benchmark
.venv\Scripts\python -m scripts.run_challenge
.venv\Scripts\python -m pytest
```

## Checklist

- [ ] Preprocessing – `src/preprocessing.py`
- [ ] Subproject I: naive indexer – `src/naive_indexer.py`, `scripts/run_naive.py`
- [ ] Subproject II: queries – `src/query_processor.py`, `scripts/run_queries.py`, `results/queries/`
- [ ] Subproject III: compression – `src/compression.py`, `experiments/compression/`, `report/compression_experiment.md`
- [ ] Subproject IV: SPIMI – `src/spimi_indexer.py`, `scripts/run_spimi.py`
- [ ] Naive vs SPIMI timing – `src/benchmark.py`, `scripts/run_benchmark.py`, `results/benchmarks/`
- [ ] Challenge queries – `scripts/run_challenge.py`, `results/challenge/`
- [ ] Tests – `tests/`
- [ ] Report – `report/project_report.md`
- [ ] Demo – `demo/demo.md`
