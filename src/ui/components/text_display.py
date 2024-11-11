# src/ui/components/text_display.py
"""Text display component."""
import streamlit as st
import re
import html
from typing import List, Dict
from src.services.pos_tagger import POSTagger
from src.config.constants import DISPLAY_MODES, POS_COLORS, POS_DESCRIPTIONS
from src.data.parser import extract_stage_directions, extract_characters
from src.data.loader import get_available_plays

def render_text_display(toc: list, acts_scenes: Dict[str, Dict[str, str]], 
                       pos_tagger: POSTagger) -> None:
    """Render text display with all display options."""
    if not toc or not acts_scenes:
        st.error("No play data available")
        return

    # Scene selection
    st.markdown("### Navigation")
    col1, col2 = st.columns(2)
    
    with col1:
        available_acts = [item["act"] for item in toc]
        if not available_acts:
            st.error("No acts found in the play")
            return
            
        selected_act = st.selectbox(
            "Select Act",
            available_acts,
            key="text_display_act_select"
        )
    
    with col2:
        act_data = next((item for item in toc if item["act"] == selected_act), None)
        if not act_data:
            st.error(f"Could not find data for act {selected_act}")
            return
            
        available_scenes = act_data["scenes"]
        if not available_scenes:
            st.error(f"No scenes found in {selected_act}")
            return
            
        selected_scene = st.selectbox(
            "Select Scene",
            available_scenes,
            key="text_display_scene_select"
        )

    # Display mode buttons
    st.markdown("### Display Mode")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(
            'Original',
            type='primary' if st.session_state.get('display_mode', 'Original') == 'Original' else 'secondary',
            use_container_width=True,
            key='btn_original'
        ):
            st.session_state.display_mode = 'Original'
            st.session_state.show_legend = False
            st.rerun()
    
    with col2:
        if st.button(
            'POS Highlight',
            type='primary' if st.session_state.get('display_mode') == 'POS Highlight' else 'secondary',
            use_container_width=True,
            key='btn_pos_highlight'
        ):
            st.session_state.display_mode = 'POS Highlight'
            st.session_state.show_legend = True
            st.rerun()
    
    with col3:
        if st.button(
            'POS Definition',
            type='primary' if st.session_state.get('display_mode') == 'POS Definition' else 'secondary',
            use_container_width=True,
            key='btn_pos_definition'
        ):
            st.session_state.display_mode = 'POS Definition'
            st.session_state.show_legend = True
            st.rerun()
    
    # Show legend toggle only in POS modes
    if st.session_state.get('display_mode') in ['POS Highlight', 'POS Definition']:
        show_legend = st.checkbox("Show POS Legend", 
                                value=st.session_state.get('show_legend', True),
                                key='legend_toggle')
        if show_legend:
            render_pos_legend()
    
    # Process and display text
    try:
        scene_text = acts_scenes[selected_act][selected_scene]
        processed_text = apply_basic_formatting(scene_text)
        
        if st.session_state.get('display_mode') in ['POS Highlight', 'POS Definition']:
            mode = 'colored_text' if st.session_state.get('display_mode') == 'POS Highlight' else 'colored_tags'
            processed_text = pos_tagger.process_text(processed_text, mode=mode)
        
        # Display text in container
        st.markdown(f"### {selected_act} - {selected_scene}")
        st.markdown(
            f"""
            <div class='text-container'>
                <div class='passage-text stText'>
                    <pre class="stText">{processed_text}</pre>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
            
    except KeyError:
        st.error(f"Could not find text for {selected_act}, {selected_scene}")
        
def apply_basic_formatting(text: str) -> str:
    """Apply standard formatting with fixed character name highlighting."""
    # Add line numbers
    lines = text.split('\n')
    numbered_lines = []
    line_number = 1
    for line in lines:
        if line.strip():
            safe_line = html.escape(line)
            
            # Handle character names
            for char in extract_characters(line):
                char_pattern = f"{char}\\."
                safe_line = re.sub(
                    char_pattern,
                    f'<span class="character-name">{char}.</span>',
                    safe_line
                )
            
            numbered_lines.append(f'<span class="line-number">{line_number}</span>{safe_line}')
            line_number += 1
        else:
            numbered_lines.append(line)
            
    text = '\n'.join(numbered_lines)
    
    # Handle stage directions
    stage_directions = extract_stage_directions(text)
    for direction in stage_directions:
        safe_direction = html.escape(direction)
        text = text.replace(
            f"[{direction}]",
            f'<span class="stage-direction">[{safe_direction}]</span>'
        )
    
    return text

def render_display_options() -> List[str]:
    """Render display options selection."""
    return st.multiselect(
        "Display Options",
        [
            "Show Stage Directions",
            "Highlight Character Names",
            "Show Line Numbers",
            "Show POS Tags"
        ],
        ["Show Stage Directions"]
    )

def process_text_with_options(text: str, display_options: List[str],
                            pos_tagger: POSTagger) -> str:
    """Process text according to selected display options."""
    if "Show POS Tags" in display_options:
        pos_mode = st.selectbox(
            "POS Tag Display Mode",
            list(DISPLAY_MODES.values())
        )
        
        mode_mapping = {v: k for k, v in DISPLAY_MODES.items()}
        text = pos_tagger.process_text(text, mode_mapping[pos_mode])
        
        if pos_mode in ["Colored Text (words in POS colors)", 
                       "Colored Tags (POS tags in colors)"]:
            render_pos_legend()
    
    text = apply_display_options(text, display_options)
    return text


def render_pos_legend() -> None:
    """Render POS tags legend with descriptions."""
    st.markdown("### POS Tags Legend")
    
    # Create a grid layout for the legend
    cols = st.columns(3)
    sorted_pos = sorted(POS_COLORS.items())
    
    for i, (pos, color) in enumerate(sorted_pos):
        col_idx = i % 3
        with cols[col_idx]:
            st.markdown(
                f'<div style="margin-bottom: 10px;">'
                f'<span style="color: {color}">■</span> '
                f'<strong>{pos}</strong><br>'
                f'<small>{POS_DESCRIPTIONS[pos]}</small>'
                f'</div>',
                unsafe_allow_html=True
            )

def apply_display_options(text: str, display_options: List[str]) -> str:
    """
    Apply selected display options to the text.
    
    Args:
        text: Original text content
        display_options: List of selected display options
    
    Returns:
        Processed text with display options applied
    """
    if "Show Stage Directions" in display_options:
        stage_directions = extract_stage_directions(text)
        for direction in stage_directions:
            text = text.replace(
                f"[{direction}]",
                f'<span class="stage-direction">[{direction}]</span>'
            )
    
    if "Highlight Character Names" in display_options:
        characters = extract_characters(text)
        for char in characters:
            text = text.replace(
                f"{char}.",
                f'<span class="character-name">{char}.</span>'
            )
    
    if "Show Line Numbers" in display_options:
        lines = text.split('\n')
        text = '\n'.join(
            f'<span class="line-number">{i+1}</span> {line}'
            for i, line in enumerate(lines)
        )
    
    return text