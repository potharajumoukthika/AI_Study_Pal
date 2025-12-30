"""
Data Processing Module
Handles data collection, cleaning, and EDA visualizations
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import json
import os
from collections import Counter


class DataProcessor:
    """Handles data collection, cleaning, and visualization"""
    
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.educational_texts_path = os.path.join(data_dir, 'educational_texts.csv')
        self.user_inputs_path = os.path.join(data_dir, 'user_inputs.json')
        
    def create_sample_dataset(self):
        """Create sample educational texts dataset"""
        sample_texts = [
            {
                'subject': 'Mathematics',
                'topic': 'Algebra',
                'text': 'Algebra is a branch of mathematics that uses symbols and letters to represent numbers and quantities in formulas and equations. It helps solve problems involving unknown values.',
                'difficulty': 'medium'
            },
            {
                'subject': 'Mathematics',
                'topic': 'Geometry',
                'text': 'Geometry is the study of shapes, sizes, and properties of space. It includes concepts like points, lines, angles, and polygons.',
                'difficulty': 'easy'
            },
            {
                'subject': 'Science',
                'topic': 'Physics',
                'text': 'Physics is the natural science that studies matter, motion, and behavior through space and time. It includes mechanics, thermodynamics, and electromagnetism.',
                'difficulty': 'medium'
            },
            {
                'subject': 'Science',
                'topic': 'Chemistry',
                'text': 'Chemistry studies the composition, structure, and properties of matter. It involves atoms, molecules, and chemical reactions.',
                'difficulty': 'medium'
            },
            {
                'subject': 'Science',
                'topic': 'Biology',
                'text': 'Biology is the study of living organisms and their interactions. It covers cells, genetics, evolution, and ecosystems.',
                'difficulty': 'easy'
            },
            {
                'subject': 'History',
                'topic': 'World History',
                'text': 'World history covers major events and civilizations from ancient times to modern era. It includes wars, revolutions, and cultural developments.',
                'difficulty': 'easy'
            },
            {
                'subject': 'Mathematics',
                'topic': 'Calculus',
                'text': 'Calculus is the mathematical study of continuous change. It includes differential and integral calculus for analyzing functions and rates.',
                'difficulty': 'hard'
            },
            {
                'subject': 'Science',
                'topic': 'Astronomy',
                'text': 'Astronomy studies celestial objects and phenomena. It explores planets, stars, galaxies, and the universe.',
                'difficulty': 'medium'
            },
            {
                'subject': 'Mathematics',
                'topic': 'Statistics',
                'text': 'Statistics involves collecting, analyzing, and interpreting data. It includes probability, distributions, and hypothesis testing.',
                'difficulty': 'medium'
            },
            {
                'subject': 'Science',
                'topic': 'Earth Science',
                'text': 'Earth science studies the planet Earth including geology, meteorology, and oceanography. It examines natural processes and systems.',
                'difficulty': 'easy'
            }
        ]
        
        df = pd.DataFrame(sample_texts)
        df.to_csv(self.educational_texts_path, index=False)
        return df
    
    def load_educational_texts(self):
        """Load educational texts dataset"""
        if not os.path.exists(self.educational_texts_path):
            return self.create_sample_dataset()
        return pd.read_csv(self.educational_texts_path)
    
    def clean_text_data(self, df):
        """Clean text data: remove duplicates, lowercase, remove extra spaces"""
        # Remove duplicates
        df_clean = df.drop_duplicates(subset=['text'], keep='first')
        
        # Lowercase text
        df_clean['text'] = df_clean['text'].str.lower()
        
        # Remove extra spaces
        df_clean['text'] = df_clean['text'].str.strip()
        df_clean['text'] = df_clean['text'].str.replace(r'\s+', ' ', regex=True)
        
        return df_clean
    
    def save_user_input(self, subject, hours, scenario, text=None):
        """Save user input to JSON file"""
        user_input = {
            'subject': subject,
            'hours': hours,
            'scenario': scenario,
            'text': text if text else '',
            'timestamp': pd.Timestamp.now().isoformat()
        }
        
        # Load existing inputs
        if os.path.exists(self.user_inputs_path):
            with open(self.user_inputs_path, 'r') as f:
                inputs = json.load(f)
        else:
            inputs = []
        
        inputs.append(user_input)
        
        # Save updated inputs
        with open(self.user_inputs_path, 'w') as f:
            json.dump(inputs, f, indent=2)
        
        return user_input
    
    def perform_eda(self, df, output_dir='data'):
        """Perform exploratory data analysis and create visualizations"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Subject distribution pie chart
        subject_counts = df['subject'].value_counts()
        plt.figure(figsize=(8, 6))
        plt.pie(subject_counts.values, labels=subject_counts.index, autopct='%1.1f%%', startangle=90)
        plt.title('Subject Distribution')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'subject_distribution.png'))
        plt.close()
        
        # Difficulty distribution bar chart
        difficulty_counts = df['difficulty'].value_counts()
        plt.figure(figsize=(8, 6))
        plt.bar(difficulty_counts.index, difficulty_counts.values, color=['green', 'orange', 'red'])
        plt.xlabel('Difficulty Level')
        plt.ylabel('Count')
        plt.title('Difficulty Distribution')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'difficulty_distribution.png'))
        plt.close()
        
        # Text length distribution
        df['text_length'] = df['text'].str.len()
        plt.figure(figsize=(8, 6))
        plt.hist(df['text_length'], bins=20, edgecolor='black')
        plt.xlabel('Text Length (characters)')
        plt.ylabel('Frequency')
        plt.title('Text Length Distribution')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'text_length_distribution.png'))
        plt.close()
        
        # Summary statistics
        summary = {
            'total_texts': len(df),
            'subjects': df['subject'].nunique(),
            'topics': df['topic'].nunique(),
            'avg_text_length': df['text_length'].mean(),
            'subject_counts': subject_counts.to_dict(),
            'difficulty_counts': difficulty_counts.to_dict()
        }
        
        return summary


