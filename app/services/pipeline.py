from .tokenizer import tokenize_text
from .spellchecker import correct_word

def correct_paragraph(text: str):
    """Full pipeline: tokenize → spellcheck → reconstruct."""
    tokens = tokenize_text(text)
    corrected = [correct_word(tok) for tok in tokens]
    return "".join(corrected)