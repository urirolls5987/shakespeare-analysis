# src/services/network.py
import networkx as nx
import re
from collections import defaultdict
import plotly.graph_objects as go
from typing import Dict, List, Set, Tuple

def extract_scene_dialogues(text: str) -> List[List[str]]:
    """Extract the sequence of character dialogues in each scene."""
    if not isinstance(text, str):
        raise TypeError("Text must be a string")
        
    try:
        scenes = re.split(r'SCENE [IVX]+\.', text)
        scene_dialogues = []
        
        for scene in scenes:
            if not scene.strip():
                continue
            # Extract sequence of speakers in the scene
            speakers = re.findall(r'\n([A-Z]{2,}(?:\s+[A-Z]{2,})*)\.\s', scene)
            if speakers:
                scene_dialogues.append(speakers)
        
        return scene_dialogues
    except Exception as e:
        print(f"Error in extract_scene_dialogues: {str(e)}")
        return []

def calculate_interaction_weights(scene_dialogues: List[List[str]]) -> Dict[Tuple[str, str], float]:
    """Calculate interaction weights based on dialogue proximity."""
    weights = defaultdict(float)
    
    for scene in scene_dialogues:
        # Consider characters speaking within 2 dialogue turns as interacting
        for i in range(len(scene)):
            for j in range(max(0, i-2), min(len(scene), i+3)):
                if i != j:
                    char1, char2 = sorted([scene[i], scene[j]])
                    weights[(char1, char2)] += 1 / (abs(i-j))  # Weight by proximity
    
    return weights

# src/services/network.py

def create_character_network_graph(text: str, selected_character: str = None) -> go.Figure:
    """Create an interactive network visualization using Plotly."""
    # Get dialogue sequences and calculate interactions
    scene_dialogues = extract_scene_dialogues(text)
    weights = calculate_interaction_weights(scene_dialogues)
    
    # Create networkx graph
    G = nx.Graph()
    
    # Add edges with weights
    for (char1, char2), weight in weights.items():
        G.add_edge(char1, char2, weight=weight)
    
    # Calculate layout
    pos = nx.spring_layout(G)
    
    # Create figure
    fig = go.Figure()
    
    # Add edges (adding them as separate traces to handle different weights)
    edge_weights = [d['weight'] for _, _, d in G.edges(data=True)]
    max_weight = max(edge_weights) if edge_weights else 1
    
    for (node1, node2, data) in G.edges(data=True):
        x0, y0 = pos[node1]
        x1, y1 = pos[node2]
        
        # Calculate edge width based on weight
        width = 1 + (data['weight'] / max_weight) * 4
        
        # Add edge as individual trace
        fig.add_trace(go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            line=dict(width=width, color='rgba(150, 150, 150, 0.3)'),
            hoverinfo='none',
            mode='lines',
            showlegend=False
        ))
    
    # Create nodes
    node_x = []
    node_y = []
    node_text = []
    node_sizes = []
    node_colors = []
    
    # Calculate centrality for node sizes
    centrality = nx.degree_centrality(G)
    max_centrality = max(centrality.values()) if centrality else 1
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        # Count character's appearances
        appearances = sum(1 for scene in scene_dialogues if node in scene)
        node_text.append(f"{node}<br>Appearances: {appearances}")
        
        # Size based on centrality
        node_sizes.append(20 + (centrality[node]/max_centrality) * 40)
        
        # Color: gold for selected, varying blues for others based on connection strength
        if node == selected_character:
            node_colors.append('#ffd700')
        else:
            # Check connection to selected character
            if selected_character and G.has_edge(selected_character, node):
                edge_weight = G[selected_character][node]['weight']
                strength = edge_weight / max_weight
                node_colors.append(f'rgba(70, 130, 180, {0.3 + strength * 0.7})')
            else:
                node_colors.append('rgba(70, 130, 180, 0.3)')
    
    # Add nodes trace
    fig.add_trace(go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=list(G.nodes()),
        textposition="top center",
        hovertext=node_text,
        hoverinfo='text',
        marker=dict(
            size=node_sizes,
            color=node_colors,
            line=dict(color='#ffffff', width=1)
        ),
        showlegend=False
    ))
    
    # Update layout
    fig.update_layout(
        title=f"Character Interaction Network{' - ' + selected_character if selected_character else ''}",
        showlegend=False,
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#1e1e1e',
        font=dict(color='#e0e0e0'),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(b=20, l=5, r=5, t=40),
        height=600
    )
    
    return fig

def get_character_metrics(text: str, character: str) -> Dict[str, float]:
    """Get network metrics for a specific character."""
    scene_dialogues = extract_scene_dialogues(text)
    weights = calculate_interaction_weights(scene_dialogues)
    
    G = nx.Graph()
    for (char1, char2), weight in weights.items():
        G.add_edge(char1, char2, weight=weight)
    
    if character not in G:
        return {}
    
    return {
        'degree': nx.degree_centrality(G)[character],
        'betweenness': nx.betweenness_centrality(G)[character],
        'eigenvector': nx.eigenvector_centrality(G, max_iter=1000)[character]
    }