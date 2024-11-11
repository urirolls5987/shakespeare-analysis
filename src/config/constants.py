from pathlib import Path
# src/config/constants.py
"""Constants and configuration values for the Shakespeare Interactive application."""

from typing import Dict

# src/config/constants.py
# Add this to your constants
SHAKESPEARE_PLAYS = {
    "Hamlet": "http://www.gutenberg.org/cache/epub/1524/pg1524.txt",
    "Macbeth": "http://www.gutenberg.org/cache/epub/2264/pg2264.txt",
    "Romeo and Juliet": "http://www.gutenberg.org/cache/epub/1513/pg1513.txt",
    "A Midsummer Night's Dream": "http://www.gutenberg.org/cache/epub/1514/pg1514.txt",
    "The Tempest": "http://www.gutenberg.org/cache/epub/2235/pg2235.txt",
    "King Lear": "http://www.gutenberg.org/cache/epub/1532/pg1532.txt",
    "Othello": "http://www.gutenberg.org/cache/epub/2267/pg2267.txt",
    "Julius Caesar": "http://www.gutenberg.org/cache/epub/1120/pg1120.txt",
    "The Merchant of Venice": "http://www.gutenberg.org/cache/epub/2243/pg2243.txt",
    "Much Ado About Nothing": "http://www.gutenberg.org/cache/epub/1519/pg1519.txt"
}

CACHE_DIR = Path("cache/plays")


# POS tag colors for visualization
POS_COLORS: Dict[str, str] = {
    'NOUN': 'green',
    'VERB': 'red',
    'ADJ': 'blue',
    'ADV': 'cyan',
    'PRON': 'magenta',
    'DET': 'yellow',
    'ADP': 'blue',
    'AUX': 'red',
    'CCONJ': 'purple',
    'INTJ': 'orange',
    'NUM': 'yellow',
    'PART': 'green',
    'PROPN': 'pink',
    'PUNCT': 'grey',
    'SCONJ': 'blue',
    'SYM': 'grey',
    'X': 'grey',
}

# POS tag descriptions for legend
POS_DESCRIPTIONS: Dict[str, str] = {
    'NOUN': 'Noun - person, place, thing, or idea',
    'VERB': 'Verb - action or state of being',
    'ADJ': 'Adjective - describes a noun',
    'ADV': 'Adverb - modifies verb, adjective, or other adverb',
    'PRON': 'Pronoun - replaces a noun',
    'DET': 'Determiner - introduces a noun',
    'ADP': 'Adposition - preposition or postposition',
    'AUX': 'Auxiliary - helping verb',
    'CCONJ': 'Coordinating Conjunction - connects words, phrases, clauses',
    'INTJ': 'Interjection - exclamation',
    'NUM': 'Number - numerical value',
    'PART': 'Particle - function word',
    'PROPN': 'Proper Noun - specific name',
    'PUNCT': 'Punctuation - punctuation marks',
    'SCONJ': 'Subordinating Conjunction - connects clauses',
    'SYM': 'Symbol - mathematical or scientific symbol',
    'X': 'Other - other word category',
}

# Display mode descriptions
DISPLAY_MODES: Dict[str, str] = {
    "colored_text": "Colored Text (words in POS colors)",
    "plain_tags": "Plain Tags (word[POS])",
    "colored_tags": "Colored Tags (POS tags in colors)",
    "tag_only": "Tags Only (POS tags without colors)"
}

# Default display options
DEFAULT_DISPLAY_OPTIONS = ["Show Stage Directions"]

# Application settings
APP_SETTINGS = {
    "page_title": "Shakespeare Interactive",
    "page_icon": "📚",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# File paths
PLAYS_DIR = "plays"
DEFAULT_PLAY = "hamlet.txt"
CSS_PATH = "src/config/styles.css"