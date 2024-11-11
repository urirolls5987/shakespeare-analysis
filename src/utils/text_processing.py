"""Utility functions for text processing."""

import re
from typing import List, Set, Dict, Any

def clean_text(text: str) -> str:
    """Clean and normalize text."""
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text

def split_into_sentences(text: str) -> List[str]:
    """Split text into sentences."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

def extract_tokens(text: str) -> List[str]:
    """Extract individual tokens from text."""
    return re.findall(r'\b\w+\b', text)

def count_words(text: str) -> Dict[str, int]:
    """Count word frequencies in text."""
    words = extract_tokens(text.lower())
    return {word: words.count(word) for word in set(words)}

def format_line_numbers(text: str) -> str:
    """Add line numbers to text."""
    lines = text.split('\n')
    return '\n'.join(f"{i+1:>4} {line}" for i, line in enumerate(lines))

def count_syllables(word: str) -> int:
    """
    Count syllables in a word using a basic rule-based approach.
    """
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    
    # Handle special cases
    if not word: return 0
    if word.endswith('e'): word = word[:-1]
    
    # Count vowel groups
    prev_char_is_vowel = False
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_char_is_vowel:
            count += 1
        prev_char_is_vowel = is_vowel
    
    # Handle special cases
    if count == 0: count = 1
    
    return count


def to_roman(num: int) -> str:
    """Convert integer to Roman numeral."""
    roman_values = [
        (1000, 'M'),
        (900, 'CM'),
        (500, 'D'),
        (400, 'CD'),
        (100, 'C'),
        (90, 'XC'),
        (50, 'L'),
        (40, 'XL'),
        (10, 'X'),
        (9, 'IX'),
        (5, 'V'),
        (4, 'IV'),
        (1, 'I')
    ]
    
    result = ''
    for value, numeral in roman_values:
        while num >= value:
            result += numeral
            num -= value
    return result

def from_roman(roman: str) -> int:
    """Convert Roman numeral to integer."""
    roman_values = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }
    
    total = 0
    prev_value = 0
    
    for char in reversed(roman.upper()):
        curr_value = roman_values[char]
        if curr_value >= prev_value:
            total += curr_value
        else:
            total -= curr_value
        prev_value = curr_value
        
    return total


def clean_gutenberg_text(text: str) -> str:
    """Remove Project Gutenberg header and footer."""
    start_markers = [
        "*** START OF THE PROJECT GUTENBERG",
        "*** START OF THIS PROJECT GUTENBERG",
        "End of Project Gutenberg's",
    ]
    end_markers = [
        "*** END OF THE PROJECT GUTENBERG",
        "*** END OF THIS PROJECT GUTENBERG",
        "End of Project Gutenberg's",
    ]
    
    # Find start of play
    start_pos = 0
    for marker in start_markers:
        pos = text.find(marker)
        if pos != -1:
            start_pos = text.find("\n", pos) + 1
            break
    
    # Find end of play
    end_pos = len(text)
    for marker in end_markers:
        pos = text.find(marker)
        if pos != -1:
            end_pos = pos
            break
    
    return text[start_pos:end_pos].strip()
