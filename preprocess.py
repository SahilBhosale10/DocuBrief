# preprocess.py
# This program cleans and prepares text for summarization

import nltk
import string

# Download required NLTK data (only needs to happen once)
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# Load the list of English stopwords once
STOP_WORDS = set(stopwords.words('english'))


def split_into_sentences(text):
    """Splits a big block of text into a list of individual sentences."""
    sentences = sent_tokenize(text)
    return sentences


def clean_sentence(sentence):
    """Cleans one sentence: lowercase, remove punctuation, remove stopwords."""
    # Step 1: lowercase everything
    sentence = sentence.lower()
    
    # Step 2: remove punctuation
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))
    
    # Step 3: split into words
    words = word_tokenize(sentence)
    
    # Step 4: remove stopwords
    cleaned_words = [word for word in words if word not in STOP_WORDS]
    
    # Step 5: join back into a cleaned sentence
    cleaned_sentence = " ".join(cleaned_words)
    return cleaned_sentence


def preprocess_text(text):
    """
    Takes raw text, returns two lists:
    - original_sentences: unmodified sentences (for final display)
    - cleaned_sentences: cleaned versions (for scoring)
    """
    original_sentences = split_into_sentences(text)
    cleaned_sentences = [clean_sentence(s) for s in original_sentences]
    return original_sentences, cleaned_sentences


# ---- Test this file directly ----
if __name__ == "__main__":
    sample_text = (
        "DocuBrief is an NLP mini-project. It summarizes long PDF documents. "
        "The system extracts text and removes unimportant words. "
        "This helps users save time while reading reports."
    )

    originals, cleaned = preprocess_text(sample_text)

    print("----- ORIGINAL SENTENCES -----")
    for i, s in enumerate(originals):
        print(f"{i+1}. {s}")

    print("\n----- CLEANED SENTENCES -----")
    for i, s in enumerate(cleaned):
        print(f"{i+1}. {s}")