"""
NLP Study Tips Generator
Uses NLTK for tokenization and keyword extraction to generate study tips
"""

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
import re
import os

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)


class StudyTipsGenerator:
    """Generates study tips using NLP techniques"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        
    def extract_keywords(self, text, top_n=10):
        """Extract top keywords from text"""
        if not text:
            return []
        
        # Tokenize
        tokens = word_tokenize(text.lower())
        
        # Remove stopwords and non-alphabetic tokens
        keywords = [
            self.lemmatizer.lemmatize(token)
            for token in tokens
            if token.isalpha() and token not in self.stop_words and len(token) > 2
        ]
        
        # Count frequency
        keyword_counts = Counter(keywords)
        
        # Return top N keywords
        top_keywords = [word for word, count in keyword_counts.most_common(top_n)]
        return top_keywords
    
    def generate_tips_from_text(self, text, subject=None):
        """Generate study tips based on text analysis"""
        if not text or len(text.strip()) < 20:
            return self.generate_generic_tips(subject)
        
        keywords = self.extract_keywords(text, top_n=5)
        
        tips = []
        
        # Tip 1: Review key terms
        if keywords:
            key_terms = ', '.join(keywords[:3])
            tips.append(f"Review key terms regularly: {key_terms}. Understanding these concepts is crucial.")
        
        # Tip 2: Active recall
        tips.append("Practice active recall by testing yourself on the material without looking at your notes.")
        
        # Tip 3: Spaced repetition
        tips.append("Use spaced repetition: review the material multiple times over increasing intervals.")
        
        # Tip 4: Summarize
        tips.append("Create your own summaries of the material. Writing helps reinforce learning.")
        
        # Tip 5: Practice problems
        if subject:
            tips.append(f"Solve practice problems related to {subject}. Application reinforces understanding.")
        else:
            tips.append("Solve practice problems regularly. Application reinforces understanding.")
        
        # Tip 6: Break down complex topics
        if len(keywords) > 3:
            tips.append("Break down complex topics into smaller, manageable chunks. Master one concept at a time.")
        
        # Tip 7: Regular review
        tips.append("Schedule regular review sessions. Consistency is key to long-term retention.")
        
        return tips[:5]  # Return top 5 tips
    
    def generate_generic_tips(self, subject=None):
        """Generate generic study tips"""
        tips = [
            "Create a study schedule and stick to it. Consistency is important for effective learning.",
            "Take breaks during study sessions. The Pomodoro technique (25 min study, 5 min break) works well.",
            "Use active learning techniques: summarize, question, and explain concepts in your own words.",
            "Review your notes regularly. Spaced repetition helps with long-term memory retention.",
            "Practice problems and quizzes. Testing yourself improves recall and identifies weak areas."
        ]
        
        if subject:
            tips.insert(0, f"Focus on understanding {subject} fundamentals before moving to advanced topics.")
        
        return tips
    
    def generate_subject_specific_tips(self, subject):
        """Generate subject-specific study tips"""
        subject_tips = {
            'Mathematics': [
                "Practice solving problems daily. Math requires consistent practice.",
                "Understand the concepts before memorizing formulas. Know why, not just how.",
                "Work through examples step by step. Don't skip steps in problem-solving.",
                "Review mistakes carefully. Learn from errors to avoid repeating them.",
                "Use visual aids like graphs and diagrams to understand abstract concepts."
            ],
            'Science': [
                "Understand the scientific method and how it applies to different topics.",
                "Connect concepts to real-world examples. Science is everywhere!",
                "Use diagrams and models to visualize complex processes.",
                "Review key terminology regularly. Scientific vocabulary is important.",
                "Perform experiments or watch demonstrations when possible."
            ],
            'History': [
                "Create timelines to understand chronological relationships.",
                "Focus on cause and effect relationships between events.",
                "Connect historical events to current events for better context.",
                "Use mnemonic devices to remember dates and names.",
                "Read primary sources when possible to understand perspectives."
            ],
            'default': [
                "Break down large topics into smaller sections.",
                "Use multiple study methods: reading, writing, speaking, and listening.",
                "Teach the material to someone else. Teaching reinforces learning.",
                "Create mind maps or concept maps to visualize relationships.",
                "Stay organized with notes and study materials."
            ]
        }
        
        return subject_tips.get(subject, subject_tips['default'])
    
    def generate_comprehensive_tips(self, text=None, subject=None):
        """Generate comprehensive study tips combining all methods"""
        all_tips = []
        
        # Add subject-specific tips
        if subject:
            all_tips.extend(self.generate_subject_specific_tips(subject))
        
        # Add text-based tips
        if text:
            all_tips.extend(self.generate_tips_from_text(text, subject))
        else:
            all_tips.extend(self.generate_generic_tips(subject))
        
        # Remove duplicates while preserving order
        seen = set()
        unique_tips = []
        for tip in all_tips:
            if tip not in seen:
                seen.add(tip)
                unique_tips.append(tip)
        
        return unique_tips[:7]  # Return top 7 unique tips


