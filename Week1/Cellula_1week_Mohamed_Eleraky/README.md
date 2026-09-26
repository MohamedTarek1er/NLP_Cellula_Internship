# Toxic Category Classification (LSTM / RNN)

A text classification project that labels input text into one of **5 toxic-content categories** using deep learning (LSTM and RNN architectures).

## Classes

- `Safe`
- `Violent Crimes`
- `Non-Violent Crimes`
- `unsafe`
- `Suicide & Self-Harm`

## Overview

The pipeline covers the full path from raw, noisy data to a trained sequence model: label correction, deduplication, class-imbalance handling, leakage-safe preprocessing, and training/evaluation of both an LSTM and an RNN model.

## Data Preparation

The source data started as 3,000 rows across two columns (image description, query). These were stacked into a single `text` column, producing 6,000 rows against an original 9-class `Toxic Category` target.

**Wrong labels.** Cross-checking exact-duplicate texts against their assigned labels surfaced two kinds of errors:

- Duplicate rows with conflicting labels — the same text tagged with several different categories across the dataset.
- Near-duplicate template phrasings scattered inconsistently across categories.

Each case was corrected using a mix of LLM-assisted review and manual judgment, choosing the label best supported by the text's actual content and by how visibly-similar phrasings were labeled elsewhere in the data.

**Duplicates.** Exact duplicate rows were removed after label correction, so every row reflects a distinct text with a verified label.

**Class imbalance after dedup.** With duplicates removed, several of the original 9 classes had almost no unique examples left (as few as 1–3 rows), making them unusable for stratified splitting and training. Related classes were merged into broader, better-supported categories:

| Original class            | Merged into        |
| ------------------------- | ------------------ |
| Child Sexual Exploitation | Sex-Related Crimes |
| Elections                 | Non-Violent Crimes |
| Sex-Related Crimes        | unsafe             |

This brought the target down from 9 classes to **5 final classes**. The resulting class distribution (unique rows) was:

| Class               | Rows |
| ------------------- | ---- |
| Safe                | 868  |
| Violent Crimes      | 689  |
| Non-Violent Crimes  | 234  |
| unsafe              | 227  |
| Suicide & Self-Harm | 3    |

`Suicide & Self-Harm` remains extremely small; it was kept separate rather than merged further because it needs a different handling path (e.g. crisis response) than a generic harmful-content label, but its low count limits how reliably the model can learn or be evaluated on it.

## Text Preprocessing

- **Cleaning** — removed hashtags, email addresses, URLs, punctuation noise, and collapsed extra whitespace.
- **Split** — data was split into train / validation / test **before** any further preprocessing (tokenizer fitting, embedding lookup, etc.), so nothing derived from validation/test leaks into training.
- **Label encoding** — `Toxic Category` was label-encoded into integer class ids for the 5 final classes.
- **Tokenization & padding** — text was tokenized into integer sequences (vocabulary built from the training set only) and padded/truncated to a fixed max length.
- **Embedding** — token ids are mapped to dense vectors via an embedding layer.

## Model Architecture & Training Setup

Two sequence architectures were trained and compared:

| Model | Core layer                                     |
| ----- | ---------------------------------------------- |
| LSTM  | LSTM layer(s) over the embedded sequence       |
| RNN   | Simple RNN layer(s) over the embedded sequence |

Shared training configuration:

| Component       | Choice                                                                                |
| --------------- | ------------------------------------------------------------------------------------- |
| Optimizer       | AdamW, with weight decay for regularization                                           |
| LR schedule     | ReduceLROnPlateau (lowers the learning rate when validation performance stalls)       |
| Early stopping  | Training halted once validation performance stopped improving, restoring best weights |
| Class imbalance | Class weights applied during training to compensate for uneven class sizes            |

This combination targets the two main risks in the dataset: overfitting on a relatively small number of unique examples, and the model defaulting to majority classes (`Safe`, `Violent Crimes`) given the imbalance.

Overall accuracy was not strong for either model. Given the class distribution (`Safe` and `Violent Crimes` together make up the large majority of unique rows, while `Suicide & Self-Harm` has only 3), per-class F1 and the confusion matrices are more informative than the single accuracy number — in particular for comparing whether LSTM or RNN handles the minority classes better, and whether either collapses onto the majority classes.

## Limitations & Next Steps

- **`Suicide & Self-Harm`** has only 3 unique examples after dedup — far too few to train or evaluate reliably. Sourcing more real examples for this class (rather than merging it away) would materially help, since it needs a distinct response path from generic `unsafe` content.
- **Dataset size.** After deduplication the usable dataset is roughly 2,000 unique texts, small for an RNN/LSTM trained from scratch; a pretrained embedding (e.g. GloVe) or a pretrained transformer encoder would likely outperform a from-scratch model at this scale.
- **Class imbalance** remains even after merging (`Safe` and `Violent Crimes` dominate); class weights help but don't fully offset it — oversampling minority classes or collecting more data for `Non-Violent Crimes` / `unsafe` would help further.
- **Next step:** review the confusion matrices once added — they'll show whether errors are concentrated in specific class pairs (e.g. `Non-Violent Crimes` vs. `unsafe`, which overlap conceptually) rather than spread evenly.
