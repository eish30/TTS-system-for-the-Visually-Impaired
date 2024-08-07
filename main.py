import PyPDF2
import pandas as pd
from gtts import gTTS
import os

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text.
    """
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_path)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

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
        print(f"Error saving text to CSV: {e}")

def save_text_to_xml(text, xml_path):
    """
    Save text to an XML file.

    Args:
        text (str): Text to save.
        xml_path (str): Path to the XML file.
    """
    try:
        df = pd.DataFrame({"Text": [text]})
        df.to_xml(xml_path, index=False)
    except Exception as e:
        print(f"Error saving text to XML: {e}")

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
        print(f"Error converting text to speech: {e}")

def main():
    # Define file paths
    pdf_path = "resume harshita.pdf"  # Path to your PDF file
    csv_path = "output.csv"  # Path to save CSV file
    xml_path = "output.xml"  # Path to save XML file
    audio_path = "output.mp3"  # Path to save audio file

    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    
    if text is not None:
        # Save text to CSV
        save_text_to_csv(text, csv_path)
        
        # Save text to XML
        save_text_to_xml(text, xml_path)
        
        # Convert text to speech and save as audio file
        text_to_speech(text, audio_path)
        
        print("Processing complete.")
    else:
        print("Error processing PDF file.")

if __name__ == "__main__":
    main()
