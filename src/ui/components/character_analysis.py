# src/ui/components/character_analysis.py
"""Character analysis component."""
import networkx as nx
import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Set
from collections import defaultdict, Counter

from src.services.network import create_character_network_graph, get_character_metrics
from src.data.parser import extract_characters, generate_character_network, get_character_lines
from src.config.constants import POS_COLORS, POS_DESCRIPTIONS
from src.services.pos_tagger import POSTagger

class CharacterAnalyzer:
    def __init__(self, nlp_model):
        self.nlp = nlp_model
        self.character_lines = defaultdict(list)
        self.character_words = defaultdict(Counter)
        self.character_pos_stats = defaultdict(Counter)
    
    def analyze_text(self, text: str, character_names: Set[str]) -> None:
        """Analyze text and collect statistics for each character."""
        current_speaker = None
        
        for line in text.split('\n'):
            # Check for character name at start of line
            for char in character_names:
                if line.startswith(f"{char}."):
                    current_speaker = char
                    break
            
            # If we have a current speaker and this isn't a character name line
            if current_speaker and not any(char + '.' in line for char in character_names):
                # Process the line
                doc = self.nlp(line)
                
                # Store the line
                self.character_lines[current_speaker].append(line)
                
                # Count words and POS tags
                for token in doc:
                    if not token.is_punct and not token.is_space:
                        self.character_words[current_speaker][token.text.lower()] += 1
                        self.character_pos_stats[current_speaker][token.pos_] += 1
    
    def get_character_stats(self, character: str) -> Dict:
        """Get comprehensive statistics for a character."""
        total_words = sum(self.character_words[character].values())
        total_lines = len(self.character_lines[character])
        pos_distribution = dict(self.character_pos_stats[character])
        
        # Calculate word frequencies
        word_frequencies = dict(self.character_words[character].most_common(20))
        
        return {
            'total_words': total_words,
            'total_lines': total_lines,
            'unique_words': len(self.character_words[character]),
            'vocabulary_diversity': len(self.character_words[character]) / total_words if total_words > 0 else 0,
            'pos_distribution': pos_distribution,
            'common_words': word_frequencies
        }

