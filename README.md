# AI Study Pal - Capstone Project

A comprehensive AI-powered study assistant web application that integrates Machine Learning, Deep Learning, and NLP to help students create personalized study plans, generate quizzes, summarize texts, and receive study tips.

## Features

- **AI-Generated Study Plans**: Creates personalized study schedules based on subject and available hours
- **Automated Quiz System**: Generates multiple-choice quizzes with difficulty classification (easy/medium)
- **Text Summarization**: Summarizes educational texts using deep learning
- **Study Tips Generator**: Provides NLP-based study tips from text analysis
- **Resource Suggestions**: Recommends study resources using topic clustering
- **Downloadable Schedules**: Export study plans as CSV files

## Project Structure

```
AI STUDY PAL/
├── app.py                 # Flask main application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── data/                 # Datasets and data files
│   ├── educational_texts.csv
│   └── user_inputs.json
├── models/               # Saved ML/DL models
├── notebooks/            # Jupyter notebooks for development
│   ├── 01_data_processing.ipynb
│   ├── 02_ml_training.ipynb
│   └── 03_dl_training.ipynb
├── src/                  # Source code modules
│   ├── data_processing.py
│   ├── ml_quiz_generator.py
│   ├── dl_summarizer.py
│   ├── nlp_tips.py
│   └── resource_suggestions.py
├── templates/            # HTML templates
│   ├── index.html
│   └── results.html
└── static/               # CSS and JavaScript files
    ├── style.css
    └── script.js
```

## Installation

1. Clone the repository or navigate to the project directory
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download NLTK data:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

4. Run the Flask application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Enter your subject and available study hours
2. Select your study scenario (exam prep, homework, etc.)
3. Optionally provide text for summarization and tips
4. Click "Generate Study Plan" to get:
   - Personalized study schedule
   - Practice quiz
   - Text summary (if provided)
   - Study tips
   - Resource suggestions
5. Download your study schedule as CSV

## Technologies Used

- **Python**: Core programming language
- **Flask**: Web framework
- **Pandas**: Data manipulation and analysis
- **Matplotlib**: Data visualization
- **scikit-learn**: Machine learning (Logistic Regression, K-means)
- **Keras/TensorFlow**: Deep learning for text summarization
- **NLTK**: Natural language processing

## Model Details

- **Quiz Generator**: Logistic Regression classifier for difficulty classification
- **Resource Suggestions**: K-means clustering for topic grouping
- **Text Summarizer**: Neural network with LSTM layers
- **Study Tips**: NLTK-based keyword extraction and tokenization

## Evaluation Metrics

- ML Models: Accuracy, F1-score for quiz difficulty classification
- DL Models: Human evaluation for summary quality
- Web App: Usability and output clarity

## Author

AI Capstone Project - Educational Support System

## License

Educational Project - For Learning Purposes


