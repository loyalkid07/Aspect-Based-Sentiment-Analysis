"""
Model Management and Setup Module

This module handles the initialization and management of NLP models
including NLTK resources and Stanza pipelines.
"""

import subprocess
import sys
import nltk
import stanza
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class ModelManager:
    """Manages NLP models and their initialization."""
    
    def __init__(self):
        self.nlp = None
        self.sid = None
        self.is_initialized = False
    

    
    def download_nltk_resources(self):
        """Download necessary NLTK resources."""
        resources = [
            'stopwords',
            'vader_lexicon', 
            'punkt',
            'averaged_perceptron_tagger',
            'punkt_tab',
            'averaged_perceptron_tagger_eng'
        ]
        
        success = True
        for resource in resources:
            try:
                nltk.download(resource, quiet=True)
            except Exception as e:
                print(f"✗ Failed to download {resource}: {e}")
                success = False
        return success
    
    def setup_stanza_pipeline(self, language='en'):
        """Download Stanza model and create pipeline."""
        print("Setting up Stanza pipeline...")
        try:
            import os
            stanza_dir = os.path.join(os.path.expanduser("~"), "stanza_resources", language)
            
            if not os.path.exists(stanza_dir):
                print("Downloading Stanza models (this happens only once)...")
                stanza.download(language, verbose=False)
            
            try:
                self.nlp = stanza.Pipeline(language, verbose=False, download_method=None)
            except TypeError:
                # Fallback for older stanza versions
                self.nlp = stanza.Pipeline(language, verbose=False)
                
            print("✓ Stanza pipeline ready")
            return True
        except Exception as e:
            print(f"✗ Error setting up Stanza: {e}")
            return False
    
    def initialize_sentiment_analyzer(self):
        """Initialize NLTK's VADER sentiment analyzer."""
        try:
            self.sid = SentimentIntensityAnalyzer()
            print("✓ Sentiment analyzer initialized")
            return True
        except Exception as e:
            print(f"✗ Error initializing sentiment analyzer: {e}")
            return False
    
    def setup_all(self):
        """Run complete setup process."""
        print("Starting model setup...")
        
        # Download NLTK resources
        if not self.download_nltk_resources():
            return False
        
        # Setup components
        stanza_ok = self.setup_stanza_pipeline()
        sentiment_ok = self.initialize_sentiment_analyzer()
        
        if stanza_ok and sentiment_ok:
            self.is_initialized = True
            print("✓ All models initialized successfully!")
            return True
        else:
            print("✗ Model initialization failed")
            return False
    
    def get_models(self):
        """Get initialized models."""
        if not self.is_initialized:
            print("Models not initialized. Run setup_all() first.")
            return None, None
        return self.nlp, self.sid


# Global model manager instance
model_manager = ModelManager()


def get_model_manager():
    """Get the global model manager instance."""
    return model_manager