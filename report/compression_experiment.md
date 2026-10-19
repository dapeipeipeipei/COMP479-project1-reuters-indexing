# Compression Experiment

**Course:** COMP 479/6791 — Information Retrieval and Web Search  
**Project:** Project 1 — Reuters-21578 Indexing  
**Dataset:** Reuters-21578  

## 1. Objective

The purpose of this experiment is to study how lossy preprocessing affects the size of an inverted index built from Reuters-21578. The experiment follows the preprocessing stages shown in Table 5.1 of the course material and records two measurements after each stage:

- the number of distinct **terms** in the dictionary;
- the number of **non-positional postings**, where one posting represents one term-document relationship.

The goal is not only to reduce the index, but also to understand which preprocessing operations mainly reduce vocabulary size and which mainly reduce postings.

## 2. Experimental Setup

The Reuters-21578 corpus was parsed using the `NEWID` attribute as the document identifier. For each document, text was extracted from the `TITLE` and `BODY` fields and tokenized with NLTK.

The following preprocessing stages were tested:

1. **Unfiltered** — tokens are kept without number removal or case folding.
2. **No numbers** — numeric tokens are removed.
3. **Case folding** — tokens are converted to lowercase.
4. **30 stopwords** — the 30 most frequent terms in the case-folded collection are removed.
5. **150 stopwords** — the 150 most frequent terms in the case-folded collection are removed.
6. **Stemming** — Porter stemming is applied after removing the 150 stopwords.

### Preprocessing Definitions

The stages are implemented in `src/compression.py` and are defined as follows.

- **Tokenization (unfiltered).** Text is tokenized with NLTK `word_tokenize`. Tokens that contain no letter or digit (punctuation only) are discarded; letter case and numbers are kept.
- **Number removal.** For each token, commas are removed and a trailing `%` is stripped, and the remainder is parsed with Python `float()`. If parsing succeeds, the token is treated as a number and removed. For example, `100`, `1,000`, `12.5` and `25%` are removed. Mixed alphanumeric forms such as `10-year`, `1986/87` and `G-7` do not parse as numbers and are therefore kept. Because `float()` also accepts the special spellings `nan`, `inf` and `infinity` in any letter case, the few tokens with these spellings are removed as well.
- **Case folding.** All tokens are converted to lowercase; for example, `Market`, `MARKET` and `market` all become `market`.
- **Stopword selection.** No predefined stopword list (such as the NLTK English list) is used. The stopwords are the 30 (or 150) most frequent terms in the case-folded Reuters-21578 collection, ranked by their total number of occurrences. Both lists are computed from, and removed from, the case-folded collection, so the 30-stopword and 150-stopword rows are two alternative variants of the case-folded collection rather than consecutive steps. Because the lists come from this collection, they contain corpus-specific frequent words such as `said`, `mln`, `dlrs`, `reuter` and `pct` in addition to function words such as `the` and `of`.
- **Stemming.** NLTK `PorterStemmer` is applied to the collection obtained after number removal, case folding and removal of the 150 most frequent terms. Porter stemming removes suffixes by rule, so related morphological forms are merged into a common stem for indexing; for example, `review`, `reviews`, `reviewed` and `reviewing` are all mapped to `review`. The resulting stems are indexing keys rather than dictionary lemmas and are not always valid English words.

For each stage, the program counts the number of unique dictionary terms and the number of unique term-document pairs. The delta column shows the change introduced by that preprocessing step, while the cumulative column shows the change relative to the unfiltered collection.

The 30-stopword and 150-stopword experiments are both compared with the case-folded collection. Stemming is compared with the 150-stopword collection.

## 3. Results

### Table 1. Effect of preprocessing on Reuters-21578

| Stage | Terms | Term Δ | Term Cml | Postings | Postings Δ | Postings Cml |
|---|---:|---:|---:|---:|---:|---:|
| Unfiltered | 91,280 | — | — | 1,723,515 | — | — |
| No numbers | 69,375 | -24.0% | -24.0% | 1,611,025 | -6.5% | -6.5% |
| Case folding | 52,967 | -23.7% | -42.0% | 1,493,162 | -7.3% | -13.4% |
| 30 stopwords | 52,937 | -0.1% | -42.0% | 1,214,289 | -18.7% | -29.5% |
| 150 stopwords | 52,817 | -0.3% | -42.1% | 933,340 | -37.5% | -45.8% |
| Stemming | 42,008 | -20.5% | -54.0% | 889,510 | -4.7% | -48.4% |

