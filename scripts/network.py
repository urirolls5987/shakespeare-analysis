import networkx as nx
import matplotlib.pyplot as plt
import re
from collections import defaultdict

def extract_dramatis_personae(text):
    """Extract the list of characters from the dramatis personae section."""
    try:
        # Find the dramatis personae section
        start = text.find("Dramatis Personæ")
        end = text.find("SCENE")
        dramatis_section = text[start:end]
        
        # Extract character names and their descriptions
        character_dict = {}
        lines = dramatis_section.split('\n')
        for line in lines:
            if line.strip() and ',' in line:
                name, description = line.split(',', 1)
                name = name.strip()
                if name.isupper():  # Only get the main character names
                    character_dict[name] = description.strip()
        
        return character_dict
    except:
        return {}

def extract_speaking_parts(text):
    """Extract all characters who have speaking parts in the play."""
    # Find all instances where a character name appears before a line of dialogue
    speaking_parts = re.findall(r'\n([A-Z]{2,}(?:\s+[A-Z]{2,})*)\.\s', text)
    return set(speaking_parts)

def extract_scene_dialogues(text):
    """Extract the sequence of character dialogues in each scene."""
    scenes = re.split(r'SCENE [IVX]+\.', text)
    scene_dialogues = []
    
    for scene in scenes:
        # Extract sequence of speakers in the scene
        speakers = re.findall(r'\n([A-Z]{2,}(?:\s+[A-Z]{2,})*)\.\s', scene)
        if speakers:
            scene_dialogues.append(speakers)
    
    return scene_dialogues

def calculate_interaction_weights(scene_dialogues):
    """Calculate interaction weights based on dialogue proximity."""
    weights = defaultdict(int)
    
    for scene in scene_dialogues:
        # Consider characters speaking within 2 dialogue turns as interacting
        for i in range(len(scene)):
            for j in range(max(0, i-2), min(len(scene), i+3)):
                if i != j:
                    char1, char2 = sorted([scene[i], scene[j]])
                    weights[(char1, char2)] += 1 / (abs(i-j))  # Weight by proximity
    
    return weights

def create_character_network(scene_dialogues, char_descriptions):
    """Create a weighted network of character interactions."""
    G = nx.Graph()
    
    # Add nodes with character descriptions
    for char in char_descriptions:
        G.add_node(char, description=char_descriptions[char])
    
    # Calculate and add weighted edges
    weights = calculate_interaction_weights(scene_dialogues)
    for (char1, char2), weight in weights.items():
        G.add_edge(char1, char2, weight=weight)
    
    return G

def analyze_character_importance(G, scene_dialogues):
    """Analyze character importance using multiple metrics."""
    # Count lines of dialogue
    dialogue_counts = defaultdict(int)
    for scene in scene_dialogues:
        for char in scene:
            dialogue_counts[char] += 1
    
    # Calculate various centrality metrics
    degree_cent = nx.degree_centrality(G)
    betweenness_cent = nx.betweenness_centrality(G)
    eigenvector_cent = nx.eigenvector_centrality(G, max_iter=1000)
    
    # Combine metrics
    character_metrics = {}
    for char in G.nodes():
        character_metrics[char] = {
            'Dialogue Count': dialogue_counts[char],
            'Degree Centrality': degree_cent[char],
            'Betweenness Centrality': betweenness_cent[char],
            'Eigenvector Centrality': eigenvector_cent[char]
        }
    
    return character_metrics

import networkx as nx
import matplotlib.pyplot as plt
import re
from collections import defaultdict
import numpy as np

# [Previous functions remain the same until visualize_network]

