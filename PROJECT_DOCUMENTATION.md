# AI Study Pal - Project Documentation

## Project Overview

AI Study Pal is a comprehensive web-based study assistant application that integrates Machine Learning, Deep Learning, and Natural Language Processing to help students create personalized study plans, generate practice quizzes, summarize educational texts, and receive study tips.

## Architecture

### Technology Stack
- **Backend**: Flask (Python web framework)
- **Machine Learning**: scikit-learn (Logistic Regression, K-means)
- **Deep Learning**: Keras/TensorFlow (Text Summarization)
- **NLP**: NLTK (Tokenization, Keyword Extraction)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib
- **Frontend**: HTML, CSS, JavaScript

### Project Structure

```
AI STUDY PAL/
├── app.py                      # Main Flask application
├── setup.py                    # Setup script for initialization
├── requirements.txt            # Python dependencies
├── README.md                   # Project overview
├── PROJECT_DOCUMENTATION.md   # This file
├── .gitignore                 # Git ignore rules
│
├── data/                      # Data storage
│   ├── educational_texts.csv # Sample educational dataset
│   └── user_inputs.json      # User input history
│
├── models/                    # Trained models
│   ├── difficulty_model.pkl  # Quiz difficulty classifier
│   ├── vectorizer.pkl        # Text vectorizer
│   ├── clusterer.pkl         # Topic clusterer
│   └── resource_vectorizer.pkl # Resource vectorizer
│
├── notebooks/                 # Jupyter notebooks
│   ├── 01_data_processing.ipynb
│   ├── 02_ml_training.ipynb
│   └── 03_dl_training.ipynb
│
├── src/                       # Source code modules
│   ├── __init__.py
│   ├── data_processing.py    # Data collection & cleaning
│   ├── ml_quiz_generator.py  # ML quiz generation
│   ├── dl_summarizer.py      # DL text summarization
│   ├── nlp_tips.py           # NLP study tips
│   └── resource_suggestions.py # Resource recommendations
│
├── templates/                 # HTML templates
│   └── index.html            # Main web interface
│
└── static/                    # Static files
    ├── style.css             # Stylesheet
    └── script.js             # Frontend JavaScript
```

## Core Features Implementation

### 1. Data Processing Module (`src/data_processing.py`)

**Purpose**: Handles data collection, cleaning, and exploratory data analysis.

**Key Functions**:
- `create_sample_dataset()`: Creates sample educational texts dataset
- `load_educational_texts()`: Loads educational texts from CSV
- `clean_text_data()`: Removes duplicates, normalizes text
- `perform_eda()`: Generates visualizations (pie charts, bar charts, histograms)
- `save_user_input()`: Saves user inputs to JSON

**Output**: Cleaned dataset, EDA visualizations (PNG files)

### 2. Machine Learning Quiz Generator (`src/ml_quiz_generator.py`)

**Purpose**: Generates quizzes with difficulty classification using Logistic Regression.

**Key Functions**:
- `train_difficulty_classifier()`: Trains logistic regression model
- `generate_quiz()`: Creates multiple-choice questions
- `classify_difficulty()`: Classifies question difficulty (easy/medium)

**Model Details**:
- **Algorithm**: Logistic Regression
- **Features**: Bag-of-Words (CountVectorizer)
- **Evaluation**: Accuracy, F1-score
- **Output**: Quiz questions with difficulty labels

### 3. Resource Suggestion System (`src/resource_suggestions.py`)

**Purpose**: Recommends study resources using K-means clustering.

**Key Functions**:
- `train_clusterer()`: Trains K-means clusterer
- `suggest_resources()`: Returns relevant study resources
- `get_cluster_resources()`: Gets resources based on text clustering

**Model Details**:
- **Algorithm**: K-means Clustering
- **Features**: TF-IDF Vectorization
- **Evaluation**: Silhouette Score
- **Output**: Recommended study resources (websites, links)

### 4. Deep Learning Text Summarizer (`src/dl_summarizer.py`)

**Purpose**: Summarizes educational texts and generates motivational feedback.

**Key Functions**:
- `summarize_text()`: Extractive summarization
- `generate_feedback()`: Creates motivational messages
- `generate_study_feedback()`: Feedback based on quiz performance

**Implementation**:
- **Method**: Extractive summarization (sentence scoring)
- **Future Enhancement**: Neural network-based abstractive summarization
- **Output**: Summarized text, motivational feedback

### 5. NLP Study Tips Generator (`src/nlp_tips.py`)

**Purpose**: Generates study tips using NLP techniques.

**Key Functions**:
- `extract_keywords()`: Extracts top keywords using NLTK
- `generate_tips_from_text()`: Creates tips from text analysis
- `generate_subject_specific_tips()`: Subject-specific recommendations
- `generate_comprehensive_tips()`: Combines all tip generation methods

**NLP Techniques**:
- Tokenization (NLTK)
- Stopword removal
- Lemmatization
- Keyword frequency analysis
- **Output**: Personalized study tips

### 6. Flask Web Application (`app.py`)

