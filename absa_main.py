"""
Main ABSA Analyzer Interface

This module provides the main interface for the Aspect-Based Sentiment Analysis system.
It integrates all components and provides easy-to-use classes and functions.
"""

import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.absa_engine import aspect_sentiment_analysis
from src.models.model_manager import get_model_manager
from src.utils.text_processing import get_stopwords
from tests.test_cases import get_test_runner


class ABSAAnalyzer:
    """
    Main ABSA Analyzer class that encapsulates all functionality.
    """
    
    def __init__(self):
        """Initialize the ABSA analyzer with required components."""
        print("Initializing ABSA Analyzer...")
        
        self.model_manager = get_model_manager()
        self.test_runner = get_test_runner()
        
        # Setup models
        if self.model_manager.setup_all():
            self.nlp, self.sid = self.model_manager.get_models()
            self.stop_words = get_stopwords()
            print("✓ ABSA Analyzer ready!")
        else:
            print("✗ Failed to initialize ABSA Analyzer")
            self.nlp = None
            self.sid = None
            self.stop_words = None
    
    def analyze(self, text):
        """
        Analyze text for aspects and sentiments.
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            list: List of [aspect, sentiment_score] pairs
        """
        if not self.is_ready():
            print("Analyzer not properly initialized!")
            return []
        
        try:
            return aspect_sentiment_analysis(text, self.stop_words, self.nlp, self.sid)
        except Exception as e:
            print(f"Error during analysis: {e}")
            return []
    
    def analyze_with_details(self, text):
        """
        Analyze text and return detailed results with sentiment labels.
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            dict: Detailed analysis results
        """
        results = self.analyze(text)
        
        detailed_results = {
            'input_text': text,
            'aspects_found': len(results),
            'aspects': []
        }
        
        for aspect, sentiment_score in results:
            sentiment_label = self._get_sentiment_label(sentiment_score)
            detailed_results['aspects'].append({
                'aspect': aspect,
                'sentiment_score': sentiment_score,
                'sentiment_label': sentiment_label
            })
        
        return detailed_results
    
    def _get_sentiment_label(self, score):
        """Convert sentiment score to label."""
        if score > 0.1:
            return "Positive"
        elif score < -0.1:
            return "Negative"
        else:
            return "Neutral"
    
    def run_tests(self):
        """Run all predefined test examples."""
        if not self.is_ready():
            print("Analyzer not properly initialized!")
            return
        
        self.test_runner.run_all_tests(self.stop_words, self.nlp, self.sid)
    
    def is_ready(self):
        """Check if analyzer is ready to use."""
        return all([self.nlp, self.sid, self.stop_words])


def interactive_mode():
    """Run the analyzer in interactive mode."""
    analyzer = ABSAAnalyzer()
    
    if not analyzer.is_ready():
        print("Failed to initialize analyzer. Exiting...")
        return
    
    print("\n" + "="*60)
    print("ABSA INTERACTIVE MODE")
    print("="*60)
    print("Welcome to the Aspect-Based Sentiment Analysis tool!")
    print("\nAvailable commands:")
    print("  • Enter any text to analyze aspects and sentiments")
    print("  • 'test' or 'tests' - Run predefined test examples")
    print("  • 'help' - Show this help message")
    print("  • 'quit', 'exit', or 'q' - Exit the program")
    print("\nExample: 'The battery life is excellent but the camera is poor'")
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if user_input.lower() in ['test', 'tests']:
                print("\n" + "="*50)
                print("RUNNING TEST EXAMPLES")
                print("="*50)
                analyzer.run_tests()
                print("\n" + "="*50)
                print("TEST EXAMPLES COMPLETED")
                print("="*50)
                continue
            
            if user_input.lower() in ['help', 'h']:
                print("\n" + "="*50)
                print("HELP - Available Commands:")
                print("="*50)
                print("• Text Analysis:")
                print("  - Simply type any text to analyze its aspects and sentiments")
                print("  - Example: 'The food was delicious but service was slow'")
                print("\n• Commands:")
                print("  - 'test' or 'tests' - Run all predefined test examples")
                print("  - 'help' or 'h' - Show this help message")
                print("  - 'quit', 'exit', or 'q' - Exit the program")
                print("\n• How it works:")
                print("  - The system identifies aspects (nouns) and their sentiments")
                print("  - Sentiment scores range from -1.0 (very negative) to +1.0 (very positive)")
                print("  - Scores between -0.1 and +0.1 are considered neutral")
                print("="*50)
                continue
            
            if not user_input:
                print("💡 Tip: Enter some text to analyze, 'test' for examples, or 'help' for more info.")
                continue
            
            print(f"\nAnalyzing: {user_input}")
            detailed_results = analyzer.analyze_with_details(user_input)
            
            if detailed_results['aspects']:
                print(f"Found {detailed_results['aspects_found']} aspects:")
                for aspect_info in detailed_results['aspects']:
                    print(f"  • {aspect_info['aspect']}: {aspect_info['sentiment_score']:.3f} ({aspect_info['sentiment_label']})")
            else:
                print("No aspects found or analysis failed.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    # Check if user wants to run tests directly
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        analyzer = ABSAAnalyzer()
        if analyzer.is_ready():
            analyzer.run_tests()
    else:
        interactive_mode()