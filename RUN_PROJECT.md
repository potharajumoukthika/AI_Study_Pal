# Exact Terminal Steps to Run AI Study Pal

## Step-by-Step Instructions

### Step 1: Open Terminal/PowerShell
- Press `Win + X` and select "Windows PowerShell" or "Terminal"
- OR Press `Win + R`, type `powershell`, press Enter

### Step 2: Navigate to Project Directory
```powershell
cd "E:\AI STUDY PAL"
```

### Step 3: Verify You're in the Right Directory
```powershell
Get-Location
```
You should see: `E:\AI STUDY PAL`

### Step 4: Install Dependencies (if not already done)
```powershell
pip install -r requirements.txt
```
**Wait for installation to complete** (may take a few minutes)

### Step 5: Download NLTK Data (if not already done)
```powershell
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

### Step 6: Test Installation (Optional but Recommended)
```powershell
python test_installation.py
```
**Expected Output**: All tests should show `[OK]` and "SUCCESS All tests passed!"

### Step 7: Initialize Project (Optional but Recommended)
```powershell
python setup.py
```
This will:
- Create sample dataset
- Train ML models
- Set up everything needed

**Wait for completion** - you'll see messages like:
- "Creating directories..."
- "Downloading NLTK data..."
- "Training quiz generator..."
- "Setup complete!"

### Step 8: Start the Web Application
```powershell
python app.py
```

**Expected Output**:
```
Initializing AI Study Pal...
Training quiz generator...
Training resource suggester...
Initialization complete!
 * Running on http://0.0.0.0:5000
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### Step 9: Open Web Browser
- Open your web browser (Chrome, Firefox, Edge, etc.)
- Go to: `http://localhost:5000`
- OR: `http://127.0.0.1:5000`

### Step 10: Use the Application
1. Enter a subject (e.g., "Mathematics", "Science", "History")
2. Enter study hours (e.g., 10)
3. Select a scenario (Exam Preparation, Homework Help, or Regular Study)
4. Optionally paste text for summarization
5. Click "Generate Study Plan"

## Complete Command Sequence (Copy & Paste)

If you want to run everything in sequence:

```powershell
# Navigate to project
cd "E:\AI STUDY PAL"

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

# Test installation
python test_installation.py

# Initialize project (optional)
python setup.py

# Start the app
python app.py
```

## Quick Start (If Already Installed)

If you've already installed everything, just run:

```powershell
cd "E:\AI STUDY PAL"
python app.py
```

Then open `http://localhost:5000` in your browser.

## Troubleshooting

### If "python" command not found:
Try:
```powershell
python3 app.py
```
OR
```powershell
py app.py
```

### If port 5000 is already in use:
The app will show an error. You can:
1. Close the other application using port 5000
2. OR edit `app.py` line 233 and change `port=5000` to `port=5001`

### To Stop the Server:
Press `CTRL + C` in the terminal

### To Run in Background (Advanced):
```powershell
Start-Process python -ArgumentList "app.py" -WindowStyle Hidden
```

## Verification Checklist

Before running the app, verify:
- [x] You're in the project directory: `E:\AI STUDY PAL`
- [x] Dependencies installed: `pip list` shows Flask, pandas, etc.
- [x] NLTK data downloaded: `python test_installation.py` passes
- [x] Models trained (optional): `models/` folder contains `.pkl` files

---

**That's it! Your AI Study Pal should now be running! 🎓**


