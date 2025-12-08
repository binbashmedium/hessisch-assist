"""Helper to convert text into the Frankfurt dialect."""
from __future__ import annotations

import random
import re

_WORD_MAP = {
    "hallo": "Servus",
    "guten tag": "Gude",
    "guten morgen": "Moije",
    "guten abend": "Gudn Aamd",
    "bitte": "biddscheen",
    "danke": "daaach",
    "danke schön": "merci",
    "entschuldigung": "entschuldisch",
    "hallo zusammen": "Gude zamma",
    "tschüss": "hau rein",
    "auf wiedersehen": "machs gudd",
    "heute": "heit",
    "klein": "klei",
    "gut": "gudd",
    "wasser": "Wasserche",
    "euch": "eisch",
    "euch allen": "eisch all",
}

_FOOD_MAP = {
    "apfel": "Äbbel",
    "apfelsaft": "Äbbelwoi",
    "kartoffel": "Grumbeer",
    "kartoffeln": "Grumbeere",
    "milch": "Millisch",
    "wurst": "Worscht",
    "brot": "Brod",
    "brötchen": "Weck",
    "braten": "Bradde",
    "kuchen": "Kuche",
    "zwiebel": "Zwiwel",
}

_PARTICLES = [
    "gell",
    "hoste",
    "mei Guddzje",
    "aaalda",
]

_PHONETIC_RULES = [
    (re.compile(r"ich\b", re.IGNORECASE), "isch"),
    (re.compile(r"ig\b", re.IGNORECASE), "isch"),
    (re.compile(r"er\b", re.IGNORECASE), "a"),
    (re.compile(r"ch", re.IGNORECASE), "sch"),
]


def _apply_maps(text: str) -> str:
    """Replace words based on dialect maps."""

    def replace_word(match: re.Match[str]) -> str:
        word = match.group(0)
        key = word.lower()
        replacement = _WORD_MAP.get(key) or _FOOD_MAP.get(key)
        if replacement:
            return _preserve_case(word, replacement)
        return word

    pattern = re.compile(r"\\b(" + "|".join(map(re.escape, _WORD_MAP.keys() | _FOOD_MAP.keys())) + r")\\b", re.IGNORECASE)
    return pattern.sub(replace_word, text)


def _preserve_case(original: str, replacement: str) -> str:
    """Preserve capitalization when replacing words."""
    if original.isupper():
        return replacement.upper()
    if original[0].isupper():
        return replacement.capitalize()
    return replacement


def _apply_phonetics(text: str) -> str:
    """Apply phonetic rules for the dialect."""
    transformed = text
    for pattern, repl in _PHONETIC_RULES:
        transformed = pattern.sub(repl, transformed)
    return transformed


def _append_particle(text: str) -> str:
    """Append a dialect particle for extra flair."""
    particle = random.choice(_PARTICLES)
    if text.endswith(('.', '!', '?')):
        return f"{text} {particle}"
    return f"{text}, {particle}"


def convert_to_frankfurt(text: str) -> str:
    """Convert the given text into the Frankfurt dialect."""
    if not text:
        return ""

    working = _apply_maps(text)
    working = _apply_phonetics(working)
    working = working.strip()

    if len(working) > 6:
        working = _append_particle(working)

    return working
