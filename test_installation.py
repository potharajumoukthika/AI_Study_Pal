"""
Test script to verify AI Study Pal installation
Run this to check if all dependencies are installed correctly
"""

import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    modules = [
        ('flask', 'Flask'),
        ('pandas', 'Pandas'),
        ('numpy', 'NumPy'),
        ('matplotlib', 'Matplotlib'),
        ('sklearn', 'scikit-learn'),
        ('keras', 'Keras'),
        ('nltk', 'NLTK'),
    ]
    
    failed = []
    
    for module_name, display_name in modules:
        try:
            __import__(module_name)
            print(f"[OK] {display_name}")
        except ImportError:
            print(f"[X] {display_name} - NOT INSTALLED")
            failed.append(display_name)
    
    return len(failed) == 0

def test_project_modules():
    """Test if project modules can be imported"""
    print("\nTesting project modules...")
    
    modules = [
        'src.data_processing',
        'src.ml_quiz_generator',
        'src.dl_summarizer',
        'src.nlp_tips',
        'src.resource_suggestions',
    ]
    
    failed = []
    
    for module_name in modules:
        try:
            __import__(module_name)
            print(f"[OK] {module_name}")
        except ImportError as e:
            print(f"[X] {module_name} - ERROR: {e}")
            failed.append(module_name)
    
    return len(failed) == 0

def test_nltk_data():
    """Test if NLTK data is available"""
    print("\nTesting NLTK data...")
    
    try:
        import nltk
        
        data_required = ['punkt', 'stopwords', 'wordnet']
        missing = []
        
        for data_name in data_required:
            try:
                if data_name == 'punkt':
                    nltk.data.find('tokenizers/punkt')
                    print(f"[OK] {data_name}")
                elif data_name == 'stopwords':
                    nltk.data.find('corpora/stopwords')
                    print(f"[OK] {data_name}")
                elif data_name == 'wordnet':
                    # Test wordnet by actually using it
                    try:
                        from nltk.corpus import wordnet
                        test_synsets = wordnet.synsets('test')
                        if len(test_synsets) > 0:
                            print(f"[OK] {data_name}")
                            continue
                    except Exception:
                        pass
                    # Fallback to file check
                    nltk.data.find('corpora/wordnet')
                    print(f"[OK] {data_name}")
            except LookupError:
                print(f"[X] {data_name} - NOT DOWNLOADED")
                missing.append(data_name)
        
        if missing:
            print(f"\nTo download missing NLTK data, run:")
            print(f"python -c \"import nltk; {'; '.join([f'nltk.download(\'{d}\')' for d in missing])}\"")
            return False
        
        return True
    except Exception as e:
        print(f"[X] Error checking NLTK: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of modules"""
    print("\nTesting basic functionality...")
    
    try:
        from src.data_processing import DataProcessor
        processor = DataProcessor()
        df = processor.load_educational_texts()
        print(f"[OK] Data processing - Loaded {len(df)} texts")
    except Exception as e:
        print(f"[X] Data processing - ERROR: {e}")
        return False
    
    try:
        from src.ml_quiz_generator import QuizGenerator
        quiz_gen = QuizGenerator()
        print("[OK] Quiz generator - Initialized")
    except Exception as e:
        print(f"[X] Quiz generator - ERROR: {e}")
        return False
    
    try:
        from src.dl_summarizer import TextSummarizer
        summarizer = TextSummarizer()
        test_summary = summarizer.summarize_text("This is a test text for summarization.")
        print(f"[OK] Text summarizer - Generated summary ({len(test_summary)} chars)")
    except Exception as e:
        print(f"[X] Text summarizer - ERROR: {e}")
        return False
    
    try:
        from src.nlp_tips import StudyTipsGenerator
        tips_gen = StudyTipsGenerator()
        tips = tips_gen.generate_generic_tips()
        print(f"[OK] Study tips generator - Generated {len(tips)} tips")
    except Exception as e:
        print(f"[X] Study tips generator - ERROR: {e}")
        return False
    
    try:
        from src.resource_suggestions import ResourceSuggester
        resource_sug = ResourceSuggester()
        resources = resource_sug.suggest_resources('Mathematics')
        print(f"[OK] Resource suggester - Found {len(resources)} resources")
    except Exception as e:
        print(f"[X] Resource suggester - ERROR: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("AI Study Pal - Installation Test")
    print("=" * 60)
    
    results = []
    
    results.append(("Dependencies", test_imports()))
    results.append(("Project Modules", test_project_modules()))
    results.append(("NLTK Data", test_nltk_data()))
    results.append(("Basic Functionality", test_basic_functionality()))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "PASSED" if passed else "FAILED"
        symbol = "[OK]" if passed else "[X]"
        print(f"{symbol} {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\nSUCCESS All tests passed! AI Study Pal is ready to use.")
        print("\nNext steps:")
        print("1. Run 'python setup.py' to initialize data and train models")
        print("2. Run 'python app.py' to start the web application")
        print("3. Open http://localhost:5000 in your browser")
    else:
        print("\nWARNING  Some tests failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("- Install missing dependencies: pip install -r requirements.txt")
        print("- Download NLTK data: python setup.py")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

