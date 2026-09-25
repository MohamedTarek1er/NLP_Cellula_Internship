# Libraries
import re
import string
import nltk

from collections import Counter

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, SnowballStemmer, WordNetLemmatizer

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from IPython.display import display

# Reading Data
def load_data(path, file_type="csv", **kwargs):
    """
    Load a dataset from CSV or Excel.
    """
    
    if file_type == "csv":
        df = pd.read_csv(path, **kwargs)

    elif file_type in ["excel", "xlsx", "xls"]:
        df = pd.read_excel(path, **kwargs)

    else:
        raise ValueError("Unsupported file type. Use 'csv' or 'excel'.")

    return df

# Exploring Data
def explore_text_data(
    df,
    text_columns=None,
    target_column=None
):

    dataset_overview = pd.DataFrame({
        "Metric": [
            "Rows",
            "Columns",
            "Missing Values",
            "Duplicate Rows",
        ],
        "Value": [
            len(df),
            len(df.columns),
            df.isnull().sum().sum(),
            df.duplicated().sum(),
        ]
    })

    # Column information
    column_info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Unique Values": df.nunique(dropna=False).values,
        "Missing Values": df.isnull().sum().values,
        "Missing %": (
            df.isnull().mean() * 100
        ).round(2).values
    })

    print("\n" + "=" * 70)
    print("DATASET OVERVIEW")
    print("=" * 70)

    display(dataset_overview)

    print("\n" + "=" * 70)
    print("Columns Information:")
    print("=" * 70)

    display(column_info)

# Text information
    text_info = None
    if text_columns is not None:

        if isinstance(text_columns, str):
            text_columns = [text_columns]

        text_results = []

        for column in text_columns:
            # Convert only for analysis
            text = df[column].fillna("").astype(str)

            char_length = text.str.len()
            word_count = text.str.split().str.len()

            empty_count = (text.str.strip() == "").sum()
            duplicate_texts = text.duplicated().sum()

            text_results.append({
                "Column": column,
                "Unique Texts": text.nunique(),
                "Empty Texts": empty_count,
                "Empty %": round(
                    empty_count / len(text) * 100, 2
                ),
                "Duplicate Texts": duplicate_texts,
                "Duplicate %": round(
                    duplicate_texts / len(text) * 100, 2
                ),
                "Min Characters": char_length.min(),
                "Max Characters": char_length.max(),
                "Min Words": word_count.min(),
                "Max Words": word_count.max(),
                "Mean Words": round(
                    word_count.mean(), 2
                ),
                "Median Words": round(
                    word_count.median(), 2
                )
            })

        if text_results:
            text_info = pd.DataFrame(text_results, columns=text_results[0].keys())

            print("\n" + "=" * 70)
            print("TEXT ANALYSIS")
            print("=" * 70)

            display(text_info)

# Target information
    target_info = None
    if target_column is not None:

        if target_column not in df.columns:
            print(f"\nWarning: '{target_column}' not found.")
        else:
            target = df[target_column]

            target_info = pd.DataFrame({
                "Class": target.value_counts(
                    dropna=False
                ).index.astype(str),

                "Count": target.value_counts(
                    dropna=False
                ).values,

                "Percentage": (
                    target.value_counts(
                        normalize=True,
                        dropna=False
                    ) * 100
                ).round(2).values
            })

            print("\n" + "=" * 70)
            print("TARGET ANALYSIS")
            print("=" * 70)

            print(f"\nTarget: {target_column}")
            print(
                f"Unique Classes: "
                f"{target.nunique(dropna=False)}"
            )
            print(
                f"Missing Targets: "
                f"{target.isnull().sum()}"
            )

            display(target_info)

    return dataset_overview, column_info, text_info, target_info

# Basic Cleaning 
def Basic_clean_text(
    text,
    lowercase=True,
    remove_html=True,
    remove_urls=True,
    remove_emails=True,
    remove_mentions=True,
    remove_hashtags=True,
    remove_numbers=False,
    remove_punctuation=True,
    remove_extra_spaces=True,
    remove_newlines=True,
    remove_control_chars=True,
    normalize_repeated_chars=False,
    min_repeated_chars=3
):

    # Handle missing / invalid values
    if text is None:
        return ""

    if not isinstance(text, str):
        text = str(text)

    # Remove HTML
    if remove_html:
        text = re.sub(r"<[^>]+>", " ", text)

    # Remove / replace URLs
    if remove_urls:
        text = re.sub(
            r"https?://\S+|www\.\S+",
            " ",
            text
        )

    # Remove / replace emails
    if remove_emails:
        text = re.sub(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            " ",
            text
        )

    # Remove mentions
    if remove_mentions:
        text = re.sub(
            r"(?<!\w)@\w+",
            " ",
            text
        )

    # Handle hashtags
    if remove_hashtags:
        text = re.sub(
            r"(?<!\w)#\w+",
            " ",
            text
        )
    else:
        # Keep the hashtag word but remove '#'
        text = re.sub(
            r"#(\w+)",
            r"\1",
            text
        )

    # Remove numbers
    if remove_numbers:
        text = re.sub(r"\d+", " ", text)

    # Normalize repeated characters
    if normalize_repeated_chars:
        pattern = rf"(.)\1{{{min_repeated_chars},}}"
        text = re.sub(
            pattern,
            r"\1",
            text
        )

    # Remove punctuation
    if remove_punctuation:
        text = re.sub(
            r"[^\w\s]",
            " ",
            text,
            flags=re.UNICODE
        )

    # Remove newlines and tabs
    if remove_newlines:
        text = re.sub(r"[\r\n\t]+", " ", text)

    # Lowercase
    if lowercase:
        text = text.lower()

    # Normalize whitespace
    if remove_extra_spaces:
        text = re.sub(r"\s+", " ", text)

    text = text.strip()

    return text

