# extract_text.py
# This program extracts text from PDF, DOCX, and TXT files

import fitz  # PyMuPDF library
import re    # Regular expressions
from docx import Document
import os


def clean_raw_text(text):
    """
    Removes leftover HTML-like tags (e.g. <b>, </b>, <i>)
    that sometimes get embedded in extracted text.
    """

    # Remove anything that looks like <...>
    cleaned = re.sub(r"<[^>]+>", "", text)

    return cleaned


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    """

    # Open the PDF file
    document = fitz.open(pdf_path)

    full_text = ""

    # Loop through every page in the PDF
    for page_number in range(len(document)):

        # Get one page
        page = document[page_number]

        # Extract text from that page
        page_text = page.get_text()

        # Add text to collected text
        full_text += page_text

    # Close the PDF
    document.close()

    # Clean extracted text
    full_text = clean_raw_text(full_text)

    return full_text


def get_pdf_page_count(pdf_path):
    """
    Returns the number of pages in a PDF.
    """

    # Open PDF
    document = fitz.open(pdf_path)

    # Get number of pages
    page_count = len(document)

    # Close PDF
    document.close()

    return page_count


# =========================================================
# DOCX EXTRACTION
# =========================================================

def extract_text_from_docx(docx_path):
    """
    Extracts text from a Word (.docx) file.
    """

    # Open the Word document
    doc = Document(docx_path)

    full_text = ""

    # Loop through all paragraphs
    for paragraph in doc.paragraphs:

        # Add paragraph text
        full_text += paragraph.text + "\n"

    # Clean extracted text
    return clean_raw_text(full_text)


# =========================================================
# TXT EXTRACTION
# =========================================================

def extract_text_from_txt(txt_path):
    """
    Extracts text from a plain .txt file.
    """

    # Open the text file
    with open(
        txt_path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as f:

        # Read complete file
        text = f.read()

    # Clean extracted text
    return clean_raw_text(text)


# =========================================================
# UNIVERSAL TEXT EXTRACTION
# =========================================================

def extract_text_universal(file_path):
    """
    Automatically selects the correct extraction method
    based on the file extension.
    """

    # Get file extension
    extension = os.path.splitext(file_path)[1].lower()

    # PDF
    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    # DOCX
    elif extension == ".docx":
        return extract_text_from_docx(file_path)

    # TXT
    elif extension == ".txt":
        return extract_text_from_txt(file_path)

    # Unsupported file
    else:
        raise ValueError(
            "Unsupported file type: " + extension
        )


# =========================================================
# UNIVERSAL PAGE COUNT
# =========================================================

def get_page_count_universal(file_path):
    """
    Returns page count for PDFs.

    DOCX and TXT files do not have a reliable page count
    in this extraction system, so they return 1.
    """

    # Get file extension
    extension = os.path.splitext(file_path)[1].lower()

    # PDF
    if extension == ".pdf":
        return get_pdf_page_count(file_path)

    # DOCX and TXT
    return 1


# =========================================================
# TEST PDF EXTRACTION
# =========================================================

if __name__ == "__main__":

    pdf_path = "sample_pdfs/sample.pdf"

    extracted_text = extract_text_from_pdf(pdf_path)

    print("----- EXTRACTED TEXT (first 500 characters) -----")

    print(extracted_text[:500])

    print("----- END OF PREVIEW -----")

    print(
        "Total characters extracted:",
        len(extracted_text)
    )