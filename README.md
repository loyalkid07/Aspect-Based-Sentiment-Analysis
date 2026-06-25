# Aspect-Based Sentiment Analysis (ABSA)

This project performs Aspect-Based Sentiment Analysis on text data. It extracts specific aspects or features from the text and determines the sentiment associated with each aspect using advanced Natural Language Processing techniques.

🌐 **Live Demo**: [Click to Try the App](https://aspect-based-sentiment-analyser.streamlit.app/)  
📂 **GitHub Repo**: [CHETHANSP27/Aspect-based-Sentimental-Analysis](https://github.com/CHETHANSP27/Aspect-based-Sentimental-Analysis)


## 🚀 Features

- **Interactive Command-Line Interface** with user-friendly prompts and help system
- **Comprehensive Test Suite** with predefined examples
- **Modular Architecture** for easy maintenance and future enhancements
- **Automatic Model Setup** with dependency management
- **Detailed Sentiment Analysis** with numerical scores and categorical labels
- **Real-time Analysis** of custom text inputs

## Project Structure

The project is organized into a modular structure for better maintainability and future enhancements:

```
Aspect-based-Sentimental-Analysis/
├── README.md                           # Project documentation
├── requirements.txt                    # Python dependencies
├── ABSA_(almost_there).ipynb          # Original Jupyter notebook
├── absa_main.py                       # Main entry point and interface
├── 
├── src/                               # Source code
│   ├── __init__.py
│   ├── core/                          # Core ABSA algorithms
│   │   ├── __init__.py
│   │   └── absa_engine.py             # Main ABSA algorithm
│   ├── models/                        # Model management
│   │   ├── __init__.py
│   │   └── model_manager.py           # NLP model initialization
│   └── utils/                         # Utility functions
│       ├── __init__.py
│       └── text_processing.py         # Text processing utilities
├── 
├── tests/                             # Test cases and examples
│   ├── __init__.py
│   └── test_cases.py                  # Predefined test examples
├── 
├── config/                            # Configuration files
│   ├── __init__.py
│   └── settings.py                    # Project settings and constants
├── 
└── docs/                              # Documentation (future)
    └── (future documentation files)
```

### Module Descriptions:

#### Core Modules (`src/`):
- **`src/core/absa_engine.py`**: Contains the main `aspect_sentiment_analysis()` function with the core ABSA logic
- **`src/models/model_manager.py`**: Manages NLP model initialization (Stanza, NLTK) with the `ModelManager` class
- **`src/utils/text_processing.py`**: Text preprocessing utilities (tokenization, POS tagging, stopword filtering)

#### Interface and Testing:
- **`absa_main.py`**: Main interface providing the `ABSAAnalyzer` class and interactive mode
- **`tests/test_cases.py`**: Comprehensive test suite with the `TestRunner` class

#### Configuration:
- **`config/settings.py`**: Centralized configuration for thresholds, POS tags, dependencies, etc.
- **`requirements.txt`**: Python package dependencies

## Project Description

Aspect-Based Sentiment Analysis is a text analysis technique that breaks down text into aspects (attributes or components of a product or service) and then allocates a sentiment level (positive, negative, neutral) to each one.

This implementation uses a combination of Natural Language Processing (NLP) libraries to achieve this:

-   **NLTK (Natural Language Toolkit):** Used for fundamental NLP tasks like sentence tokenization, word tokenization, Part-of-Speech (POS) tagging, and stop-word removal. It also provides the VADER sentiment analysis tool.
-   **Stanza:** A powerful NLP library from Stanford, used here for dependency parsing to understand the grammatical structure of sentences and identify relationships between words. This is crucial for linking opinion words (like "excellent") to aspect words (like "battery").

The overall workflow is as follows:
1.  The input text is processed to clean and structure it.
2.  Sentences are broken down and tagged for parts of speech.
3.  Stanza's dependency parser analyzes the sentence structure.
4.  The code identifies potential aspects (typically nouns) and opinion words (typically adjectives).
5.  By analyzing the dependency relations, the code links opinion words to the aspects they describe.
6.  The sentiment for each aspect is calculated using NLTK's VADER (Valence Aware Dictionary and sEntiment Reasoner).

## Installation and Setup

### Quick Setup (Recommended)

1. **Clone/Download:** Get all the project files
2. **Run Setup Script:**
   ```bash
   python setup_project.py
   ```
   This automated setup will:
   - Verify the complete directory structure
   - Install all required dependencies automatically
   - Optionally setup NLP models (or they'll download on first use)
   - Validate the installation

3. **Start Using:**
   ```bash
   python absa_main.py
   ```

### Alternative Setup Methods

#### Option 1: Using pip and requirements.txt

```bash
pip install -r requirements.txt
python absa_main.py
```

#### Option 2: Manual Installation

```bash
pip install pandas numpy nltk stanza
python absa_main.py
```

### First Run Setup

If you didn't setup models during installation, they will be automatically downloaded on first use. The first run may take a few minutes to download NLTK data and Stanza models.

## How to Use

### Option 1: Interactive Mode (Recommended for Beginners)

```bash
python absa_main.py
```

**Features of Interactive Mode:**
- **User-friendly interface** with clear instructions and examples
- **Built-in help system** - type `help` for detailed guidance
- **Test examples** - type `test` to see predefined examples
- **Real-time analysis** - simply type any text to analyze
- **Visual formatting** with clear result presentation

**Available Commands:**
- Enter any text to analyze aspects and sentiments
- `test` or `tests` - Run predefined test examples
- `help` or `h` - Show detailed help information
- `quit`, `exit`, or `q` - Exit the program

**Example Session:**
```
> The battery life is excellent but the camera is poor
Analyzing: The battery life is excellent but the camera is poor
Found 4 aspects:
  • battery: 0.000 (Neutral)
  • life: 0.659 (Positive)
  • camera: 0.000 (Neutral)
  • poor: -0.477 (Negative)
```

### Option 2: Command Line Testing

```bash
# Run all test examples directly
python absa_main.py --test
```

### Option 3: Using as Python Library

```python
from absa_main import ABSAAnalyzer

# Initialize the analyzer (handles all setup automatically)
analyzer = ABSAAnalyzer()

# Basic analysis
text = "The food was delicious but the service was slow"
results = analyzer.analyze(text)
print(results)  # [['food', 0.0], ['delicious', 0.6249], ...]

# Detailed analysis with labels
detailed_results = analyzer.analyze_with_details(text)
for aspect_info in detailed_results['aspects']:
    print(f"{aspect_info['aspect']}: {aspect_info['sentiment_label']} ({aspect_info['sentiment_score']:.3f})")
```

### Option 4: Using Individual Modules (Advanced)

```python
from src.models.model_manager import get_model_manager
from src.core.absa_engine import aspect_sentiment_analysis
from src.utils.text_processing import get_stopwords

# Setup components manually
manager = get_model_manager()
if manager.setup_all():
    nlp, sid = manager.get_models()
    stop_words = get_stopwords()
    
    # Analyze text with core function
    text = "Your text here"
    results = aspect_sentiment_analysis(text, stop_words, nlp, sid)
```

### Option 5: Using the Jupyter Notebook

1. Open `ABSA_(almost_there).ipynb` in Jupyter Notebook or Jupyter Lab
2. Run the cells sequentially
3. The notebook now includes references to the modular structure

## Usage Examples

### Interactive Mode Examples

The system provides an intuitive interface with helpful prompts:

```bash
$ python absa_main.py

============================================================
ABSA INTERACTIVE MODE
============================================================
Welcome to the Aspect-Based Sentiment Analysis tool!

Available commands:
  • Enter any text to analyze aspects and sentiments
  • 'test' or 'tests' - Run predefined test examples
  • 'help' - Show this help message
  • 'quit', 'exit', or 'q' - Exit the program

Example: 'The battery life is excellent but the camera is poor'

> The restaurant has amazing food but terrible service
Analyzing: The restaurant has amazing food but terrible service
Found 4 aspects:
  • restaurant: 0.000 (Neutral)
  • amazing: 0.593 (Positive)
  • food: 0.000 (Neutral)
  • terrible: -0.649 (Negative)

> help
==================================================
HELP - Available Commands:
==================================================
• Text Analysis:
  - Simply type any text to analyze its aspects and sentiments
  - Example: 'The food was delicious but service was slow'

• Commands:
  - 'test' or 'tests' - Run all predefined test examples
  - 'help' or 'h' - Show this help message
  - 'quit', 'exit', or 'q' - Exit the program

• How it works:
  - The system identifies aspects (nouns) and their sentiments
  - Sentiment scores range from -1.0 (very negative) to +1.0 (very positive)
  - Scores between -0.1 and +0.1 are considered neutral
==================================================
```

### Programmatic Usage Examples

```python
from absa_main import ABSAAnalyzer

# Initialize analyzer
analyzer = ABSAAnalyzer()

# Example 1: Product Review
review = "The battery life of this phone is excellent, but the camera quality is disappointing."
results = analyzer.analyze_with_details(review)

print(f"Analysis of: {results['input_text']}")
print(f"Aspects found: {results['aspects_found']}")
for aspect in results['aspects']:
    print(f"  {aspect['aspect']}: {aspect['sentiment_label']} ({aspect['sentiment_score']:.3f})")

# Example 2: Restaurant Review
restaurant_review = "The food was delicious and the atmosphere was cozy, but the service was slow."
simple_results = analyzer.analyze(restaurant_review)
print(f"Simple results: {simple_results}")
```

### Expected Output Formats

**Simple Analysis Output:**
```python
[['battery', 0.0], ['life', 0.6588], ['phone', 0.0], ['excellent', 0.6588], ['camera', 0.0], ['quality', 0.0], ['disappointing', -0.4767]]
```

**Detailed Analysis Output:**
```python
{
    'input_text': 'The battery life is excellent but the camera is poor',
    'aspects_found': 4,
    'aspects': [
        {'aspect': 'battery', 'sentiment_score': 0.0, 'sentiment_label': 'Neutral'},
        {'aspect': 'life', 'sentiment_score': 0.659, 'sentiment_label': 'Positive'},
        {'aspect': 'camera', 'sentiment_score': 0.0, 'sentiment_label': 'Neutral'},
        {'aspect': 'poor', 'sentiment_score': -0.477, 'sentiment_label': 'Negative'}
    ]
}
```

## Code Structure and Logic

### Core Algorithm: `src/core/absa_engine.py`

The main `aspect_sentiment_analysis()` function performs the following steps:

1. **Text Preprocessing:** Converts text to lowercase and tokenizes into sentences
2. **POS Tagging:** Identifies parts of speech for each word using NLTK
3. **Noun Phrase Merging:** Combines consecutive nouns into compound aspects
4. **Stopword Filtering:** Removes common English stopwords
5. **Dependency Parsing:** Uses Stanza to understand grammatical relationships
6. **Feature Extraction:** Identifies potential aspects (nouns, adjectives, adverbs)
7. **Dependency Matching:** Links opinion words to aspects using predefined dependency relationships
8. **Sentiment Analysis:** Applies VADER sentiment analysis to each identified aspect

### Model Management: `src/models/model_manager.py`

The `ModelManager` class handles:
- Automatic installation of required packages
- Downloading of NLTK resources
- Initialization of Stanza pipeline
- Setup of VADER sentiment analyzer
- Centralized model access

### Text Processing: `src/utils/text_processing.py`

Utility functions for:
- Text preprocessing and normalization
- Tokenization (sentences and words)
- POS tagging
- Stopword management

### Configuration: `config/settings.py`

Centralized configuration for:
- Model settings and thresholds
- POS tags to consider as features
- Dependency relations for aspect-opinion linking
- Package requirements

### Key Parameters:

- `txt`: Input text string
- `stop_words`: Set of English stopwords to filter out
- `nlp`: Stanza pipeline object for dependency parsing
- `sid`: NLTK SentimentIntensityAnalyzer for sentiment scoring

## Testing

Run the test examples to see the system in action:

```bash
python test_examples.py
```

This will run all the predefined test cases and show the results.

## Future Enhancements

The project offers several opportunities for improvement:

### Immediate Improvements:
-   **Enhanced Sentiment Context:** Modify sentiment analysis to consider opinion words in relation to aspects, not just the aspect words themselves
-   **Better Output Format:** Return structured results as dictionaries with clearer aspect-sentiment mappings
-   **Error Handling:** Add robust error handling and validation for edge cases

### Advanced Features:
-   **Aspect Clustering:** Group similar aspects (e.g., "picture quality" and "photo clarity" → "camera")
-   **Implicit Aspect Detection:** Detect aspects that aren't explicitly mentioned (e.g., "expensive" → "price")
-   **Multi-language Support:** Extend to other languages beyond English
-   **Confidence Scores:** Add confidence levels to aspect-sentiment predictions

### Technical Improvements:
-   **Performance Optimization:** Cache models and optimize processing for large datasets
-   **Configuration Management:** Centralized settings in `config/settings.py` for easy customization
-   **Comprehensive Logging:** Implement detailed logging for debugging and monitoring
-   **Unit Tests:** Expand test suite with comprehensive unit tests for all modules
-   **Error Handling:** Enhanced error handling with informative error messages
-   **Documentation:** Auto-generated API documentation

### Advanced Models:
-   **BERT Integration:** Use transformer models for more accurate aspect extraction and sentiment analysis
-   **Custom Training:** Train domain-specific models for better accuracy in specific industries
-   **Deep Learning:** Implement neural network approaches for aspect-based sentiment analysis
-   **Ensemble Methods:** Combine multiple models for improved accuracy

### User Interface:
-   **Web Interface:** Create a Flask/Streamlit web app for easy browser-based access
-   **REST API:** Develop a comprehensive API for integration with other applications
-   **Batch Processing:** Add support for analyzing multiple texts and CSV files
-   **Data Visualization:** Create interactive charts and graphs to visualize sentiment analysis results
-   **Export Features:** Add functionality to export results to JSON, CSV, and other formats

## 🧪 Testing

The project includes comprehensive testing capabilities:

### Running Tests

```bash
# Run all predefined test examples
python absa_main.py --test

# Run tests through the test module
python tests/test_cases.py

# Interactive testing
python absa_main.py
> test
```

### Test Cases Included

1. **Phone Review**: Battery and camera analysis
2. **Person Description**: Character trait analysis  
3. **Food Review**: Ice cream and waffle evaluation
4. **Dress Review**: Quality and color assessment
5. **Book Review**: Appearance and paper quality
6. **Movie Experience**: Film and theater quality
7. **Self Description**: Personal characteristic analysis
8. **Special Characters**: Handling of non-standard text

## 🛠️ Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're running from the project root directory
2. **Model Download Fails**: Check internet connection and try running setup again
3. **NLTK Resource Errors**: Run `python setup_project.py` to download missing resources
4. **Stanza Pipeline Errors**: Ensure sufficient disk space for model downloads

### Getting Help

- Use the built-in help: Type `help` in interactive mode
- Check the console output for detailed error messages
- Verify installation with `python setup_project.py`

## Contributing

This project is actively maintained and welcomes contributions! Here are ways to contribute:

### Areas for Contribution:
- **Algorithm Improvements**: Enhance the core ABSA algorithm
- **New Features**: Implement features from the future enhancements list
- **Testing**: Add more test cases and improve test coverage
- **Documentation**: Improve documentation and add examples
- **Bug Fixes**: Report and fix issues

### Development Setup:
1. Fork the repository
2. Run `python setup_project.py` to set up the development environment
3. Make your changes in the appropriate module directories
4. Test your changes with `python absa_main.py --test`
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **NLTK Team** for providing excellent natural language processing tools
- **Stanford NLP Group** for the Stanza library
- **Contributors** who help improve this project

---

**Note**: This project is named `ABSA_original` in the original notebook, indicating it's a work in progress. The modular restructure makes it production-ready while maintaining all original functionality.
