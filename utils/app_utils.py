"""
Utility functions for the Streamlit ABSA application.
These functions are now integrated directly into streamlit_app.py
"""
import pickle
from typing import Dict, List
import pandas as pd
import numpy as np
import streamlit as st
# Note: These functions have been moved to streamlit_app.py for better integration
# This file is kept for compatibility but functions are now defined in the main app
def load_model(model_path: str):
    """Load trained model with caching for better performance."""
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

@st.cache_data
def preprocess_text(text: str) -> str:
    """Preprocess text for analysis."""
    # TODO: Integrate with your preprocessing pipeline
    return text.strip().lower()

def analyze_single_text(text: str, model=None) -> Dict:
    """Analyze a single text for aspects and sentiment."""
    # TODO: Replace with your actual model inference
    # This is a placeholder implementation
    
    aspects = ["food", "service", "ambiance", "price", "location"]
    results = {}
    
    for aspect in aspects:
        if aspect.lower() in text.lower():
            # Mock sentiment analysis
            sentiment_score = np.random.uniform(-1, 1)
            sentiment_label = "positive" if sentiment_score > 0.1 else "negative" if sentiment_score < -0.1 else "neutral"
            
            results[aspect] = {
                "sentiment": sentiment_label,
                "score": sentiment_score,
                "confidence": abs(sentiment_score)
            }
    
    return results

def analyze_batch_texts(texts: List[str], model=None) -> pd.DataFrame:
    """Analyze multiple texts and return aggregated results."""
    all_results = []
    
    for i, text in enumerate(texts):
        results = analyze_single_text(text, model)
        for aspect, data in results.items():
            all_results.append({
                "text_id": i,
                "aspect": aspect,
                "sentiment": data["sentiment"],
                "score": data["score"],
                "confidence": data["confidence"]
            })
    
    return pd.DataFrame(all_results)

def create_word_cloud(texts: List[str], aspect: str = None):
    """Create word cloud for visualization."""
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    
    combined_text = " ".join(texts)
    
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='white',
        colormap='viridis'
    ).generate(combined_text)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    
    return fig

def format_results_for_display(results: Dict) -> pd.DataFrame:
    """Format analysis results for better display in Streamlit."""
    formatted_data = []
    
    for aspect, data in results.items():
        formatted_data.append({
            "Aspect": aspect.title(),
            "Sentiment": data["sentiment"].title(),
            "Score": round(data["score"], 3),
            "Confidence": f"{round(data['confidence'] * 100, 1)}%"
        })
    
    return pd.DataFrame(formatted_data)

def export_results_to_csv(results_df: pd.DataFrame) -> str:
    """Export results to CSV format for download."""
    return results_df.to_csv(index=False)
