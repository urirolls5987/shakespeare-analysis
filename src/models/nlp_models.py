# src/models/nlp_model.py
"""NLP model initialization and management."""

import spacy
from typing import Optional
from pathlib import Path

class NLPModel:
    _instance: Optional['NLPModel'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NLPModel, cls).__new__(cls)
            cls._instance.model = None
        return cls._instance
    
    def initialize(self, model_name: str = 'en_core_web_sm') -> None:
        """Initialize the spaCy model."""
        if self.model is None:
            self.model = spacy.load(model_name)
    
    @property
    def nlp(self):
        """Get the spaCy model instance."""
        if self.model is None:
            self.initialize()
        return self.model

def initialize_nlp(model_name: str = 'en_core_web_sm') -> spacy.language.Language:
    """Initialize and return the NLP model."""
    nlp_model = NLPModel()
    nlp_model.initialize(model_name)
    return nlp_model.nlp