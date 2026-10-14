// =====================================================
// DocuBrief - Frontend JavaScript
// =====================================================


// =====================================================
// GET HTML ELEMENTS
// =====================================================

const dropArea =
    document.getElementById("dropArea");

const pdfInput =
    document.getElementById("pdfInput");

const fileNameDisplay =
    document.getElementById("fileName");

const summarizeBtn =
    document.getElementById("summarizeBtn");

const statusMessage =
    document.getElementById("statusMessage");

const loader =
    document.getElementById("loader");

const resultBox =
    document.getElementById("resultBox");

const summaryText =
    document.getElementById("summaryText");

const wordStats =
    document.getElementById("wordStats");

const summaryLength =
    document.getElementById("summaryLength");


// =====================================================
// TRANSLATION ELEMENTS
// =====================================================

const languageSelect =
    document.getElementById("languageSelect");

const translateBtn =
    document.getElementById("translateBtn");

const translatedResult =
    document.getElementById("translatedResult");


// =====================================================
// STORE SELECTED FILE
// =====================================================

let selectedFile = null;


// =====================================================
// STORE ORIGINAL SUMMARY
// =====================================================

let originalSummary = "";


// =====================================================
// FILE SELECTION
// =====================================================

pdfInput.addEventListener(
    "change",
    function () {

        if (pdfInput.files.length > 0) {

            setSelectedFile(
                pdfInput.files[0]
            );

        }

    }
);


// =====================================================
// DRAG OVER
// =====================================================

dropArea.addEventListener(
    "dragover",
    function (event) {

        event.preventDefault();

        dropArea.classList.add(
            "dragover"
        );

    }
);


// =====================================================
// DRAG LEAVE
// =====================================================

dropArea.addEventListener(
    "dragleave",
    function () {

        dropArea.classList.remove(
            "dragover"
        );

    }
);


// =====================================================
// DROP FILE
// =====================================================

dropArea.addEventListener(
    "drop",
    function (event) {

        event.preventDefault();

        dropArea.classList.remove(
            "dragover"
        );


        if (
            event.dataTransfer.files.length > 0
        ) {

            setSelectedFile(
                event.dataTransfer.files[0]
            );

        }

    }
);


// =====================================================
// SET SELECTED FILE
// =====================================================

function setSelectedFile(file) {

    const fileName =
        file.name.toLowerCase();


    const allowedExtensions = [
        ".pdf",
        ".docx",
        ".txt"
    ];


    const isAllowed =
        allowedExtensions.some(
            function (extension) {

                return fileName.endsWith(
                    extension
                );

            }
        );


    if (!isAllowed) {

        statusMessage.textContent =
            "Please select a PDF, DOCX, or TXT file.";

        selectedFile = null;

        summarizeBtn.disabled = true;

        return;

    }


    selectedFile = file;


    fileNameDisplay.textContent =
        "Selected: " + file.name;


    statusMessage.textContent = "";


    summarizeBtn.disabled = false;

}


// =====================================================
// SUMMARIZE BUTTON
// =====================================================

