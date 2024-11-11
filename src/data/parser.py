# parser.py

import re
from typing import Dict, List, Tuple

# from src.data.loader import clean_gutenberg_text
from src.utils.text_processing import to_roman, clean_gutenberg_text

def extract_play_structure(text: str) -> Tuple[List[Dict], Dict[str, Dict[str, str]]]:
    """
    Parse a play text into a structured format with acts and scenes.
    
    Args:
        text (str): The full text of the play
    
    Returns:
        Tuple containing:
        - List of dictionaries representing table of contents
        - Dictionary of acts and scenes with their content
    """
    
    # Initialize data structures
    toc = []  # Table of contents
    acts_scenes = {}  # Dictionary to store act/scene content
    current_act = ""
    current_scene = ""
    scene_content = []
    
    # Split text into lines
    text = text[text.find("Dramatis Personæ"):-1]
    lines = text.split('\n')
    
    # Regular expressions for matching act and scene headers
    act_pattern = re.compile(r'^ACT [IVX]+')
    scene_pattern = re.compile(r'^SCENE [IVX]+\.')
    
    
    # Process each line
    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
            
        # Check for new act
        act_match = act_pattern.match(line)
        if act_match:
            # Save previous scene if exists
            if current_act and current_scene:
                if current_act not in acts_scenes:
                    acts_scenes[current_act] = {}
                acts_scenes[current_act][current_scene] = '\n'.join(scene_content)
            
            current_act = line
            scene_content = []
            toc.append({"act": current_act, "scenes": []})
            continue
            
        # Check for new scene
        scene_match = scene_pattern.match(line)
        if scene_match:
            # Save previous scene if exists
            if current_act and current_scene:
                if current_act not in acts_scenes:
                    acts_scenes[current_act] = {}
                acts_scenes[current_act][current_scene] = '\n'.join(scene_content)
            
            current_scene = line
            scene_content = []
            if toc:  # Make sure we have an act to add the scene to
                toc[-1]["scenes"].append(current_scene)
            continue
        
        # Add line to current scene content
        if current_act and current_scene:
            scene_content.append(line)
    
    # Save the last scene
    if current_act and current_scene and scene_content:
        if current_act not in acts_scenes:
            acts_scenes[current_act] = {}
        acts_scenes[current_act][current_scene] = '\n'.join(scene_content)
    
    return toc, acts_scenes

def parse_play(text: str) -> Tuple[List[Dict], Dict[str, Dict[str, str]]]:
    """Parse play text into structured format."""
    # Remove any remaining Gutenberg artifacts
    text = clean_gutenberg_text(text)
    
    # Extract play structure
    return extract_play_structure(text)


def extract_stage_directions(text: str) -> List[str]:
    """
    Extract stage directions from the text.
    
    Args:
        text (str): Scene text
        
    Returns:
        List of stage directions
    """
    # Look for text in square brackets or parentheses
    stage_directions = re.findall(r'\[(.*?)\]|\((.*?)\)', text)
    # Flatten the list of tuples and remove empty strings
    return [direction for tuple_pair in stage_directions for direction in tuple_pair if direction]

def extract_characters(text: str) -> List[str]:
    """
    Extract character names from the scene.
    
    Args:
        text (str): Scene text
        
    Returns:
        List of unique character names
    """
    # Look for lines that start with character names (in all caps)
    characters = re.findall(r'^([A-Z]{2,}[A-Z\s]*?)\.', text, re.MULTILINE)
    return list(set(characters))

# def get_character_lines(text: str, character: str) -> List[str]:
#     """
#     Get all lines spoken by a specific character.
    
#     Args:
#         text (str): Scene text
#         character (str): Character name
        
#     Returns:
#         List of character's lines
#     """
#     # Find all lines that follow the character's name
#     pattern = f"{character}\\.(.*?)(?=[A-Z]{{2,}}\\.|$)"
#     lines = re.findall(pattern, text, re.DOTALL | re.MULTILINE)
#     return [line.strip() for line in lines]

def get_character_lines(text: str, character: str) -> List[str]:
    """
    Get all lines spoken by a specific character.
    
    Args:
        text (str): Scene text
        character (str): Character name
        
    Returns:
        List of character's lines
    """
    # Find all lines that follow the character's name
    pattern = f"{character}\\.(.*?)(?=[A-Z]{{2,}}\\.|$)"
    lines = re.findall(pattern, text, re.DOTALL | re.MULTILINE)
    return [line.strip() for line in lines]

def generate_character_network(text):
    """Generate character interaction network"""
    characters = extract_characters(text)
    # Create links between characters that appear in same scenes
    links = []
    for char1 in characters:
        for char2 in characters:
            if char1 != char2:
                if re.search(f"{char1}.*{char2}|{char2}.*{char1}", text, re.MULTILINE):
                    links.append((char1, char2))
    return characters, links

if __name__ == "__main__":
    # Example usage
    with open("/Users/urirolls/urirolls/Cardenio/Cardenio/statistical_breakdown/plays/hamlet.txt", "r", encoding="utf-8") as f:
        play_text = f.read()
    
    toc, acts_scenes = parse_play(play_text)
    
    # Print table of contents
    for act in toc:
        print(f"\n{act['act']}")
        for scene in act['scenes']:
            print(f"  {scene}")
            
    total_lines = 0
    character_lines = []
    for act in acts_scenes:
        for scene in acts_scenes[act]:
            lines = get_character_lines(acts_scenes[act][scene], "HAMLET")
            if lines:
                print(f"\n{act} - {scene}")
                print('\n'.join(lines))
            character_lines.extend(lines)
            total_lines += len(lines)
    # get_character_lines(acts_scenes['ACT I']['SCENE I.'], 'FRANCISCO')