**Purpose**: Main web application integrating all components.

**Routes**:
- `GET /`: Main page with input form
- `POST /generate`: Generates study plan and all features
- `POST /download_schedule`: Downloads study schedule as CSV
- `GET /health`: Health check endpoint

**Features**:
- User input form (subject, hours, scenario, text)
- Study schedule generation
- Quiz display
- Summary display
- Tips display
- Resource suggestions
- CSV download functionality

## Workflow

1. **User Input**: User provides subject, study hours, scenario, and optional text
2. **Data Processing**: Input saved, dataset loaded/cleaned
3. **Study Plan Generation**: Creates personalized schedule based on inputs
4. **Quiz Generation**: ML model generates questions with difficulty classification
5. **Text Summarization**: DL model summarizes provided text
6. **Tips Generation**: NLP extracts keywords and generates tips
7. **Resource Suggestions**: K-means clustering suggests relevant resources
8. **Feedback Generation**: DL model creates motivational feedback
9. **Output Display**: All results displayed on web interface
10. **CSV Download**: User can download study schedule

## Model Training

### Quiz Difficulty Classifier
- **Training Data**: Educational texts with difficulty labels
- **Features**: Bag-of-Words representation (100 features)
- **Model**: Logistic Regression (C=1.0, max_iter=1000)
- **Metrics**: Accuracy, F1-score
- **Saved Model**: `models/difficulty_model.pkl`

### Resource Clusterer
- **Training Data**: Subject-topic-text combinations
- **Features**: TF-IDF vectors (50 features)
- **Model**: K-means (optimal clusters determined by silhouette score)
- **Metrics**: Silhouette Score
- **Saved Model**: `models/clusterer.pkl`

## Evaluation Metrics

### Machine Learning Models
- **Accuracy**: Percentage of correct difficulty classifications
- **F1-Score**: Weighted F1-score for difficulty classification
- **Silhouette Score**: Quality of topic clustering

### Deep Learning Models
- **Compression Ratio**: Summary length / Original length
- **Human Evaluation**: Quality of summaries and feedback (manual)

### Web Application
- **Usability**: User-friendly interface
- **Output Clarity**: Clear, organized results
- **Functionality**: All features working correctly

## Usage Instructions

### Installation

1. **Clone/Navigate to project directory**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data** (or run setup.py):
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   nltk.download('wordnet')
   ```

4. **Run setup script** (optional, initializes data and trains models):
   ```bash
   python setup.py
   ```

### Running the Application

**Option 1: Direct execution**
```bash
python app.py
```

**Option 2: Using batch/shell script**
- Windows: `run_app.bat`
- Linux/Mac: `bash run_app.sh`

**Option 3: Using Flask CLI**
```bash
flask run
```

### Accessing the Application

Open your browser and navigate to: `http://localhost:5000`

### Using the Application

1. Enter subject name (e.g., Mathematics, Science)
2. Enter total study hours (e.g., 10)
3. Select study scenario (Exam Prep, Homework, Regular Study)
4. Optionally paste text for summarization
5. Click "Generate Study Plan"
6. Review generated:
   - Study schedule
   - Practice quiz
   - Text summary (if provided)
   - Study tips
   - Resource suggestions
   - Motivational feedback
7. Download schedule as CSV if needed

## Development Notebooks

### Notebook 1: Data Processing (`notebooks/01_data_processing.ipynb`)
- Load and explore dataset
- Clean data
- Perform EDA
- Generate visualizations

### Notebook 2: ML Training (`notebooks/02_ml_training.ipynb`)
- Train quiz difficulty classifier
- Evaluate model performance
- Test quiz generation
- Test difficulty classification

### Notebook 3: DL Training (`notebooks/03_dl_training.ipynb`)
- Test text summarization
- Test feedback generation
- Evaluate summarization quality

## Future Enhancements

1. **Abstractive Summarization**: Implement neural network-based summarization
2. **Advanced Quiz Generation**: Use GPT-like models for question generation
3. **User Accounts**: Add user authentication and progress tracking
4. **Adaptive Learning**: Personalize based on user performance
5. **Voice Output**: Add text-to-speech for accessibility
6. **Mobile App**: Develop mobile application version
7. **Multi-language Support**: Support multiple languages
8. **Advanced Analytics**: Track study patterns and performance

## Troubleshooting

### Common Issues

1. **NLTK Data Not Found**
   - Solution: Run `python setup.py` or manually download NLTK data

2. **Models Not Found**
   - Solution: Run `python setup.py` to train initial models

3. **Port Already in Use**
   - Solution: Change port in `app.py` or kill process using port 5000

4. **Import Errors**
   - Solution: Ensure all dependencies are installed: `pip install -r requirements.txt`

## Contributing

This is an educational capstone project. For improvements:
1. Follow Python PEP 8 style guidelines
2. Add comments and docstrings
3. Test all features before submitting
4. Update documentation as needed

## License

Educational Project - For Learning Purposes

## Contact

AI Capstone Project - Educational Support System

---

**Last Updated**: December 2024
**Version**: 1.0.0


