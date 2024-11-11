# src/ui/components/navigation.py
"""Navigation component for the application."""

import streamlit as st
from typing import Optional, Tuple

def render_navigation(toc: list) -> str:
    """Render navigation sidebar and return selected view."""
    st.sidebar.markdown("<div class='sidebar-title'>Shakespeare Interactive</div>", 
                       unsafe_allow_html=True)
    
    nav_option = st.sidebar.radio(
        "Navigation",
        ["Table of Contents", "Character Analysis", "Scene Analysis", "About"]
    )
    
    if nav_option == "Table of Contents":
        render_toc_navigation(toc)
    
    return nav_option

def render_toc_navigation(toc: list) -> Tuple[str, str]:
    """Render table of contents navigation."""
    selected_act = st.sidebar.selectbox(
        "Select Act",
        [item["act"] for item in toc],
        key="nav_act_select"
    )
    
    selected_scene = st.sidebar.selectbox(
        "Select Scene",
        [item for item in toc if item["act"] == selected_act][0]["scenes"],
        key="nav_scene_select"
    )
    
    return selected_act, selected_scene