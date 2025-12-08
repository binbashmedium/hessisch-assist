"""Utilities to convert text into Hessisch dialect."""
from __future__ import annotations

import random
import re
from typing import Dict, Iterable

# Core dialect word mappings
_WORD_MAP: Dict[str, str] = {
    "hallo": "gude",
    "guten tag": "gude",
    "guten morgen": "moije",
    "guten abend": "gude owe",
    "tschüss": "mach's gudd",
    "auf wiedersehen": "mach's fei gudd",
    "danke": "merci",
    "bitte": "biddschee",
    "entschuldigung": "entschuldisch",
    "klein": "klei",
    "groß": "grob",
    "schnell": "flinks",
    "langsam": "lambsam",
    "wasser": "wasserche",
    "gut": "gudd",
    "fertig": "ferdisch",
    "kalt": "kald",
    "warm": "woarm",
}

# Food related words typical for Hessian region
_FOOD_MAP: Dict[str, str] = {
    "apfel": "äbbel",
    "apfelsaft": "äbbelwoi",
    "kartoffel": "grumbeer",
    "kartoffeln": "grumbeere",
    "milch": "millisch",
    "kaffee": "kaffeeche",
    "wurst": "worscht",
    "brot": "brod",
    "brötchen": "weck",
    "kuchen": "kuche",
    "zwiebel": "zwiwel",
    "zwiebeln": "zwiwele",
}

# Dialect particles for flavor
_PARTICLES: Iterable[str] = (
    "gell",
    "hoschd",
    "mei guddzje",
    "aaldä",
    "ei jo",
    "odder",
)

# Phonetic substitutions to reflect Hessisch pronunciation
_PHONETIC_RULES = [
    (re.compile(r"ich\b", re.IGNORECASE), "isch"),
    (re.compile(r"ig\b", re.IGNORECASE), "isch"),
    (re.compile(r"er\b", re.IGNORECASE), "a"),
    (re.compile(r"ch", re.IGNORECASE), "sch"),
]


def _preserve_case(original: str, replacement: str) -> str:
    """Return replacement with capitalization matching the original word."""
    if original.isupper():
        return replacement.upper()
    if original[:1].isupper():
        return replacement.capitalize()
    return replacement


def _apply_maps(text: str, intensity: int) -> str:
    """Replace words based on dialect maps with optional intensity boost."""

    all_keys = set(_WORD_MAP.keys()) | set(_FOOD_MAP.keys())
    pattern = re.compile(r"\\b(" + "|".join(map(re.escape, all_keys)) + r")\\b", re.IGNORECASE)

    def replace(match: re.Match[str]) -> str:
        word = match.group(0)
        key = word.lower()
        replacement = _WORD_MAP.get(key) or _FOOD_MAP.get(key)
        if not replacement:
            return word
        # higher intensity may add emphasis via exclamation
        adjusted = replacement
        if intensity >= 3 and not replacement.endswith("!"):
            adjusted = f"{replacement}!"
        return _preserve_case(word, adjusted)

    return pattern.sub(replace, text)


def _apply_phonetics(text: str) -> str:
    """Apply phonetic shifts to approximate Hessisch sounds."""
    processed = text
    for pattern, repl in _PHONETIC_RULES:
        processed = pattern.sub(repl, processed)
    return processed


def _append_particles(text: str, intensity: int) -> str:
    """Append dialect particles depending on intensity."""
    if not text:
        return text

    particle_count = 1 if intensity == 1 else 2 if intensity == 2 else 3
    chosen = random.sample(list(_PARTICLES), k=min(particle_count, len(_PARTICLES)))
    suffix = ", ".join(chosen)

    if text.endswith((".", "!", "?")):
        return f"{text} {suffix}"
    return f"{text}, {suffix}"


def _intensity_prefix(text: str, intensity: int) -> str:
    """Optionally add a small intro word for stronger dialect."""
    if intensity == 1:
        return text
    if intensity == 2:
        return f"Ei {text}" if not text.lower().startswith("ei") else text
    return f"Ei jo, {text}" if not text.lower().startswith("ei jo") else text


def convert_to_hessisch(text: str) -> str:
    """Convert a plain response into Hessisch dialect with random intensity."""
    if not text:
        return ""

    intensity = random.randint(1, 3)

    working = _apply_maps(text, intensity)
    working = _apply_phonetics(working)
    working = working.strip()
    working = _intensity_prefix(working, intensity)

    if len(working) > 4:
        working = _append_particles(working, intensity)

    return working
