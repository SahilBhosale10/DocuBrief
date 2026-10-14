# test_pipeline.py
# This program connects PDF extraction + summarization and tests it end-to-end

from extract_text import extract_text_from_pdf
from summarizer import summarize


def run_pipeline(pdf_path, num_sentences=5):
    print(f"Reading PDF: {pdf_path}")
    
    # Step 1: Extract raw text from PDF
    raw_text = extract_text_from_pdf(pdf_path)
    print(f"Extracted {len(raw_text)} characters from PDF.\n")

    # Step 2: Generate summary from that text
    summary = summarize(raw_text, num_sentences=num_sentences)

    return raw_text, summary


# ---- Run the pipeline on a real PDF ----
if __name__ == "__main__":
    pdf_path = "sample_pdfs/sample.pdf"   # change this to test different PDFs
    
    raw_text, summary = run_pipeline(pdf_path, num_sentences=5)

    print("----- ORIGINAL TEXT (first 800 characters) -----")
    print(raw_text[:800])
    print("...\n")

    print("----- GENERATED SUMMARY -----")
    print(summary)

    print("\n----- STATS -----")
    print("Original word count:", len(raw_text.split()))
    print("Summary word count:", len(summary.split()))
    reduction = 100 - (len(summary.split()) / len(raw_text.split()) * 100)
    print(f"Reduction: {reduction:.1f}% shorter than original")