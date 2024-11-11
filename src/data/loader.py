# src/data/loader.py
from pathlib import Path
from typing import Tuple, Dict, Any

# src/data/loader.py
import requests
from pathlib import Path
import streamlit as st
from typing import Tuple, Dict, Optional
import re
from src.utils.text_processing import clean_gutenberg_text
from src.data.parser import parse_play

@st.cache_data
def fetch_play(url: str, cache_path: Path) -> str:
    """Fetch play from Gutenberg or cache."""
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    
    if cache_path.exists():
        return cache_path.read_text(encoding='utf-8')
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        text = response.text
        
        clean_text = clean_gutenberg_text(text)
        cache_path.write_text(clean_text, encoding='utf-8')
        
        return clean_text
    except Exception as e:
        st.error(f"Error fetching play: {str(e)}")
        return ""
    
def get_available_plays():
    """Get list of available plays in the plays directory."""
    plays_dir = Path('plays')
    if not plays_dir.exists():
        return []
    return [f.name for f in plays_dir.glob('*.txt')]

def load_play(file_path: str) -> Tuple[list, Dict[str, Dict[str, str]]]:
    """
    Load and parse a play file.
    
    Args:
        file_path: String path to the play file
        
    Returns:
        Tuple containing table of contents and acts/scenes dictionary
    """
    try:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Play file not found: {file_path}")
            
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
            
        return parse_play(text)
    except FileNotFoundError:
        raise FileNotFoundError(f"Play file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading play: {str(e)}")
    
if __name__ == "__main__":
    from pathlib import Path
    import sys
    from pprint import pprint
    from src.config.constants import SHAKESPEARE_PLAYS, CACHE_DIR
    from src.data.parser import parse_play
    from src.data.parser import extract_characters

    def debug_play_structure(play_title: str, verbose: bool = False):
        """Debug the loading and parsing of a play."""
        print(f"\n{'='*20} Debugging {play_title} {'='*20}")
        
        # Get URL and setup cache path
        url = SHAKESPEARE_PLAYS[play_title]
        cache_path = CACHE_DIR / f"{play_title.lower().replace(' ', '_')}.txt"
        print(f"URL: {url}")
        print(f"Cache path: {cache_path}")
        
        # Try loading the play
        print("\nFetching play...")
        try:
            text = fetch_play(url, cache_path)
            print(f"Text length: {len(text)}")
            if verbose:
                print("\nFirst 500 characters:")
                print("-" * 50)
                print(text[:500])
                print("-" * 50)
            
            # Look for act/scene markers
            print("\nChecking for structure markers:")
            act_matches = re.findall(r'ACT [IVX]+', text)
            scene_matches = re.findall(r'SCENE [IVX]+', text)
            print(f"Found {len(act_matches)} act markers: {act_matches[:5]}")
            print(f"Found {len(scene_matches)} scene markers: {scene_matches[:5]}")
            
            # Try parsing
            print("\nParsing play structure...")
            toc, acts_scenes = parse_play(text)
            
            print("\nTable of Contents:")
            pprint(toc)
            
            print("\nAct/Scene structure:")
            for act in acts_scenes:
                print(f"\n{act}:")
                for scene in acts_scenes[act]:
                    scene_text = acts_scenes[act][scene]
                    print(f"  {scene}: {len(scene_text)} characters")
                    if verbose:
                        print(f"    First 100 chars: {scene_text[:100]}")
            
            # Check for characters
            print("\nChecking for characters:")
            all_characters = set()
            for act in acts_scenes:
                for scene in acts_scenes[act]:
                    scene_chars = extract_characters(acts_scenes[act][scene])
                    all_characters.update(scene_chars)
            print(f"Found {len(all_characters)} unique characters:")
            pprint(sorted(list(all_characters)))
            
        except Exception as e:
            print(f"\nERROR: {str(e)}")
            import traceback
            traceback.print_exc()

    # Command line arguments
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    
    if len(sys.argv) > 1 and sys.argv[1] in SHAKESPEARE_PLAYS:
        # Debug specific play
        debug_play_structure(sys.argv[1], verbose)
    else:
        # List available plays
        print("\nAvailable plays:")
        for i, play in enumerate(SHAKESPEARE_PLAYS.keys(), 1):
            print(f"{i}. {play}")
        
        # Debug first play as example
        print("\nDebugging first play as example...")
        debug_play_structure(list(SHAKESPEARE_PLAYS.keys())[0], verbose)