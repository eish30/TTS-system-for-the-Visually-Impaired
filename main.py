from pdfminer.high_level import extract_text
from gtts import gTTS
import speech_recognition as sr
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from docx import Document
from bs4 import BeautifulSoup
from ebooklib import epub
from striprtf.striprtf import rtf_to_text
from odf.opendocument import load
from odf.text import P
import os

def text_from_file(file_path):
    try:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            return extract_text(file_path)
        elif ext in ['.txt', '.md']:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        elif ext == '.docx':
            doc = Document(file_path)
            return '\n'.join(p.text for p in doc.paragraphs)
        elif ext in ['.html', '.htm']:
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                return soup.get_text(separator='\n')
        elif ext == '.epub':
            book = epub.read_epub(file_path)
            text = []
            for item in book.get_items():
                if item.get_type() == epub.ITEM_DOCUMENT:
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    text.append(soup.get_text())
            return '\n'.join(text)
        elif ext == '.rtf':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return rtf_to_text(f.read())
        elif ext == '.odt':
            doc = load(file_path)
            paragraphs = doc.getElementsByType(P)
            return '\n'.join(p.firstChild.data if p.firstChild else '' for p in paragraphs)

        else:
            print("Unsupported file format.")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def text_to_speech(text, output_file='output.mp3', language='en'):
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(output_file)
        return output_file
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak Now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"Text from speech: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Error: {e}")
        return None
    
def text_to_pdf(text, output_file='output.pdf'):
    try:
        with open(output_file, 'w') as file:
            file.write(text)
        print(f"Text saved to PDF: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error: {e}")
        return None

while True:
    print("\nChoose an option at Flood:")
    print("1. PDF Text to Audio")
    print("2. Audio Text to PDF")
    print("3. Exit")
    choice = input("Choice 1/2/3: ")
    if choice == '1':
        file_path = input("Enter document path: ")
        user_extracted_text = text_from_file(file_path)
        if user_extracted_text:
            user_output_file_audio = text_to_speech(user_extracted_text)
            if user_output_file_audio:
                os.system(f"start {user_output_file_audio}")
    elif choice == '2':
        extracted_text_from_speech = speech_to_text()
        if extracted_text_from_speech:
            output_file_pdf = text_to_pdf(extracted_text_from_speech)
            if output_file_pdf:
                print(f"Text converted from speech to PDF. Output file: {output_file_pdf}")
    elif choice == '3':
        print("Exiting the program. Thank you!")
        break
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
