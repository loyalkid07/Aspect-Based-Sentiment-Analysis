"""Neural ABSA components based on an aspect-aware Attention Bi-LSTM."""

from src.neural.inference import AttentionBiLSTMPredictor
from src.neural.preprocessing import ABSAPreprocessor

__all__ = ["ABSAPreprocessor", "AttentionBiLSTMPredictor"]
