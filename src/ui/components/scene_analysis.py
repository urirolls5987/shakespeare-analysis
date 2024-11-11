# src/ui/components/scene_analysis.py
"""Scene analysis component."""

import streamlit as st
import plotly.graph_objects as go
from typing import Counter, Dict
import pandas as pd
from src.data.parser import extract_characters, extract_stage_directions
from src.services.pos_tagger import POSTagger, POS_COLORS

def render_scene_analysis(acts_scenes: Dict[str, Dict[str, str]], pos_tagger: POSTagger) -> None:
    """Render scene analysis with POS statistics."""
    st.markdown("### Scene Analysis")
    
    # Calculate POS distributions for each scene
    scene_stats = {}
    for act in acts_scenes:
        for scene in acts_scenes[act]:
            text = acts_scenes[act][scene]
            doc = pos_tagger.nlp(text)
            
            # Count POS tags
            pos_counts = Counter([token.pos_ for token in doc if not token.is_punct])
            total_tokens = sum(pos_counts.values())
            
            # Calculate percentages
            pos_distribution = {
                pos: (count / total_tokens * 100) 
                for pos, count in pos_counts.items()
            }
            
            scene_stats[f"{act} - {scene}"] = {
                'pos_distribution': pos_distribution,
                'total_tokens': total_tokens,
                'word_count': len([t for t in doc if not t.is_punct and not t.is_space])
            }
    
    # Create visualizations
    fig = go.Figure()
    
    # Add traces for major POS categories
    main_pos = ['NOUN', 'VERB', 'ADJ', 'ADV']
    for pos in main_pos:
        fig.add_trace(go.Bar(
            name=f"{pos} %",
            x=list(scene_stats.keys()),
            y=[stats['pos_distribution'].get(pos, 0) for stats in scene_stats.values()],
            marker_color=POS_COLORS.get(pos)
        ))
    
    fig.update_layout(
        title="Part of Speech Distribution Across Scenes",
        barmode='group',
        xaxis_title="Scene",
        yaxis_title="Percentage",
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#1e1e1e',
        font=dict(color='#e0e0e0')
    )
    
    st.plotly_chart(fig)
    
    # Add detailed analysis
    st.markdown("### Scene Complexity Analysis")
    
    # Calculate complexity metrics
    complexity_metrics = {}
    for scene_id, stats in scene_stats.items():
        pos_diversity = len(stats['pos_distribution'])
        weighted_pos = sum(
            pct * (1 if pos in ['NOUN', 'VERB'] else 0.5) 
            for pos, pct in stats['pos_distribution'].items()
        )
        
        complexity_metrics[scene_id] = {
            'POS Diversity': pos_diversity,
            'Weighted Complexity': weighted_pos,
            'Words per Scene': stats['word_count']
        }
    
    # Display metrics
    df = pd.DataFrame(complexity_metrics).T
    st.dataframe(
        df.style.background_gradient(cmap='viridis', axis=0)
        .format({"Weighted Complexity": "{:.2f}", "Words per Scene": "{:,.0f}"})
    )

def calculate_scene_metrics(acts_scenes: Dict[str, Dict[str, str]]) -> Dict[str, Dict[str, int]]:
    """Calculate metrics for each scene."""
    metrics = {}
    for act in acts_scenes:
        for scene in acts_scenes[act]:
            scene_text = acts_scenes[act][scene]
            metrics[f"{act} - {scene}"] = {
                "characters": len(extract_characters(scene_text)),
                "words": len(scene_text.split()),
                "stage_directions": len(extract_stage_directions(scene_text))
            }
    return metrics

def create_scene_metrics_visualization(metrics: Dict[str, Dict[str, int]]) -> go.Figure:
    """Create visualization of scene metrics."""
    fig = go.Figure()
    scenes = list(metrics.keys())
    
    fig.add_trace(go.Scatter(
        x=scenes,
        y=[m["characters"] for m in metrics.values()],
        name="Characters"
    ))
    
    fig.add_trace(go.Scatter(
        x=scenes,
        y=[m["stage_directions"] for m in metrics.values()],
        name="Stage Directions"
    ))
    
    fig.update_layout(
        title="Scene Metrics",
        xaxis_title="Scene",
        yaxis_title="Count"
    )
    
    return fig