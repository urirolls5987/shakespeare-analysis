import streamlit as st
from pathlib import Path
import re
import plotly.graph_objects as go

from src.config.constants import APP_SETTINGS, CACHE_DIR, CSS_PATH, PLAYS_DIR, DEFAULT_PLAY, SHAKESPEARE_PLAYS
from src.models.nlp_models import initialize_nlp
from src.services.pos_tagger import POSTagger
from src.ui.components.navigation import render_navigation
from src.ui.components.text_display import render_text_display
from src.data.loader import fetch_play, load_play
from src.ui.components.character_analysis import render_character_analysis
from src.ui.components.scene_analysis import render_scene_analysis
from src.ui.components.about_page import render_about_page
from src.data.parser import extract_characters, parse_play

import spacy
from pathlib import Path

# Load or download the spaCy model
model_path = Path(spacy.util.get_package_path("en_core_web_sm"))
if not model_path.exists():
    spacy.cli.download("en_core_web_sm")
nlp = spacy.load("en_core_web_sm")


def initialize_session_state():
    """Initialize session state variables."""
    if 'nlp' not in st.session_state:
        st.session_state.nlp = initialize_nlp()
    
    if 'current_play' not in st.session_state:
        st.session_state.current_play = list(SHAKESPEARE_PLAYS.keys())[0]
        

def main():
    """Main application entry point."""
    initialize_session_state()
    
    st.set_page_config(
        page_title="Shakespeare Interactive",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load CSS
    try:
        with open(CSS_PATH, 'r') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Error loading CSS: {str(e)}. Using default styles.")
    
    # Play selection in sidebar
    play_title = st.sidebar.selectbox(
        "Select Play",
        list(SHAKESPEARE_PLAYS.keys()),
        index=list(SHAKESPEARE_PLAYS.keys()).index(st.session_state.current_play),
        key="play_select"
    )
    
    if play_title != st.session_state.current_play:
        st.session_state.current_play = play_title
        st.rerun()
    
    # Load play
    play_url = SHAKESPEARE_PLAYS[play_title]
    cache_path = CACHE_DIR / f"{play_title.lower().replace(' ', '_')}.txt"
    
    try:
        text = fetch_play(play_url, cache_path)
        if not text:
            st.error("Failed to load play text")
            return
            
        toc, acts_scenes = parse_play(text)
        print(toc)
        if not toc or not acts_scenes:
            st.error("Failed to parse play structure")
            return
            
    except Exception as e:
        st.error(f"Error loading play: {str(e)}")
        return
    
    # Initialize services
    pos_tagger = POSTagger(st.session_state.nlp)
    
    # Sidebar navigation
    nav_option = st.sidebar.radio(
        "Navigation",
        ["Table of Contents", "Character Analysis", "Scene Analysis", "About"]
    )
    
    # Render selected view
    if nav_option == "Table of Contents":
        render_text_display(toc, acts_scenes, pos_tagger)
    elif nav_option == "Character Analysis":
        render_character_analysis(acts_scenes, pos_tagger)
    elif nav_option == "Scene Analysis":
        render_scene_analysis(acts_scenes, pos_tagger)
    else:  # About
        render_about_page()
        
if __name__ == "__main__":
    main()