summarizeBtn.addEventListener(
    "click",
    async function () {


        // -------------------------------------------------
        // CHECK FILE
        // -------------------------------------------------

        if (!selectedFile) {

            statusMessage.textContent =
                "Please select a file first.";

            return;

        }


        // -------------------------------------------------
        // GET SUMMARY LENGTH
        // -------------------------------------------------

        const selectedLength =
            summaryLength.value;


        console.log(
            "Selected Summary Length:",
            selectedLength
        );


        // -------------------------------------------------
        // CREATE FORM DATA
        // -------------------------------------------------

        const formData =
            new FormData();


        formData.append(
            "pdf_file",
            selectedFile
        );


        formData.append(
            "length",
            selectedLength
        );


        // -------------------------------------------------
        // SHOW LOADING
        // -------------------------------------------------

        statusMessage.textContent = "";


        resultBox.classList.add(
            "hidden"
        );


        loader.classList.remove(
            "hidden"
        );


        summarizeBtn.disabled = true;


        // Clear previous translation

        if (translatedResult) {

            translatedResult.textContent = "";

        }


        if (languageSelect) {

            languageSelect.value = "";

        }


        try {

            // =============================================
            // SEND FILE TO FLASK
            // =============================================

            const response =
                await fetch(
                    "/summarize",
                    {
                        method: "POST",
                        body: formData
                    }
                );


            // =============================================
            // GET RESPONSE
            // =============================================

            const responseText =
                await response.text();


            console.log(
                "SERVER RESPONSE:",
                responseText
            );


            // =============================================
            // CONVERT RESPONSE TO JSON
            // =============================================

            let data;


            try {

                data =
                    JSON.parse(
                        responseText
                    );

            }
            catch (jsonError) {

                throw new Error(
                    "Server did not return valid JSON."
                );

            }


            // =============================================
            // CHECK FOR SERVER ERROR
            // =============================================

            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "Server returned an error."
                );

            }


            // =============================================
            // CHECK SUMMARY
            // =============================================

            if (!data.summary) {

                throw new Error(
                    "Summary was not returned by Flask."
                );

            }


            // =============================================
            // STORE ORIGINAL SUMMARY
            // =============================================

            originalSummary =
                data.summary;


            // =============================================
            // DISPLAY HIGHLIGHTED SUMMARY
            // =============================================

            if (data.highlighted_summary) {

                summaryText.innerHTML =
                    data.highlighted_summary;

            }
            else {

                summaryText.textContent =
                    data.summary;

            }


            // =============================================
            // DISPLAY STATISTICS
            // =============================================

            wordStats.textContent =
                "Length: " +
                data.length.toUpperCase() +
                " | Original: " +
                data.original_word_count +
                " words → Summary: " +
                data.summary_word_count +
                " words → Reduction: " +
                data.reduction_percent +
                "%";


            // =============================================
            // SHOW RESULT
            // =============================================

            resultBox.classList.remove(
                "hidden"
            );


            // =============================================
            // DEBUG
            // =============================================

            console.log(
                "Server received length:",
                data.length
            );


            console.log(
                "Highlighted Summary:",
                data.highlighted_summary
            );

        }


        // =============================================
        // ERROR
        // =============================================

        catch (error) {

            console.error(
                "FULL ERROR:",
                error
            );


            statusMessage.textContent =
                "Error: " +
                error.message;

        }


        // =============================================
        // FINALLY
        // =============================================

        finally {

            loader.classList.add(
                "hidden"
            );


            summarizeBtn.disabled =
                false;

        }

    }
);


// =====================================================
// TRANSLATE BUTTON
// =====================================================

if (translateBtn) {

    translateBtn.addEventListener(
        "click",
        async function () {


            // -------------------------------------------------
            // CHECK LANGUAGE
            // -------------------------------------------------

            const targetLanguage =
                languageSelect.value;


            if (!targetLanguage) {

                statusMessage.textContent =
                    "Please select a language.";

                return;

            }


            // -------------------------------------------------
            // CHECK SUMMARY
            // -------------------------------------------------

            if (!originalSummary) {

                statusMessage.textContent =
                    "Please summarize a document first.";

                return;

            }


            // -------------------------------------------------
            // SHOW TRANSLATION LOADING
            // -------------------------------------------------

            translateBtn.disabled = true;

            translateBtn.textContent =
                "Translating...";


            statusMessage.textContent = "";


            try {

                // =============================================
                // SEND SUMMARY TO FLASK
                // =============================================

                const response =
                    await fetch(
                        "/translate",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({

                                text:
                                    originalSummary,

                                target_lang:
                                    targetLanguage

                            })
                        }
                    );


                // =============================================
                // GET RESPONSE
                // =============================================

                const data =
                    await response.json();


                // =============================================
                // CHECK ERROR
                // =============================================

                if (!response.ok) {

                    throw new Error(
                        data.error ||
                        "Translation failed."
                    );

                }


                // =============================================
                // DISPLAY TRANSLATION
                // =============================================

                translatedResult.textContent =
                    data.translated_text;


                console.log(
                    "Translated text:",
                    data.translated_text
                );

            }


            // =============================================
            // TRANSLATION ERROR
            // =============================================

            catch (error) {

                console.error(
                    "TRANSLATION ERROR:",
                    error
                );


                translatedResult.textContent =
                    "Translation error: " +
                    error.message;

            }


            // =============================================
            // FINALLY
            // =============================================

            finally {

                translateBtn.disabled =
                    false;

                translateBtn.textContent =
                    "Translate";

            }

        }
    );

}