"""
Machine Learning Quiz Generator
Uses Logistic Regression for difficulty classification and generates quizzes
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.cluster import KMeans
import pickle
import os
import random


class QuizGenerator:
    """Generates quizzes using ML models"""
    
    def __init__(self, model_dir='models'):
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
        self.vectorizer = CountVectorizer(max_features=100, stop_words='english')
        self.difficulty_model = None
        self.topic_clusterer = None
        self.is_trained = False
        
    def prepare_training_data(self, df):
        """Prepare data for training"""
        # Create features from text
        X = self.vectorizer.fit_transform(df['text']).toarray()
        
        # Map difficulty to binary (easy=0, medium/hard=1)
        y = df['difficulty'].map({'easy': 0, 'medium': 1, 'hard': 1})
        
        return X, y
    
    def train_difficulty_classifier(self, df):
        """Train logistic regression model for difficulty classification"""
        X, y = self.prepare_training_data(df)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.difficulty_model = LogisticRegression(
            max_iter=1000,
            random_state=42,
            C=1.0
        )
        self.difficulty_model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.difficulty_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        # Save model
        model_path = os.path.join(self.model_dir, 'difficulty_model.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(self.difficulty_model, f)
        
        vectorizer_path = os.path.join(self.model_dir, 'vectorizer.pkl')
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        
        self.is_trained = True
        
        return {
            'accuracy': accuracy,
            'f1_score': f1,
            'classification_report': classification_report(y_test, y_pred)
        }
    
    def load_models(self):
        """Load pre-trained models"""
        model_path = os.path.join(self.model_dir, 'difficulty_model.pkl')
        vectorizer_path = os.path.join(self.model_dir, 'vectorizer.pkl')
        
        if os.path.exists(model_path) and os.path.exists(vectorizer_path):
            with open(model_path, 'rb') as f:
                self.difficulty_model = pickle.load(f)
            with open(vectorizer_path, 'rb') as f:
                self.vectorizer = pickle.load(f)
            self.is_trained = True
            return True
        return False
    
    def generate_quiz(self, subject, num_questions=5):
        """Generate quiz questions for a subject with randomization"""
        questions = []
        
        # Expanded question bank with many more questions per subject
        question_bank = {
            'Mathematics': [
                {'question': 'What is the value of x in the equation 2x + 5 = 15?', 'options': ['5', '10', '7', '8'], 'correct': 0},
                {'question': 'What is the area of a circle with radius 5?', 'options': ['25π', '10π', '5π', '15π'], 'correct': 0},
                {'question': 'What is the derivative of x²?', 'options': ['x', '2x', 'x²', '2x²'], 'correct': 1},
                {'question': 'What is 15% of 200?', 'options': ['30', '25', '35', '40'], 'correct': 0},
                {'question': 'What is the square root of 64?', 'options': ['6', '7', '8', '9'], 'correct': 2},
                {'question': 'Solve: 3x - 7 = 14', 'options': ['x = 5', 'x = 7', 'x = 9', 'x = 11'], 'correct': 1},
                {'question': 'What is the perimeter of a rectangle with length 8 and width 5?', 'options': ['26', '40', '13', '20'], 'correct': 0},
                {'question': 'What is 2³ × 2²?', 'options': ['2⁵', '2⁶', '4⁵', '8²'], 'correct': 0},
                {'question': 'What is the sum of angles in a triangle?', 'options': ['90°', '180°', '270°', '360°'], 'correct': 1},
                {'question': 'What is the value of sin(90°)?', 'options': ['0', '0.5', '1', '√2/2'], 'correct': 2},
                {'question': 'What is the formula for the volume of a cylinder?', 'options': ['πr²h', '2πr', 'πr²', '4/3πr³'], 'correct': 0},
                {'question': 'What is the slope of the line y = 3x + 2?', 'options': ['2', '3', '5', '6'], 'correct': 1},
                {'question': 'What is the value of log₁₀(100)?', 'options': ['1', '2', '10', '100'], 'correct': 1},
                {'question': 'What is the integral of 2x?', 'options': ['x²', '2x²', 'x² + C', '2x + C'], 'correct': 2},
                {'question': 'What is the median of [3, 5, 7, 9, 11]?', 'options': ['5', '7', '9', '6'], 'correct': 1},
            ],
            'Science': [
                {'question': 'What is the chemical symbol for water?', 'options': ['H2O', 'CO2', 'O2', 'NaCl'], 'correct': 0},
                {'question': 'What is the speed of light?', 'options': ['300,000 km/s', '150,000 km/s', '450,000 km/s', '200,000 km/s'], 'correct': 0},
                {'question': 'What is the largest planet in our solar system?', 'options': ['Earth', 'Jupiter', 'Saturn', 'Neptune'], 'correct': 1},
                {'question': 'What process do plants use to make food?', 'options': ['Respiration', 'Photosynthesis', 'Digestion', 'Circulation'], 'correct': 1},
                {'question': 'What is the smallest unit of matter?', 'options': ['Molecule', 'Atom', 'Cell', 'Electron'], 'correct': 1},
                {'question': 'What is the pH of pure water?', 'options': ['5', '6', '7', '8'], 'correct': 2},
                {'question': 'Which gas makes up most of Earth\'s atmosphere?', 'options': ['Oxygen', 'Nitrogen', 'Carbon Dioxide', 'Argon'], 'correct': 1},
                {'question': 'What is the force that pulls objects toward Earth?', 'options': ['Magnetism', 'Gravity', 'Friction', 'Inertia'], 'correct': 1},
                {'question': 'What is the hardest natural substance?', 'options': ['Gold', 'Diamond', 'Iron', 'Platinum'], 'correct': 1},
                {'question': 'What type of energy does the Sun produce?', 'options': ['Chemical', 'Nuclear', 'Electrical', 'Mechanical'], 'correct': 1},
                {'question': 'What is the chemical symbol for gold?', 'options': ['Go', 'Gd', 'Au', 'Ag'], 'correct': 2},
                {'question': 'How many bones are in an adult human body?', 'options': ['196', '206', '216', '226'], 'correct': 1},
                {'question': 'What is the closest star to Earth?', 'options': ['Alpha Centauri', 'The Sun', 'Sirius', 'Betelgeuse'], 'correct': 1},
                {'question': 'What is the process of cell division called?', 'options': ['Mitosis', 'Meiosis', 'Photosynthesis', 'Respiration'], 'correct': 0},
                {'question': 'What is the unit of electric current?', 'options': ['Volt', 'Ampere', 'Watt', 'Ohm'], 'correct': 1},
            ],
            'History': [
                {'question': 'In which year did World War II end?', 'options': ['1944', '1945', '1946', '1947'], 'correct': 1},
                {'question': 'Who wrote the Declaration of Independence?', 'options': ['George Washington', 'Thomas Jefferson', 'Benjamin Franklin', 'John Adams'], 'correct': 1},
                {'question': 'What was the main cause of the American Civil War?', 'options': ['Taxation', 'Slavery', 'Trade', 'Territory'], 'correct': 1},
                {'question': 'Which empire was ruled by Julius Caesar?', 'options': ['Greek', 'Roman', 'Egyptian', 'Persian'], 'correct': 1},
                {'question': 'When did the French Revolution begin?', 'options': ['1787', '1789', '1791', '1793'], 'correct': 1},
                {'question': 'Who was the first President of the United States?', 'options': ['Thomas Jefferson', 'George Washington', 'John Adams', 'Benjamin Franklin'], 'correct': 1},
                {'question': 'In which year did World War I begin?', 'options': ['1912', '1914', '1916', '1918'], 'correct': 1},
                {'question': 'Which ancient civilization built the pyramids?', 'options': ['Greeks', 'Romans', 'Egyptians', 'Mayans'], 'correct': 2},
                {'question': 'When did the Berlin Wall fall?', 'options': ['1987', '1989', '1991', '1993'], 'correct': 1},
                {'question': 'Who painted the Mona Lisa?', 'options': ['Michelangelo', 'Leonardo da Vinci', 'Picasso', 'Van Gogh'], 'correct': 1},
                {'question': 'Which war was fought between 1950-1953?', 'options': ['Vietnam War', 'Korean War', 'World War II', 'Cold War'], 'correct': 1},
                {'question': 'Who was known as the Iron Lady?', 'options': ['Indira Gandhi', 'Margaret Thatcher', 'Angela Merkel', 'Golda Meir'], 'correct': 1},
                {'question': 'When did the Renaissance period begin?', 'options': ['1300s', '1400s', '1500s', '1600s'], 'correct': 1},
                {'question': 'Which country was the first to land on the moon?', 'options': ['Soviet Union', 'United States', 'China', 'Japan'], 'correct': 1},
                {'question': 'Who was the leader of the Soviet Union during WWII?', 'options': ['Lenin', 'Stalin', 'Khrushchev', 'Gorbachev'], 'correct': 1},
            ],
            'English': [
                {'question': 'What is a group of words that expresses a complete thought?', 'options': ['Phrase', 'Sentence', 'Clause', 'Paragraph'], 'correct': 1},
                {'question': 'Which of these is a proper noun?', 'options': ['city', 'London', 'beautiful', 'quickly'], 'correct': 1},
                {'question': 'What is the past tense of "go"?', 'options': ['goed', 'went', 'gone', 'going'], 'correct': 1},
                {'question': 'What figure of speech compares two things using "like" or "as"?', 'options': ['Metaphor', 'Simile', 'Personification', 'Alliteration'], 'correct': 1},
                {'question': 'Who wrote "Romeo and Juliet"?', 'options': ['Charles Dickens', 'William Shakespeare', 'Jane Austen', 'Mark Twain'], 'correct': 1},
                {'question': 'What is the main character in a story called?', 'options': ['Antagonist', 'Protagonist', 'Narrator', 'Author'], 'correct': 1},
                {'question': 'What type of word describes a noun?', 'options': ['Verb', 'Adjective', 'Adverb', 'Pronoun'], 'correct': 1},
                {'question': 'What is a word that sounds like what it means?', 'options': ['Onomatopoeia', 'Alliteration', 'Metaphor', 'Simile'], 'correct': 0},
                {'question': 'How many syllables are in "beautiful"?', 'options': ['2', '3', '4', '5'], 'correct': 1},
                {'question': 'What is the plural of "child"?', 'options': ['childs', 'children', 'childes', 'childrens'], 'correct': 1},
                {'question': 'Which punctuation mark shows strong emotion?', 'options': ['Period', 'Comma', 'Exclamation mark', 'Question mark'], 'correct': 2},
                {'question': 'What is the opposite of "synonym"?', 'options': ['Homonym', 'Antonym', 'Acronym', 'Pseudonym'], 'correct': 1},
                {'question': 'Who wrote "1984"?', 'options': ['George Orwell', 'Aldous Huxley', 'Ray Bradbury', 'J.D. Salinger'], 'correct': 0},
                {'question': 'What is the study of word origins called?', 'options': ['Syntax', 'Etymology', 'Semantics', 'Phonetics'], 'correct': 1},
                {'question': 'What is a group of lines in a poem called?', 'options': ['Paragraph', 'Stanza', 'Verse', 'Chapter'], 'correct': 1},
            ],
            'Physics': [
                {'question': 'What is the unit of force?', 'options': ['Joule', 'Newton', 'Watt', 'Pascal'], 'correct': 1},
                {'question': 'What is the speed of light in vacuum?', 'options': ['3 × 10⁸ m/s', '3 × 10⁶ m/s', '3 × 10¹⁰ m/s', '3 × 10⁴ m/s'], 'correct': 0},
                {'question': 'What is Newton\'s first law also known as?', 'options': ['Law of Inertia', 'Law of Acceleration', 'Law of Action-Reaction', 'Law of Gravity'], 'correct': 0},
                {'question': 'What type of energy is stored in a battery?', 'options': ['Kinetic', 'Potential', 'Chemical', 'Thermal'], 'correct': 2},
                {'question': 'What is the acceleration due to gravity on Earth?', 'options': ['9.8 m/s²', '10 m/s²', '8.9 m/s²', '11 m/s²'], 'correct': 0},
                {'question': 'What happens to light when it passes through a prism?', 'options': ['Reflection', 'Refraction', 'Diffraction', 'Dispersion'], 'correct': 3},
                {'question': 'What is the formula for kinetic energy?', 'options': ['mgh', '½mv²', 'Fd', 'PV'], 'correct': 1},
                {'question': 'What is the unit of electric charge?', 'options': ['Volt', 'Ampere', 'Coulomb', 'Ohm'], 'correct': 2},
                {'question': 'What type of wave requires a medium to travel?', 'options': ['Electromagnetic', 'Sound', 'Light', 'Radio'], 'correct': 1},
                {'question': 'What is the resistance of a superconductor?', 'options': ['High', 'Medium', 'Zero', 'Infinite'], 'correct': 2},
            ],
            'Chemistry': [
                {'question': 'What is the atomic number of carbon?', 'options': ['4', '6', '8', '12'], 'correct': 1},
                {'question': 'What is the most abundant gas in Earth\'s atmosphere?', 'options': ['Oxygen', 'Nitrogen', 'Carbon Dioxide', 'Argon'], 'correct': 1},
                {'question': 'What is the pH of an acid?', 'options': ['Less than 7', 'Equal to 7', 'Greater than 7', 'Equal to 14'], 'correct': 0},
                {'question': 'What is the chemical symbol for sodium?', 'options': ['So', 'Sd', 'Na', 'Sa'], 'correct': 2},
                {'question': 'What type of bond shares electrons?', 'options': ['Ionic', 'Covalent', 'Metallic', 'Hydrogen'], 'correct': 1},
                {'question': 'What is the process of a solid turning directly into gas?', 'options': ['Melting', 'Sublimation', 'Evaporation', 'Condensation'], 'correct': 1},
                {'question': 'What is Avogadro\'s number?', 'options': ['6.02 × 10²³', '6.02 × 10²²', '6.02 × 10²⁴', '6.02 × 10²¹'], 'correct': 0},
                {'question': 'What is the lightest element?', 'options': ['Helium', 'Hydrogen', 'Lithium', 'Carbon'], 'correct': 1},
                {'question': 'What is the formula for water?', 'options': ['H2O', 'CO2', 'NaCl', 'O2'], 'correct': 0},
                {'question': 'What is a substance that speeds up a reaction?', 'options': ['Inhibitor', 'Catalyst', 'Reactant', 'Product'], 'correct': 1},
            ],
            'Biology': [
                {'question': 'What is the basic unit of life?', 'options': ['Atom', 'Cell', 'Molecule', 'Organ'], 'correct': 1},
                {'question': 'What process do plants use to make food?', 'options': ['Respiration', 'Photosynthesis', 'Digestion', 'Circulation'], 'correct': 1},
                {'question': 'How many chambers does a human heart have?', 'options': ['2', '3', '4', '5'], 'correct': 2},
                {'question': 'What is the powerhouse of the cell?', 'options': ['Nucleus', 'Mitochondria', 'Ribosome', 'Golgi'], 'correct': 1},
                {'question': 'What is the study of heredity called?', 'options': ['Ecology', 'Genetics', 'Anatomy', 'Physiology'], 'correct': 1},
                {'question': 'What is the largest organ in the human body?', 'options': ['Liver', 'Lungs', 'Skin', 'Intestines'], 'correct': 2},
                {'question': 'What type of blood cell fights infection?', 'options': ['Red blood cell', 'White blood cell', 'Platelet', 'Plasma'], 'correct': 1},
                {'question': 'What is DNA short for?', 'options': ['Deoxyribonucleic Acid', 'Ribonucleic Acid', 'Deoxyribose Acid', 'Nucleic Acid'], 'correct': 0},
                {'question': 'What is the process of cell division?', 'options': ['Mitosis', 'Meiosis', 'Photosynthesis', 'Respiration'], 'correct': 0},
                {'question': 'How many bones are in an adult human body?', 'options': ['196', '206', '216', '226'], 'correct': 1},
            ]
        }
        
        # Normalize subject name (case-insensitive matching)
        subject_lower = subject.lower()
        matched_subject = None
        
        # Match subject to question bank
        for key in question_bank.keys():
            if key.lower() == subject_lower or subject_lower in key.lower() or key.lower() in subject_lower:
                matched_subject = key
                break
        
        # Also check for common variations
        subject_variations = {
            'math': 'Mathematics',
            'maths': 'Mathematics',
            'chem': 'Chemistry',
            'bio': 'Biology',
            'phys': 'Physics',
            'hist': 'History',
            'eng': 'English',
            'sci': 'Science'
        }
        
        if not matched_subject and subject_lower in subject_variations:
            matched_subject = subject_variations[subject_lower]
        
        # Get questions for matched subject or use Mathematics as default
        if matched_subject and matched_subject in question_bank:
            available_questions = question_bank[matched_subject].copy()
        else:
            available_questions = question_bank['Mathematics'].copy()
        
        # Shuffle and select random questions
        random.shuffle(available_questions)
        selected = available_questions[:min(num_questions, len(available_questions))]
        
        # Shuffle options for each question to make it more random
        for q in selected:
            # Store correct answer
            correct_answer = q['options'][q['correct']]
            # Shuffle options
            random.shuffle(q['options'])
            # Find new position of correct answer
            q['correct'] = q['options'].index(correct_answer)
            
            # Classify difficulty if model is trained
            if self.is_trained:
                text_rep = q['question'].lower()
                try:
                    X = self.vectorizer.transform([text_rep]).toarray()
                    difficulty_pred = self.difficulty_model.predict(X)[0]
                    q['difficulty'] = 'easy' if difficulty_pred == 0 else 'medium'
                except:
                    q['difficulty'] = random.choice(['easy', 'medium'])
            else:
                q['difficulty'] = random.choice(['easy', 'medium'])
            
            questions.append(q)
        
        return questions
    
    def classify_difficulty(self, text):
        """Classify text difficulty using trained model"""
        if not self.is_trained:
            return 'medium'  # Default
        
        X = self.vectorizer.transform([text.lower()]).toarray()
        prediction = self.difficulty_model.predict(X)[0]
        return 'easy' if prediction == 0 else 'medium'


