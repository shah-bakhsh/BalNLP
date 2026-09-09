import unicodedata

import regex

from .exceptions import BalNLPError
from .schemas import Token

# Preserve marks, joiners and all Balochi letters; separate punctuation, retain offsets.
WORD_PATTERN = regex.compile(r"[\p{L}\p{N}\p{M}\u200c\u200d]+|[^\s]", regex.VERSION1)
SENTENCE_END = {".", "!", "?", "؟", "۔"}


def normalize_text(text: str, max_length: int = 2000) -> str:
    if not isinstance(text, str) or not text.strip():
        raise BalNLPError("INVALID_TEXT", "Please enter Balochi text.")
    if len(text) > max_length:
        raise BalNLPError("TEXT_TOO_LONG", f"Please use at most {max_length} characters.")
    if any(unicodedata.category(c) == "Cc" and c not in "\n\r\t" for c in text):
        raise BalNLPError("INVALID_TEXT", "Please remove unsupported control characters.")
    normalized = unicodedata.normalize("NFC", text)
    if not any(unicodedata.category(c)[0] in {"L", "N"} for c in normalized):
        raise BalNLPError("INVALID_TEXT", "Please enter a sentence containing words.")
    return normalized


def tokenize_balochi(text: str) -> list[Token]:
    text = unicodedata.normalize("NFC", text)
    tokens: list[Token] = []
    sentence = 1
    for match in WORD_PATTERN.finditer(text):
        if tokens:
            gap = text[tokens[-1].end : match.start()]
            if "\n" in gap or tokens[-1].form in SENTENCE_END:
                sentence += 1
        tokens.append(
            Token(
                id=len(tokens) + 1,
                form=match.group(),
                start=match.start(),
                end=match.end(),
                sentence_id=sentence,
            )
        )
    return tokens