# Download NLTK resources
def download_resources():
    resources = [
        "punkt",
        "punkt_tab",
        "stopwords",
        "wordnet",
    ]

    for resource in resources:
        nltk.download(resource, quiet=True)

# Splitting data
def split_data(
    df,
    target_column=None,
    test_size=0.2,
    validation_size=0.2,
    random_state=42,
    stratify=True,
    shuffle=True
):
    
    # 1. Validate target column
    if target_column is not None:
        if target_column not in df.columns:
            raise ValueError(
                f"Target column '{target_column}' not found."
            )

    # 2. Stratification
    stratify_data = None
    if stratify and target_column is not None:
        stratify_data = df[target_column]

    # 3. Split train + test
    train_df, test_df = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state,
        shuffle=shuffle,
        stratify=stratify_data
    )

    # 4. No validation set
    if validation_size is None:
        return train_df, test_df

    # 5. Calculate validation ratio
    validation_ratio = validation_size / (
        1 - test_size
    )

    # Stratification for train/validation
    stratify_train = None
    if stratify and target_column is not None:
        stratify_train = train_df[target_column]

    # Split train + validation
    train_df, validation_df = train_test_split(
        train_df,
        test_size=validation_ratio,
        random_state=random_state,
        shuffle=shuffle,
        stratify=stratify_train
    )

    return train_df, validation_df, test_df

# Preprocessing
def clean_text(
    text,
    lowercase=True,
    remove_urls=True,
    remove_emails=True,
    remove_html=True,
    remove_mentions=False,
    remove_hashtags=False,
    remove_numbers=False,
    remove_punctuation=True,
    remove_special_chars=True,
    normalize_whitespace=True
):
    """Clean and normalize raw text."""

    if lowercase:
        text = text.lower()

    if remove_html:
        text = re.sub(r"<[^>]+>", " ", text)

    if remove_urls:
        text = re.sub(
            r"https?://\S+|www\.\S+",
            " ",
            text
        )

    if remove_emails:
        text = re.sub(
            r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b",
            " ",
            text
        )

    if remove_mentions:
        text = re.sub(r"@\w+", " ", text)

    if remove_hashtags:
        text = re.sub(r"#\w+", " ", text)

    if remove_numbers:
        text = re.sub(r"\d+", " ", text)

    if remove_punctuation:
        text = text.translate(
            str.maketrans("", "", string.punctuation)
        )

    if remove_special_chars:
        text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    if normalize_whitespace:
        text = re.sub(r"\s+", " ", text).strip()

    return text

# Tokenization
def tokenize(text, method="word"):
    """
    method:
        word
        sentence
        regex
    """

    if method == "word":
        return nltk.word_tokenize(text)

    elif method == "sentence":
        return nltk.sent_tokenize(text)

    elif method == "regex":
        return re.findall(r"\b\w+\b", text)

    else:
        raise ValueError(
            "method must be 'word', 'sentence', or 'regex'"
        )

# Normalization
def normalize_tokens(
    tokens,
    remove_stopwords=True,
    normalization="lemmatize",
    language="english"
):
    """
    normalization:
        None
        stem
        lemmatize
    """

    stop_words = set(stopwords.words(language))

    if normalization == "stem":
        stemmer = PorterStemmer()

    elif normalization == "lemmatize":
        lemmatizer = WordNetLemmatizer()

    elif normalization is not None:
        raise ValueError(
            "normalization must be None, 'stem', or 'lemmatize'"
        )

    result = []

    for token in tokens:

        if remove_stopwords and token in stop_words:
            continue

        if normalization == "stem":
            token = stemmer.stem(token)

        elif normalization == "lemmatize":
            token = lemmatizer.lemmatize(token)

        result.append(token)

    return result

# Vectorization
def vectorize(
    documents,
    method="tfidf",
    max_features=None,
    ngram_range=(1, 1)
):
    """
    method:
        bow
        tfidf
    """

    if method == "bow":

        vectorizer = CountVectorizer(
            max_features=max_features,
            ngram_range=ngram_range
        )

    elif method == "tfidf":

        vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range
        )

    else:
        raise ValueError(
            "method must be 'bow' or 'tfidf'"
        )

    matrix = vectorizer.fit_transform(documents)
    features = vectorizer.get_feature_names_out()

    return matrix, features