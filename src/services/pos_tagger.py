from typing import List, Dict
import spacy
import html
import re
from src.config.constants import POS_COLORS, POS_DESCRIPTIONS

class POSTagger:
    def __init__(self, nlp_model: spacy.language.Language):
        self.nlp = nlp_model
    
    def process_text(self, text: str, mode: str = 'colored_text') -> str:
        """Process text with different POS visualization modes."""
        # Split into lines while preserving HTML
        lines = text.split('\n')
        processed_lines = []
        
        for line in lines:
            if not line.strip():
                processed_lines.append('')
                continue
                
            # Preserve line numbers and character names
            prefix = ''
            main_text = line
            
            # Extract line number if present
            line_num_match = re.match(r'<span class="line-number">(\d+)</span>', line)
            if line_num_match:
                prefix = line_num_match.group(0)
                main_text = line[len(prefix):]
            
            # Handle character names
            char_name_match = re.search(r'<span class="character-name">(.*?)</span>', main_text)
            if char_name_match:
                char_part = char_name_match.group(0)
                main_text = main_text.replace(char_part, '')
                prefix += char_part
            
            # Process the main text
            doc = self.nlp(main_text)
            
            if mode == 'colored_text':
                processed_tokens = [
                    f'<span style="color: {POS_COLORS.get(token.pos_, "#e0e0e0")}">{html.escape(token.text)}</span>'
                    for token in doc
                ]
                processed_lines.append(f"{prefix}{' '.join(processed_tokens)}")
            elif mode == 'colored_tags':
                processed_tokens = [
                    f'<span style="color: {POS_COLORS.get(token.pos_, "#e0e0e0")}">{token.pos_}</span>'
                    for token in doc
                ]
                processed_lines.append(f"{prefix}{' '.join(processed_tokens)}")
            
        return '\n'.join(processed_lines)