"""
Configuration settings for ABSA project
"""

# Model settings
STANZA_LANGUAGE = 'en'
NLTK_LANGUAGE = 'english'

# Dependency relations to consider for aspect-opinion linking
DEPENDENCY_RELATIONS = [
    "nsubj", "acl:relcl", "obj", "dobj", "agent", 
    "advmod", "amod", "neg", "prep_of", "acomp", 
    "xcomp", "compound"
]

# POS tags to consider as potential aspects/features
FEATURE_POS_TAGS = ['JJ', 'NN', 'JJR', 'NNS', 'RB']

# Sentiment score thresholds
POSITIVE_THRESHOLD = 0.1
NEGATIVE_THRESHOLD = -0.1

# NLTK resources to download
NLTK_RESOURCES = [
    'stopwords',
    'vader_lexicon', 
    'punkt',
    'averaged_perceptron_tagger',
    'punkt_tab',
    'averaged_perceptron_tagger_eng'
]

# Package requirements
REQUIREMENTS = [
    'pandas>=2.0.0',
    'numpy>=1.24.0',
    'nltk>=3.8.0',
    'stanza>=1.7.0'
]