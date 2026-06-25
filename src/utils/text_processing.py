"""
Text Processing Utilities for ABSA

This module contains utilities for text preprocessing, tokenization,
and other text-related operations.
"""

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords


def preprocess_text(text):
    """
    Basic text preprocessing.
    
    Args:
        text (str): Input text
        
    Returns:
        str: Preprocessed text
    """
    return text.lower().strip()


def get_stopwords(language='english'):
    """
    Get stopwords for specified language.
    
    Args:
        language (str): Language for stopwords
        
    Returns:
        set: Set of stopwords
    """
    try:
        return set(stopwords.words(language))
    except Exception as e:
        print(f"Error loading stopwords: {e}")
        return set()


def tokenize_sentences(text):
    """
    Tokenize text into sentences.
    
    Args:
        text (str): Input text
        
    Returns:
        list: List of sentences
    """
    return sent_tokenize(text)


def tokenize_words(text):
    """
    Tokenize text into words.
    
    Args:
        text (str): Input text
        
    Returns:
        list: List of words
    """
    return word_tokenize(text)


def pos_tag_words(words):
    """
    Perform part-of-speech tagging on words.
    
    Args:
        words (list): List of words
        
    Returns:
        list: List of (word, pos_tag) tuples
    """
    return nltk.pos_tag(words)


def filter_stopwords(words, stop_words):
    """
    Filter out stopwords from word list.
    
    Args:
        words (list): List of words
        stop_words (set): Set of stopwords
        
    Returns:
        list: Filtered word list
    """
    return [w for w in words if w not in stop_words]