def visualize_network(G, metrics):
    """Create a balanced visualization of the character network."""
    # Create figure and axis explicitly
    fig, ax = plt.subplots(figsize=(15, 10))
    
    # Calculate normalized node sizes with a smaller range
    dialogue_counts = [metrics[char]['Dialogue Count'] for char in G.nodes()]
    max_count = max(dialogue_counts)
    node_sizes = [300 + (count/max_count) * 700 for count in dialogue_counts]
    
    # Calculate edge properties
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
    max_weight = max(edge_weights)
    min_weight = min(edge_weights)
    
    # Normalize edge weights for coloring
    norm = plt.Normalize(vmin=min_weight, vmax=max_weight)
    
    # Create color map for edges based on weight
    edge_colors = [plt.cm.YlOrRd(norm(w)) for w in edge_weights]
    edge_widths = [1 + (w/max_weight) * 5 for w in edge_weights]
    
    # Create layout
    pos = nx.spring_layout(G, k=2, iterations=100, seed=42)
    
    # Draw the network elements
    nx.draw_networkx_edges(G, pos, 
                          ax=ax,
                          width=edge_widths,
                          edge_color=edge_colors,
                          alpha=0.6)
    
    # Create node colors based on centrality
    node_colors = [plt.cm.Blues(metrics[node]['Degree Centrality']) 
                  for node in G.nodes()]
    
    nx.draw_networkx_nodes(G, pos, 
                          ax=ax,
                          node_color=node_colors,
                          node_size=node_sizes, 
                          alpha=0.7)
    
    # Add labels with different sizes based on importance
    centrality = nx.degree_centrality(G)
    for node in G.nodes():
        # Adjust label sizes based on centrality but with less variation
        font_size = 8 + (centrality[node] * 4)
        
        # Create label
        label = node if centrality[node] > 0.2 else '\n'.join([node[i:i+10] for i in range(0, len(node), 10)])
        
        # Add label with white background
        ax.text(pos[node][0], pos[node][1], label,
               fontsize=font_size,
               ha='center', va='center',
               bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
    
    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap=plt.cm.YlOrRd, norm=norm)
    sm.set_array([])
    plt.colorbar(sm, ax=ax, label='Interaction Strength', fraction=0.046, pad=0.04)
    
    # Add title and adjust layout
    ax.set_title("Character Interaction Network in Hamlet", pad=20)
    ax.axis('off')
    
    # Add legend for node sizes
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                                 markerfacecolor='lightblue', markersize=10, 
                                 label=label)
                      for label in ['Major Character', 'Supporting Character', 'Minor Character']]
    
    ax.legend(handles=legend_elements,
             loc='upper left',
             title='Character Importance',
             bbox_to_anchor=(1.1, 1))
    
    # Adjust layout to prevent clipping
    plt.tight_layout()
    
    return plt

def print_character_analysis(metrics, char_descriptions):
    """Print detailed character analysis with interaction patterns."""
    print("\nCharacter Analysis:")
    print("-" * 50)
    
    # Calculate normalized importance scores
    importance_scores = {}
    max_dialogue = max(m['Dialogue Count'] for m in metrics.values())
    
    for char in metrics:
        # Combine different metrics with weights
        score = (
            0.4 * metrics[char]['Degree Centrality'] +
            0.3 * metrics[char]['Betweenness Centrality'] +
            0.2 * metrics[char]['Eigenvector Centrality'] +
            0.1 * (metrics[char]['Dialogue Count'] / max_dialogue)
        )
        importance_scores[char] = score
    
    # Sort and print character analysis
    sorted_chars = sorted(importance_scores.items(), key=lambda x: x[1], reverse=True)
    
    for char, importance in sorted_chars[:10]:
        print(f"\n{char}:")
        if char in char_descriptions:
            print(f"Role: {char_descriptions[char]}")
        print(f"Importance Score: {importance:.3f}")
        print(f"Lines of dialogue: {metrics[char]['Dialogue Count']}")
        print(f"Interaction Pattern:")
        print(f"- Network centrality: {metrics[char]['Degree Centrality']:.3f}")
        print(f"- Plot influence: {metrics[char]['Betweenness Centrality']:.3f}")
        print(f"- Character connections: {metrics[char]['Eigenvector Centrality']:.3f}")


def main(text):
    # Extract character information
    char_descriptions = extract_dramatis_personae(text)
    scene_dialogues = extract_scene_dialogues(text)
    
    # Create and analyze network
    G = create_character_network(scene_dialogues, char_descriptions)
    metrics = analyze_character_importance(G, scene_dialogues)
    
    # Print analysis
    print_character_analysis(metrics, char_descriptions)
    
    # Visualize network
    plt = visualize_network(G, metrics)
    plt.show()

if __name__ == "__main__":
    with open("/Users/urirolls/urirolls/Cardenio/Cardenio/statistical_breakdown/plays/hamlet.txt", 'r') as file:
        text = file.read()
    main(text)