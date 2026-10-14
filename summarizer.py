# summarizer.py
# DocuBrief - TF-IDF based document summarizer
# Includes keyword extraction and keyword highlighting

import re
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer

from preprocess import preprocess_text


# =========================================================
# GET NUMBER OF SUMMARY SENTENCES
# =========================================================

def get_num_sentences(total_sentences, length="medium"):

    if length == "small":
        num_sentences = 3

    elif length == "medium":
        num_sentences = 6

    elif length == "large":
        num_sentences = 10

    else:
        num_sentences = 6


    if num_sentences > total_sentences:
        num_sentences = total_sentences


    return num_sentences


# =========================================================
# SCORE SENTENCES
# =========================================================

def score_sentences(cleaned_sentences):

    if not cleaned_sentences:
        return np.array([])


    vectorizer = TfidfVectorizer()


    try:

        tfidf_matrix = vectorizer.fit_transform(
            cleaned_sentences
        )

    except ValueError:

        return np.zeros(
            len(cleaned_sentences)
        )


    sentence_scores = np.array(
        tfidf_matrix.sum(axis=1)
    ).flatten()


    return sentence_scores


# =========================================================
# EXTRACT KEYWORDS
# =========================================================

def extract_keywords(cleaned_sentences, top_n=8):

    if not cleaned_sentences:
        return []


    vectorizer = TfidfVectorizer()


    try:

        tfidf_matrix = vectorizer.fit_transform(
            cleaned_sentences
        )

    except ValueError:

        return []


    scores = np.array(
        tfidf_matrix.sum(axis=0)
    ).flatten()


    words = vectorizer.get_feature_names_out()


    word_scores = list(
        zip(words, scores)
    )


    word_scores.sort(
        key=lambda x: x[1],
        reverse=True
    )


    top_keywords = [
        word
        for word, score in word_scores[:top_n]
    ]


    return top_keywords


# =========================================================
# HIGHLIGHT KEYWORDS
# =========================================================

def highlight_keywords(summary_text, keywords):

    highlighted = summary_text


    # Sort longest keywords first
    # This prevents shorter words from interfering
    keywords = sorted(
        keywords,
        key=len,
        reverse=True
    )


    for keyword in keywords:

        pattern = re.compile(
            r"\b(" +
            re.escape(keyword) +
            r")\b",
            re.IGNORECASE
        )


        highlighted = pattern.sub(
            r"<mark>\1</mark>",
            highlighted
        )


    return highlighted


# =========================================================
# CREATE SUMMARY
# =========================================================

def summarize(text, length="medium"):

    original_sentences, cleaned_sentences = preprocess_text(
        text
    )


    total_sentences = len(
        original_sentences
    )


    print("--------------------------------")
    print(
        "Total sentences:",
        total_sentences
    )


    print(
        "Selected length:",
        length
    )


    num_sentences = get_num_sentences(
        total_sentences,
        length
    )


    print(
        "Summary sentences:",
        num_sentences
    )


    print("--------------------------------")


    if total_sentences == 0:

        return "No text could be summarized."


    if total_sentences <= num_sentences:

        return " ".join(
            original_sentences
        )


    scores = score_sentences(
        cleaned_sentences
    )


    if len(scores) == 0:

        return " ".join(
            original_sentences[:num_sentences]
        )


    ranked_indexes = np.argsort(
        scores
    )[::-1]


    top_indexes = ranked_indexes[
        :num_sentences
    ]


    # Put sentences back into original order
    top_indexes_sorted = sorted(
        top_indexes
    )


    summary_sentences = []


    for index in top_indexes_sorted:

        summary_sentences.append(
            original_sentences[index]
        )


    summary = " ".join(
        summary_sentences
    )


    return summary