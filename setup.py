"""
Setup script for AI Study Pal
Run this to initialize the project and download required data
"""

import nltk
import os

def download_nltk_data():
    """Download required NLTK data"""
    print("Downloading NLTK data...")
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        print("✓ NLTK data downloaded successfully")
    except Exception as e:
        print(f"Error downloading NLTK data: {e}")

def create_directories():
    """Create necessary directories"""
    print("Creating directories...")
    directories = ['data', 'models', 'notebooks', 'src', 'templates', 'static']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✓ Directories created")

def initialize_data():
    """Initialize sample data"""
    print("Initializing sample data...")
    try:
        from src.data_processing import DataProcessor
        processor = DataProcessor()
        df = processor.create_sample_dataset()
        print(f"✓ Sample dataset created with {len(df)} entries")
    except Exception as e:
        print(f"Error initializing data: {e}")

def train_models():
    """Train initial models"""
    print("Training models...")
    try:
        from src.data_processing import DataProcessor
        from src.ml_quiz_generator import QuizGenerator
        from src.resource_suggestions import ResourceSuggester
        
        processor = DataProcessor()
        df = processor.load_educational_texts()
        df_clean = processor.clean_text_data(df)
        
        # Train quiz generator
        quiz_gen = QuizGenerator()
        results = quiz_gen.train_difficulty_classifier(df_clean)
        print(f"✓ Quiz generator trained (Accuracy: {results['accuracy']:.4f})")
        
        # Train resource suggester
        resource_sug = ResourceSuggester()
        cluster_results = resource_sug.train_clusterer(df_clean)
        print(f"✓ Resource suggester trained ({cluster_results['n_clusters']} clusters)")
        
    except Exception as e:
        print(f"Error training models: {e}")

if __name__ == '__main__':
    print("=" * 50)
    print("AI Study Pal - Setup")
    print("=" * 50)
    
    create_directories()
    download_nltk_data()
    initialize_data()
    train_models()
    
    print("\n" + "=" * 50)
    print("Setup complete! You can now run: python app.py")
    print("=" * 50)