def render_character_analysis(acts_scenes: Dict[str, Dict[str, str]], pos_tagger: POSTagger) -> None:
    """Render character analysis view."""
    st.markdown("### Character Analysis")
    
    # Get all text from acts and scenes
    full_text = '\n'.join(
        scene_text
        for act in acts_scenes.values()
        for scene_text in act.values()
    )
    
    # Get all characters
    all_characters = set()
    for act in acts_scenes:
        for scene in acts_scenes[act]:
            all_characters.update(extract_characters(acts_scenes[act][scene]))
    
    # Character selection
    selected_character = st.selectbox(
        "Select Character",
        sorted(list(all_characters)),
        key="character_analysis_select"
    )
    
    # Add tabs for different views
    # tab2 = st.tabs(["Character Network"])
    # tab1, tab2 = st.tabs(["Character Network", "Word Analysis"])
    
    # with tab1:
    if st.checkbox("Show Network Debug", key="network_debug"):
        st.write("Number of characters:", len(all_characters))
        st.write("Sample characters:", list(all_characters)[:5])
        st.write("Text length:", len(full_text))
    
    if full_text:  # Only create network if we have text
        try:
            network_fig = create_character_network_graph(full_text, selected_character)
            st.plotly_chart(network_fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating network visualization: {str(e)}")
            if st.checkbox("Show Error Details"):
                st.exception(e)

    # with tab2:
        # Word frequency analysis
        # total_lines = 0
        # character_lines = []
        # for act in acts_scenes:
        #     for scene in acts_scenes[act]:
        #         lines = get_character_lines(acts_scenes[act][scene], selected_character)
        #         character_lines.extend(lines)
        #         total_lines += len(lines)
        
        # col1, col2, col3 = st.columns(3)
        # with col1:
        #     st.metric("Total Lines", total_lines)
        # with col2:
        #     st.metric("Total Words", len(' '.join(character_lines).split()))
        # with col3:
        #     st.metric("Unique Words", len(set(' '.join(character_lines).lower().split())))
        
        # if character_lines:
        #     # Word frequency analysis
        #     words = ' '.join(character_lines).lower().split()
        #     word_freq = Counter(words)
            
        #     # Filter out stopwords and sort
        #     filtered_words = {
        #         word: count for word, count in word_freq.items()
        #         if word not in pos_tagger.nlp.Defaults.stop_words 
        #         and len(word) > 1  # Filter out single characters
        #         and count >= 3  # Minimum frequency threshold
        #     }
            
        #     sorted_words = dict(sorted(filtered_words.items(), 
        #                              key=lambda x: x[1], 
        #                              reverse=True)[:20])
            
        #     fig = go.Figure(data=[
        #         go.Bar(
        #             x=list(sorted_words.keys()),
        #             y=list(sorted_words.values()),
        #             marker_color='#ffd700'
        #         )
        #     ])
            
        #     fig.update_layout(
        #         title=f"Most Common Words - {selected_character}",
        #         xaxis_title="Word",
        #         yaxis_title="Frequency",
        #         plot_bgcolor='#1e1e1e',
        #         paper_bgcolor='#1e1e1e',
        #         font=dict(color='#e0e0e0')
        #     )
            
        #     st.plotly_chart(fig)
    
    
def render_pos_legend() -> None:
    """Render POS tags legend with descriptions."""
    st.markdown("### POS Tags Legend")
    
    legend_html = []
    for pos, color in POS_COLORS.items():
        description = POS_DESCRIPTIONS.get(pos, pos)
        legend_html.append(
            f'<div class="pos-tag-item">'
            f'<span style="color: {color}">■</span> '
            f'<strong>{pos}</strong> - {description}'
            f'</div>'
        )
    
    st.markdown(
        f"""
        <div class="pos-legend">
            <div class="pos-legend-grid">
                {''.join(legend_html)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# def render_character_network(character: str, acts_scenes: Dict[str, Dict[str, str]], 
#                            pos_tagger: POSTagger) -> None:
#     """Generate and display character interaction network."""
#     all_characters = set()
#     interactions = defaultdict(int)
    
#     # Analyze interactions
#     for act in acts_scenes:
#         for scene in acts_scenes[act]:
#             text = acts_scenes[act][scene]
#             scene_chars = extract_characters(text)
#             all_characters.update(scene_chars)
            
#             # Count character co-occurrences in scenes
#             for char1 in scene_chars:
#                 for char2 in scene_chars:
#                     if char1 < char2:  # Avoid double counting
#                         interactions[(char1, char2)] += 1

#     # Create network
#     G = nx.Graph()
    
#     # Add nodes (characters)
#     for char in all_characters:
#         G.add_node(char, size=1)
    
#     # Add edges (interactions)
#     for (char1, char2), weight in interactions.items():
#         G.add_edge(char1, char2, weight=weight)
    
#     # Calculate node sizes based on degree centrality
#     centrality = nx.degree_centrality(G)
#     node_sizes = {node: centrality[node] * 1000 for node in G.nodes()}
    
#     # Create network visualization
#     pos = nx.spring_layout(G)
    
#     # Create plot
#     fig = go.Figure()
    
#     # Add edges
#     edge_x = []
#     edge_y = []
#     for edge in G.edges():
#         x0, y0 = pos[edge[0]]
#         x1, y1 = pos[edge[1]]
#         edge_x.extend([x0, x1, None])
#         edge_y.extend([y0, y1, None])
    
#     fig.add_trace(go.Scatter(
#         x=edge_x, y=edge_y,
#         line=dict(width=0.5, color='#888'),
#         hoverinfo='none',
#         mode='lines'
#     ))
    
#     # Add nodes
#     node_x = []
#     node_y = []
#     node_text = []
#     node_size = []
#     node_color = []
    
#     for node in G.nodes():
#         x, y = pos[node]
#         node_x.append(x)
#         node_y.append(y)
#         node_text.append(node)
#         node_size.append(node_sizes[node])
#         node_color.append('#ffd700' if node == character else '#1f77b4')
    
#     fig.add_trace(go.Scatter(
#         x=node_x, y=node_y,
#         mode='markers+text',
#         hoverinfo='text',
#         text=node_text,
#         textposition="top center",
#         marker=dict(
#             size=node_size,
#             color=node_color,
#             line_width=2
#         )
#     ))
    
#     fig.update_layout(
#         title=f"Character Interaction Network (highlighting {character})",
#         showlegend=False,
#         plot_bgcolor='#1e1e1e',
#         paper_bgcolor='#1e1e1e',
#         font=dict(color='#e0e0e0'),
#         xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
#         yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
#         margin=dict(b=20,l=5,r=5,t=40),
#         height=600
#     )
    
#     st.plotly_chart(fig, use_container_width=True)