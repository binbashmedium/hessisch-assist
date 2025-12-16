"""
Utilities to convert German text into Hessisch dialect.
Clean, robust and Home-Assistant safe.
"""

from __future__ import annotations

import random
import re
from typing import Dict, Iterable


# ---------------------------------------------------------------------------
# Core dialect mappings
# ---------------------------------------------------------------------------

_WORD_MAP: Dict[str, str] = {
    "ja": "jo",
    "nein": "nee",
    "nicht": "net",
    "nichts": "nix",
    "was": "was",
    "wer": "wer",
    "wo": "wo",
    "wann": "wann",
    "warum": "warum",
    "wie": "wie",

    "hier": "do",
    "dort": "dort",
    "da": "do",
    "drinnen": "drin",
    "draußen": "drauße",

    "heute": "heut",
    "morgen": "morje",
    "gestern": "gestern",
    "jetzt": "jetz",
    "gleich": "gleich",

    "immer": "immer",
    "oft": "oft",
    "vielleicht": "vielleischt",

    "machen": "mache",
    "gehen": "geh",
    "kommen": "komm",
    "sehen": "gucke",
    "hören": "höre",
    "sagen": "sache",
    "arbeiten": "schaffe",
    "schlafen": "penn",

    "viel": "viel",
    "wenig": "wenisch",

    "sehr": "arg",
    "wirklich": "wirlisch",
    "kaputt": "hinne",
}

_FOOD_MAP: Dict[str, str] = {
    "apfelwein": "äbbelwoi",
    "wein": "woi",
    "bier": "bierche",

    "fleisch": "flaisch",
    "schinken": "schinke",
    "käse": "käs",
    "quark": "quarg",

    "suppe": "sobb",
    "soße": "soß",
    "salat": "salad",

    "ei": "ei",
    "eier": "eier",

    "zucker": "zugger",
    "salz": "salz",
}

# ---------------------------------------------------------------------------
# Dialect flavor particles
# ---------------------------------------------------------------------------

_PARTICLES: Iterable[str] = (
    "gell",
    "mei guddzje",
    "ei jo",
    "odder",
)

# ---------------------------------------------------------------------------
# Phonetic rules (applied BEFORE word replacement!)
# ---------------------------------------------------------------------------

_PHONETIC_RULES = [
    (re.compile(r"\bich\b", re.IGNORECASE), "isch"),
    (re.compile(r"\big\b", re.IGNORECASE), "isch"),
    (re.compile(r"\ber\b", re.IGNORECASE), "a"),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _preserve_case(original: str, replacement: str) -> str:
    """Preserve capitalization style of the original token."""
    if original.isupper():
        return replacement.upper()
    if original[:1].isupper():
        return replacement.capitalize()
    return replacement


# ---------------------------------------------------------------------------
# Phonetic processing
# ---------------------------------------------------------------------------

def _apply_phonetics(text: str) -> str:
    """Apply phonetic rules safely (before dictionary replacement)."""
    for pattern, repl in _PHONETIC_RULES:
        text = pattern.sub(repl, text)
    return text


# ---------------------------------------------------------------------------
# Dictionary replacement (phrases + words)
# ---------------------------------------------------------------------------

def _apply_maps(text: str, intensity: int) -> str:
    """
    Replace known words and phrases with Hessisch equivalents.

    Strategy:
    1. Replace multi-word phrases first
    2. Replace single words with punctuation awareness
    """

    # -----------------------------
    # 1️⃣ Multi-word phrases first
    # -----------------------------
    phrase_keys = sorted(
        (k for k in _WORD_MAP if " " in k),
        key=len,
        reverse=True,
    )

    for key in phrase_keys:
        pattern = re.compile(re.escape(key), re.IGNORECASE)

        def phrase_replace(match: re.Match[str]) -> str:
            repl = _WORD_MAP[key]
            if intensity >= 3:
                repl += "!"
            return _preserve_case(match.group(0), repl)

        text = pattern.sub(phrase_replace, text)

    # -----------------------------
    # 2️⃣ Single words
    # -----------------------------
    word_map = {**_WORD_MAP, **_FOOD_MAP}
    single_words = sorted(
        (k for k in word_map if " " not in k),
        key=len,
        reverse=True,
    )

    pattern = re.compile(
        r"\b(" + "|".join(map(re.escape, single_words)) + r")\b(?=[\s.,!?]|$)",
        re.IGNORECASE,
    )

    def word_replace(match: re.Match[str]) -> str:
        word = match.group(0)
        key = word.lower()
        repl = word_map.get(key, word)

        if intensity >= 3:
            repl += "!"

        return _preserve_case(word, repl)

    return pattern.sub(word_replace, text)


# ---------------------------------------------------------------------------
# Flavor additions
# ---------------------------------------------------------------------------

def _intensity_prefix(text: str, intensity: int) -> str:
    if intensity == 1:
        return text
    if intensity == 2:
        return f"Ei {text}" if not text.lower().startswith("ei") else text
    return f"Ei jo, {text}" if not text.lower().startswith("ei jo") else text


def _append_particles(text: str, intensity: int) -> str:
    if not text:
        return text

    count = 1 if intensity == 1 else 2 if intensity == 2 else 3
    chosen = random.sample(list(_PARTICLES), k=count)
    suffix = ", ".join(chosen)

    if text.endswith((".", "!", "?")):
        return f"{text} {suffix}"
    return f"{text}, {suffix}"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def convert_to_hessisch(text: str) -> str:
    """Convert a German sentence into Hessisch dialect."""
    if not text:
        return ""

    intensity = random.randint(1, 3)

    working = text.strip()
    working = _apply_phonetics(working)
    working = _apply_maps(working, intensity)
    working = _intensity_prefix(working, intensity)

    if len(working) > 4:
        working = _append_particles(working, intensity)

    return working