After all preprocessing stages, the number of terms decreases from **91,280 to 42,008**, which is a cumulative reduction of about **54.0%**. The number of non-positional postings decreases from **1,723,515 to 889,510**, which is a cumulative reduction of about **48.4%**.

## 4. Discussion

### 4.1 Removing numbers

Removing numeric tokens causes the dictionary to shrink from 91,280 to 69,375 terms, a reduction of 24.0%. The postings count decreases by only 6.5%.

This suggests that Reuters-21578 contains many different numeric forms. Values such as years, percentages, prices, dates, and other quantities can all become separate dictionary entries. Because many of these numeric forms occur in only a small number of documents, they increase the number of distinct terms much more than they increase the total number of postings.

In other words, number removal mainly reduces vocabulary variation in this collection.

### 4.2 Case folding

Case folding reduces the dictionary from 69,375 to 52,967 terms, a reduction of 23.7%. The postings count decreases by 7.3%.

The main effect is that different surface forms such as `Market`, `MARKET`, and `market` are treated as one term. Therefore, case folding merges dictionary entries that differ only in capitalization. The reduction in postings is smaller because the documents containing those word forms still contribute to the merged postings list.

### 4.3 Stopword removal

Removing 30 stopwords changes the dictionary only slightly, from 52,967 to 52,937 terms. However, the postings count decreases by 18.7%.

The same pattern becomes stronger when 150 stopwords are removed. The dictionary decreases by only 0.3% relative to the case-folded collection, while the postings count decreases by 37.5%.

This happens because stopwords are few in number but appear in a very large number of documents. A word such as `the` contributes only one dictionary term, but its postings list can contain thousands of document IDs. Removing a small set of high-frequency words therefore has little effect on dictionary size but a large effect on postings.

### 4.4 Stemming

After removing 150 stopwords, Porter stemming reduces the number of terms from 52,817 to 42,008, a reduction of 20.5%. The postings count decreases by only 4.7%.

Stemming mainly merges related word forms into a common stem. For example, forms such as `review`, `reviews`, `reviewed`, and `reviewing` can be mapped to the same stem. This reduces the number of dictionary entries, while many of the original document occurrences remain represented in the merged postings list.

Therefore, stemming has a much stronger effect on vocabulary size than on postings count.

## 5. Comparison with Table 5.1

The reference Table 5.1 in the course material reports the following values for a much larger Reuters collection:

| Stage | Terms | Term Δ | Term Cml | Non-positional postings | Posting Δ | Posting Cml |
|---|---:|---:|---:|---:|---:|---:|
| Unfiltered | 484,494 | — | — | 109,971,179 | — | — |
| No numbers | 473,723 | -2% | -2% | 100,680,242 | -8% | -8% |
| Case folding | 391,523 | -17% | -19% | 96,969,056 | -3% | -12% |
| 30 stopwords | 391,493 | ~0% | -19% | 83,390,443 | -14% | -24% |
| 150 stopwords | 391,373 | ~0% | -19% | 67,001,847 | -30% | -39% |
| Stemming | 322,383 | -17% | -33% | 63,812,300 | -4% | -42% |

The exact percentages are different, but the main trends are similar.

First, stopword removal has almost no effect on the number of terms but has a much larger effect on postings. This is true in both the reference table and the Reuters-21578 experiment.

Second, stemming produces a substantial reduction in the number of terms but only a small reduction in postings. Again, this trend is visible in both experiments.

Case folding also reduces dictionary size more strongly than it reduces postings.

The largest difference is number removal. In this experiment, number removal reduces the term count by 24.0%, while the reference table reports only about 2%. A likely explanation is that the two experiments use different corpus sizes and may differ in tokenization details and the exact text included for indexing. The course reference uses a much larger Reuters collection, while this project uses Reuters-21578.

Therefore, the exact percentages are not expected to match. The important observation is that the overall behavior of the preprocessing operations is consistent with the reference experiment.

## 6. Conclusion

The experiment shows that different lossy preprocessing techniques affect different parts of an inverted index.

- **Number removal** and **case folding** mainly reduce vocabulary variation.
- **Stopword removal** mainly reduces postings because a small number of very frequent terms occur in many documents.
- **Stemming** mainly reduces dictionary size by merging related word forms.

For Reuters-21578, the complete preprocessing pipeline reduces the dictionary by about **54.0%** and the non-positional postings by about **48.4%**.

The exact percentages differ from Table 5.1, but the main trends are similar. This supports the same general conclusion as the reference experiment: lossy preprocessing can make an inverted index substantially smaller by removing or merging information that is not always necessary for retrieval.
