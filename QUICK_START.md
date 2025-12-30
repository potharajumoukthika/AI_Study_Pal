# Quick Start Guide - AI Study Pal

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation Steps

### Step 1: Install Dependencies

Open terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

### Step 2: Initialize Project (Optional but Recommended)

Run the setup script to download NLTK data and train initial models:

```bash
python setup.py
```

**OR** manually download NLTK data:

```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

### Step 3: Run the Application

**Option A: Using Python directly**
```bash
python app.py
```

**Option B: Using batch file (Windows)**
```bash
run_app.bat
```

**Option C: Using shell script (Linux/Mac)**
```bash
bash run_app.sh
```

### Step 4: Access the Application

Open your web browser and go to:
```
http://localhost:5000
```

## First Use

1. **Enter Subject**: Type a subject name (e.g., "Mathematics", "Science", "History")
2. **Enter Hours**: Specify total study hours (e.g., 10)
3. **Select Scenario**: Choose from:
   - Exam Preparation (7 days, 2 sessions/day)
   - Homework Help (3 days, 1 session/day)
   - Regular Study (5 days, 1 session/day)
4. **Optional Text**: Paste educational text for summarization and tips
5. **Click "Generate Study Plan"**

## What You'll Get

- ✅ **Personalized Study Schedule**: Day-by-day plan with topics and activities
- ✅ **Practice Quiz**: 5 multiple-choice questions with difficulty levels
- ✅ **Text Summary**: Condensed version of your input text (if provided)
- ✅ **Study Tips**: AI-generated tips based on your subject and text
- ✅ **Resource Suggestions**: Recommended websites and study materials
- ✅ **Motivational Feedback**: Encouraging messages to keep you motivated
- ✅ **CSV Download**: Download your study schedule as a CSV file

## Troubleshooting

### Issue: "Module not found" error
**Solution**: Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: "NLTK data not found"
**Solution**: Run setup script or manually download:
```bash
python setup.py
```

### Issue: Port 5000 already in use
**Solution**: Change port in `app.py` line 235:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001 or any available port
```

### Issue: Models not loading
**Solution**: The app will automatically train models on first run if they don't exist. Wait for initialization to complete.

## Example Usage

### Example 1: Mathematics Exam Prep
- Subject: Mathematics
- Hours: 15
- Scenario: Exam Preparation
- Text: (optional) "Algebra is a branch of mathematics..."

**Result**: 7-day study plan with 2 sessions per day, algebra-focused quiz, tips, and resources.

### Example 2: Science Homework
- Subject: Science
- Hours: 5
- Scenario: Homework Help
- Text: "Physics is the study of matter and energy..."

**Result**: 3-day focused plan, physics quiz, summary of your text, science-specific tips.

## Next Steps

- Explore the Jupyter notebooks in `notebooks/` folder
- Read `PROJECT_DOCUMENTATION.md` for detailed information
- Customize quiz questions in `src/ml_quiz_generator.py`
- Add more subjects and resources in `src/resource_suggestions.py`

## Support

For detailed documentation, see:
- `README.md` - Project overview
- `PROJECT_DOCUMENTATION.md` - Complete technical documentation

---

**Happy Studying! 🎓**


