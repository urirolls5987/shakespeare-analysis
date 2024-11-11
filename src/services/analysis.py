from typing import List, Dict, Any
from collections import Counter
import spacy

from src.utils.text_processing import count_syllables

def analyze_sentiment(text: str, nlp: spacy.language.Language) -> float:
    """Analyze sentiment of text."""
    doc = nlp(text)
    return sum([token.sentiment for token in doc if hasattr(token, 'sentiment')]) / len(doc)

def analyze_complexity(text: str, nlp: spacy.language.Language) -> Dict[str, float]:
    """Analyze text complexity metrics."""
    doc = nlp(text)
    sentences = list(doc.sents)
    
    return {
        "avg_sentence_length": sum(len(sent) for sent in sentences) / len(sentences),
        "avg_word_length": sum(len(token.text) for token in doc) / len(doc),
        "unique_words_ratio": len(set(token.text.lower() for token in doc)) / len(doc),
        "complexity_score": calculate_complexity_score(doc)
    }

def calculate_complexity_score(doc: spacy.tokens.Doc) -> float:
    """Calculate overall text complexity score."""
    # Implementation of complexity scoring algorithm
    syllable_count = sum(count_syllables(token.text) for token in doc)
    word_count = len(doc)
    sentence_count = len(list(doc.sents))
    
    return (syllable_count / word_count * 100 + word_count / sentence_count) / 2
