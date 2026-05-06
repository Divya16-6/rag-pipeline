from langdetect import detect
from deep_translator import GoogleTranslator

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

def translate(text, src, tgt):
    if src == tgt:
        return text
    return GoogleTranslator(source=src, target=tgt).translate(text)