import pandas as pd
import streamlit as st
import pdfplumber
from gtts import gTTS
import os
import tempfile
from streamlit_option_menu import option_menu

# Create the Streamlit app
st.set_page_config(page_title="PDF to Audio Converter", layout="wide")

# Navigation bar
with st.sidebar:
    selected = option_menu("Main Menu", ["Home", "About", "Upload File"],
                           icons=["house", "info-circle", "cloud-upload"],
                           menu_icon="cast", default_index=0)

# Home section
if selected == "Home":
    st.title('Welcome to PDF to Audio Converter')
    st.write("Use the navigation bar to switch between sections.")

# About section
elif selected == "About":
    st.title('About')
    st.write('''Experience the future of communication with our cutting-edge text-to-speech technology. 
    Transform your written words into captivating audio experiences that resonate with your audience.

    Instant Transformation: Watch as your text is seamlessly converted into natural-sounding speech, delivered with precision and clarity.
    Unmatched Versatility: From engaging presentations to accessible content, our TTS solution adapts to your every need.
    Lifelike Voices: Immerse yourself in a world of authentic voices that bring your message to life.
    Global Reach: Break language barriers and connect with audiences worldwide through our diverse range of accents and languages.
    Whether you're aiming to enhance accessibility, boost engagement, or simply streamline your workflow, our text-to-speech technology is your ultimate companion.''')

# Upload File section
elif selected == "Upload File":
    st.title('Upload PDF File')
    
    # PDF extraction using pdfplumber
    def extract_text_from_pdf(pdf_path):
        """
        Extract text from a PDF file.

        Args:
            pdf_path (str): Path to the PDF file.

        Returns:
            str: Extracted text.
        """
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
            return text
        except Exception as e:
            st.error(f"Error extracting text from PDF: {e}")
            return None

    # Extracted text save to CSV
    def save_text_to_csv(text, csv_path):
        """
        Save text to a CSV file.

        Args:
            text (str): Text to save.
            csv_path (str): Path to the CSV file.
        """
        try:
            df = pd.DataFrame({"Text": [text]})
            df.to_csv(csv_path, index=False)
        except Exception as e:
            st.error(f"Error saving text to CSV: {e}")

    # Convert text to speech
    def text_to_speech(text, audio_path):
        """
        Convert text to speech and save as an audio file.

        Args:
            text (str): Text to convert.
            audio_path (str): Path to the audio file.
        """
        try:
            tts = gTTS(text)
            tts.save(audio_path)
        except Exception as e:
            st.error(f"Error converting text to speech: {e}")

    # File uploader section
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_file_path = temp_file.name

        # Extract text from PDF
        extract_text = extract_text_from_pdf(temp_file_path)

        if extract_text:
            # Display extracted text
            st.header('Extracted Text')
            st.text_area('Extracted Text from PDF', extract_text, height=300)

            # Save extracted text to CSV
            csv_file_path = "extracted_text.csv"
            save_text_to_csv(extract_text, csv_file_path)

            # Convert text to speech
            audio_file_path = "text_to_speech.mp3"
            text_to_speech(extract_text, audio_file_path)

            # Read the audio data
            with open(audio_file_path, 'rb') as audio_file:
                audio_data = audio_file.read()

            # Display the audio file
            st.header('Audio File')
            st.audio(audio_data, format='audio/mp3')

            # Create a downloadable audio file
            st.header('Downloadable Audio File')
            st.download_button('Download Audio File', audio_data, file_name='text_to_speech.mp3')

            # Clean up temporary files
            os.remove(temp_file_path)
            os.remove(audio_file_path)
        else:
            st.error("Failed to extract text from the PDF file. Please check the file and try again.")
