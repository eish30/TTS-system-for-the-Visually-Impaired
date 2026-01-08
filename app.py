import streamlit as st
import os
import tempfile
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

from gtts import gTTS
from pdfminer.high_level import extract_text
from docx import Document
from bs4 import BeautifulSoup
from ebooklib import epub
from striprtf.striprtf import rtf_to_text
from odf.opendocument import load
from odf.text import P

OCR_LANGUAGE_MAP = {
    "en": "eng",
    "hi": "hin",
    "bn": "ben",
    "ta": "tam",
    "te": "tel",
    "fr": "fra",
    "es": "spa",
    "de": "deu"
}

def ocr_pdf(pdf_path, lang_code):
    try:
        images = convert_from_path(pdf_path)
        text = []

        for img in images:
            page_text = pytesseract.image_to_string(img, lang=lang_code)
            text.append(page_text)

        return "\n".join(text)

    except Exception as e:
        st.error(f"OCR Error: {e}")
        return None


def extract_text_from_file(uploaded_file):
    try:
        name = uploaded_file.name
        ext = os.path.splitext(name)[1].lower()

        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp.write(uploaded_file.getbuffer())
            temp_path = tmp.name

        if ext == ".pdf":
            text = extract_text(temp_path)

            if text and text.strip():
                return text
            else:
                st.warning("Scanned PDF detected. Running OCR...")
                ocr_lang = OCR_LANGUAGE_MAP.get(selected_language, "eng")
                return ocr_pdf(temp_path, ocr_lang)

        elif ext in [".txt", ".md"]:
            return uploaded_file.getvalue().decode("utf-8")

        elif ext == ".docx":
            doc = Document(temp_path)
            return "\n".join(p.text for p in doc.paragraphs)

        elif ext in [".html", ".htm"]:
            soup = BeautifulSoup(uploaded_file.getvalue(), "html.parser")
            return soup.get_text(separator="\n")

        elif ext == ".epub":
            book = epub.read_epub(temp_path)
            text = []
            for item in book.get_items():
                if item.get_type() == epub.ITEM_DOCUMENT:
                    soup = BeautifulSoup(item.get_content(), "html.parser")
                    text.append(soup.get_text())
            return "\n".join(text)

        elif ext == ".rtf":
            return rtf_to_text(uploaded_file.getvalue().decode("utf-8", errors="ignore"))

        elif ext == ".odt":
            doc = load(temp_path)
            paragraphs = doc.getElementsByType(P)
            return "\n".join(
                p.firstChild.data if p.firstChild else "" for p in paragraphs
            )

        else:
            st.error("Unsupported file format")
            return None

    except Exception as e:
        st.error(f"Error extracting text: {e}")
        return None


def text_to_speech(text, language="en"):
    tts = gTTS(text=text, lang=language, slow=False)
    audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(audio_file.name)
    return audio_file.name


st.set_page_config(page_title="Universal Document to Speech", layout="centered")

st.title("Universal Document to Speech Converter")
st.write("Upload any text-based document and convert it into spoken audio.")

uploaded_file = st.file_uploader(
    "Upload a document",
    type=["pdf", "txt", "md", "docx", "html", "htm", "epub", "rtf", "odt"]
)

language = st.selectbox(
    "Select language",
    ["en", "hi", "bn", "ta", "te", "fr", "es", "de"]
)
selected_language = language

if uploaded_file:
    with st.spinner("Extracting text..."):
        text = extract_text_from_file(uploaded_file)

    if text and text.strip():
        st.success("Text extracted successfully")

        with st.expander("Preview extracted text"):
            st.text(text[:3000])

        if st.button("Convert to Audio"):
            with st.spinner("Generating audio..."):
                audio_path = text_to_speech(text, language)

            st.success("Audio generated")

            st.audio(audio_path)

            with open(audio_path, "rb") as f:
                st.download_button(
                    "⬇ Download MP3",
                    f,
                    file_name="output.mp3",
                    mime="audio/mpeg"
                )
    else:
        st.error(
            "No readable text found in this document."
        )
