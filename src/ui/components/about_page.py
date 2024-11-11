import streamlit as st
from datetime import datetime

def render_about_page() -> None:
    """Render the About page with application information."""
    st.markdown("""
    # About Shakespeare Interactive
    
    This interactive tool helps you explore and analyze Shakespeare's plays with modern computational techniques.
    
    ## Features
    
    ### Text Analysis
    - **Part of Speech Tagging**: Visualize the grammatical structure of the text
    - **Stage Directions**: Highlight and analyze stage directions
    - **Line Numbers**: Enable line numbers for easy reference
    
    ### Character Analysis
    - **Network Analysis**: Visualize character interactions and relationships
    - **Dialogue Statistics**: Analyze speaking patterns and word usage
    - **Character Centrality**: Measure character importance in the play
    
    ### Scene Analysis
    - **Metrics Visualization**: Track characters and stage directions per scene
    - **Text Complexity**: Analyze language complexity across scenes
    - **Interactive Navigation**: Easily move between acts and scenes
    
    ## Technical Details
    - Built with Streamlit and Python
    - Uses spaCy for natural language processing
    - Network analysis with NetworkX
    - Visualizations with Plotly
    
    ## Version Information
    - **Version**: 1.0.0
    - **Last Updated**: {}
    """.format(datetime.now().strftime("%B %Y")))
    
    # Add feedback section
    st.markdown("---")
    st.markdown("### Feedback")
    
    with st.expander("Share Your Feedback"):
        feedback_type = st.selectbox(
            "Feedback Type",
            ["Feature Request", "Bug Report", "General Feedback"],
            key="about_feedback_type"
        )
        feedback_text = st.text_area(
            "Your Feedback",
            key="about_feedback_text"
        )
        if st.button("Submit Feedback", key="about_feedback_submit"):
            st.success("Thank you for your feedback!")