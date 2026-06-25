"""
Test Examples and Test Cases for ABSA

This module contains predefined test cases and utilities for testing
the ABSA functionality.
"""

from src.core.absa_engine import aspect_sentiment_analysis


class TestRunner:
    """Manages and runs test cases for ABSA."""
    
    def __init__(self):
        self.test_cases = [
            {
                "name": "Phone Review",
                "text": "The battery life of this phone is excellent, but the camera quality is disappointing.",
                "expected_aspects": ["battery", "life", "camera", "quality"]
            },
            {
                "name": "Person Description", 
                "text": "Shreyas is intelligent but he is very lazy.",
                "expected_aspects": ["intelligent", "lazy"]
            },
            {
                "name": "Food Review",
                "text": "The ice cream is great but the waffle is hard to eat.",
                "expected_aspects": ["cream", "waffle"]
            },
            {
                "name": "Dress Review",
                "text": "Quality of the dress is good but the colour is dull",
                "expected_aspects": ["quality", "dress", "colour"]
            },
            {
                "name": "Book Review",
                "text": "Appearance of the cover page is beautiful but paper quality is poor",
                "expected_aspects": ["appearance", "cover", "page", "paper", "quality"]
            },
            {
                "name": "Movie Experience",
                "text": "The movie was super but the screen and sound quality in the theatre were horrible",
                "expected_aspects": ["movie", "screen", "sound", "quality", "theatre"]
            },
            {
                "name": "Self Description",
                "text": "i am an bad guy but also good at the same time",
                "expected_aspects": ["guy", "good"]
            },
            {
                "name": "Phone Review (with special character)",
                "text": "The battery life of this phone is excellent, but the camera quality is disappointing.",
                "expected_aspects": ["battery", "life", "camera", "quality"]
            }
        ]
    
    def run_all_tests(self, stop_words, nlp, sid):
        """
        Run all predefined test cases.
        
        Args:
            stop_words (set): Set of English stopwords
            nlp: Stanza NLP pipeline object
            sid: NLTK SentimentIntensityAnalyzer object
        """
        print("Running ABSA Test Examples")
        print("=" * 50)
        
        for i, test_case in enumerate(self.test_cases, 1):
            print(f"\nTest {i}: {test_case['name']}")
            print(f"Input: {test_case['text']}")
            
            try:
                result = aspect_sentiment_analysis(test_case['text'], stop_words, nlp, sid)
                print(f"Result: {result}")
                
                # Basic validation
                if result:
                    aspects_found = [aspect[0] for aspect in result]
                    print(f"Aspects found: {aspects_found}")
                else:
                    print("No aspects detected")
                    
            except Exception as e:
                print(f"Error: {e}")
            
            print("-" * 40)
    
    def run_single_test(self, text, stop_words, nlp, sid):
        """
        Run ABSA on a single text input.
        
        Args:
            text (str): Input text to analyze
            stop_words (set): Set of English stopwords
            nlp: Stanza NLP pipeline object
            sid: NLTK SentimentIntensityAnalyzer object
        
        Returns:
            list: ABSA results
        """
        try:
            result = aspect_sentiment_analysis(text, stop_words, nlp, sid)
            return result
        except Exception as e:
            print(f"Error analyzing text: {e}")
            return []
    
    def add_test_case(self, name, text, expected_aspects=None):
        """
        Add a new test case.
        
        Args:
            name (str): Name of the test case
            text (str): Test text
            expected_aspects (list): Expected aspects (optional)
        """
        test_case = {
            "name": name,
            "text": text,
            "expected_aspects": expected_aspects or []
        }
        self.test_cases.append(test_case)
        print(f"Added test case: {name}")


# Global test runner instance
test_runner = TestRunner()


def get_test_runner():
    """Get the global test runner instance."""
    return test_runner


if __name__ == "__main__":
    from src.models.model_manager import get_model_manager
    from src.utils.text_processing import get_stopwords
    
    # Setup components
    manager = get_model_manager()
    if manager.setup_all():
        nlp, sid = manager.get_models()
        stop_words = get_stopwords()
        
        if nlp and sid and stop_words:
            # Run test examples
            test_runner.run_all_tests(stop_words, nlp, sid)
        else:
            print("Failed to initialize components")
    else:
        print("Setup failed. Cannot run tests.")