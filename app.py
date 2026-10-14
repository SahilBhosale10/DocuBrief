# app.py
# Flask backend for DocuBrief
# Feature 2: Small / Medium / Large summaries
# Feature 3: Keyword extraction and highlighting
# Feature 4: Hindi translation


import os

from flask import Flask, request, jsonify, render_template

from extract_text import (
    extract_text_universal,
    get_page_count_universal
)

from summarizer import (
    summarize,
    extract_keywords,
    highlight_keywords
)

from preprocess import preprocess_text

from translator import translate_text


# =========================================================
# CREATE FLASK APPLICATION
# =========================================================

app = Flask(__name__)


# =========================================================
# UPLOAD FOLDER
# =========================================================

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# =========================================================
# SUMMARIZE ROUTE
# =========================================================

@app.route("/summarize", methods=["POST"])
def summarize_document():

    # -----------------------------------------------------
    # 1. CHECK FILE
    # -----------------------------------------------------

    if "pdf_file" not in request.files:

        return jsonify({
            "error": "No file uploaded."
        }), 400


    uploaded_file = request.files["pdf_file"]


    if uploaded_file.filename == "":

        return jsonify({
            "error": "No file selected."
        }), 400


    # -----------------------------------------------------
    # 2. GET FILE EXTENSION
    # -----------------------------------------------------

    extension = os.path.splitext(
        uploaded_file.filename
    )[1].lower()


    allowed_extensions = [
        ".pdf",
        ".docx",
        ".txt"
    ]


    if extension not in allowed_extensions:

        return jsonify({
            "error":
            "Only PDF, DOCX, and TXT files are allowed."
        }), 400


    # -----------------------------------------------------
    # 3. GET SUMMARY LENGTH
    # -----------------------------------------------------

    length = request.form.get(
        "length",
        "medium"
    ).lower()


    if length not in [
        "small",
        "medium",
        "large"
    ]:

        length = "medium"


    # -----------------------------------------------------
    # 4. CREATE SAFE FILE NAME
    # -----------------------------------------------------

    filename = os.path.basename(
        uploaded_file.filename
    )


    save_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )


    # -----------------------------------------------------
    # 5. SAVE FILE
    # -----------------------------------------------------

    uploaded_file.save(
        save_path
    )


    print("\n===================================")
    print("FILE RECEIVED")
    print("Filename:", filename)
    print("Extension:", extension)
    print("Summary Length:", length)
    print("Saved Path:", save_path)
    print("===================================\n")


    try:

        # -------------------------------------------------
        # 6. EXTRACT TEXT
        # -------------------------------------------------

        raw_text = extract_text_universal(
            save_path
        )


        print(
            "Extracted characters:",
            len(raw_text)
        )


        # -------------------------------------------------
        # 7. CHECK EXTRACTED TEXT
        # -------------------------------------------------

        if len(raw_text.strip()) == 0:

            return jsonify({
                "error":
                "Could not extract any text from this file."
            }), 400


        # -------------------------------------------------
        # 8. GET PAGE COUNT
        # -------------------------------------------------

        page_count = get_page_count_universal(
            save_path
        )


        # -------------------------------------------------
        # 9. CREATE SUMMARY
        # -------------------------------------------------

        summary = summarize(
            raw_text,
            length=length
        )


        # -------------------------------------------------
        # 10. PREPROCESS DOCUMENT
        # -------------------------------------------------

        original_sentences, cleaned_sentences = preprocess_text(
            raw_text
        )


        # -------------------------------------------------
        # 11. EXTRACT TOP 8 KEYWORDS
        # -------------------------------------------------

        keywords = extract_keywords(
            cleaned_sentences,
            top_n=8
        )


        print(
            "Keywords:",
            keywords
        )


        # -------------------------------------------------
        # 12. HIGHLIGHT KEYWORDS
        # -------------------------------------------------

        highlighted_summary = highlight_keywords(
            summary,
            keywords
        )


        # -------------------------------------------------
        # 13. WORD COUNTS
        # -------------------------------------------------

        original_word_count = len(
            raw_text.split()
        )


        summary_word_count = len(
            summary.split()
        )


        # -------------------------------------------------
        # 14. REDUCTION PERCENTAGE
        # -------------------------------------------------

        if original_word_count > 0:

            reduction_percent = round(
                100 -
                (
                    summary_word_count
                    / original_word_count
                    * 100
                ),
                1
            )

        else:

            reduction_percent = 0


        # -------------------------------------------------
        # 15. RETURN RESULT
        # -------------------------------------------------

        return jsonify({

            "page_count":
                page_count,

            "original_word_count":
                original_word_count,

            "summary_word_count":
                summary_word_count,

            "reduction_percent":
                reduction_percent,

            "length":
                length,

            "summary":
                summary,

            "highlighted_summary":
                highlighted_summary,

            "keywords":
                keywords

        })


    # -----------------------------------------------------
    # ERROR HANDLING
    # -----------------------------------------------------

    except Exception as e:

        print(
            "ERROR:",
            str(e)
        )


        return jsonify({
            "error":
            "Something went wrong while processing: "
            + str(e)
        }), 500


    # -----------------------------------------------------
    # DELETE TEMPORARY FILE
    # -----------------------------------------------------

    finally:

        if os.path.exists(save_path):

            os.remove(
                save_path
            )


# =========================================================
# TRANSLATE SUMMARY ROUTE
# =========================================================

@app.route("/translate", methods=["POST"])
def translate_summary():

    data = request.get_json()


    # -----------------------------------------------------
    # GET DATA
    # -----------------------------------------------------

    text = data.get(
        "text",
        ""
    )

    target_lang = data.get(
        "target_lang",
        ""
    )


    # -----------------------------------------------------
    # CHECK TEXT
    # -----------------------------------------------------

    if not text:

        return jsonify({

            "error":
            "No text provided."

        }), 400


    # -----------------------------------------------------
    # CHECK LANGUAGE
    # -----------------------------------------------------

    if target_lang not in [
        "en",
        "hi"
    ]:

        return jsonify({

            "error":
            "Invalid language."

        }), 400


    try:

        # -------------------------------------------------
        # TRANSLATE TEXT
        # -------------------------------------------------

        translated_text = translate_text(
            text,
            target_lang
        )


        # -------------------------------------------------
        # CHECK TRANSLATION
        # -------------------------------------------------

        if translated_text is None:

            return jsonify({

                "error":
                "Translation failed."

            }), 500


        # -------------------------------------------------
        # RETURN TRANSLATION
        # -------------------------------------------------

        return jsonify({

            "translated_text":
                translated_text

        })


    except Exception as e:

        print(
            "Translation error:",
            str(e)
        )


        return jsonify({

            "error":
            str(e)

        }), 500


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/", methods=["GET"])
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# RUN FLASK
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )