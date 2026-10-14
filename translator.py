import argostranslate.translate


def translate_text(text, target_lang="en"):

    try:

        # English → Hindi
        if target_lang == "hi":

            translated = argostranslate.translate.translate(
                text,
                "en",
                "hi"
            )

            return translated

        # English
        elif target_lang == "en":

            return text

        else:

            return None

    except Exception as e:

        print("Translation error:", e)

        return None


# Test translation
if __name__ == "__main__":

    text = "Artificial intelligence is changing the world."

    print("Original:")
    print(text)

    print("\nHindi:")

    result = translate_text(
        text,
        "hi"
    )

    if result:

        print(result)

    else:

        print("Translation failed.")