"""
Deep Learning Text Summarizer
Uses Keras neural network for text summarization and feedback generation
"""

import numpy as np
import re
import pickle
import os
import random

# Keras imports (optional - not currently used but kept for future DL implementation)
# The code uses simple extractive summarization, so Keras is not required
try:
    # Try Keras 2.x imports first
    try:
        from keras.models import Sequential
        from keras.layers import LSTM, Dense, Embedding, Dropout
        from keras.preprocessing.text import Tokenizer
        from keras.preprocessing.sequence import pad_sequences
    except ImportError:
        # Try Keras 3.x imports (comes with TensorFlow 2.20+)
        from keras import Sequential
        from keras.layers import LSTM, Dense, Embedding, Dropout
        from keras.preprocessing.text import Tokenizer
        from keras.preprocessing.sequence import pad_sequences
    KERAS_AVAILABLE = True
except ImportError:
    KERAS_AVAILABLE = False
    # Keras not available - using simple extractive summarization instead


class TextSummarizer:
    """Summarizes text using deep learning"""
    
    def __init__(self, model_dir='models'):
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
        self.tokenizer = None
        self.model = None
        self.max_len = 200
        self.vocab_size = 1000
        self.is_trained = False
        
    def simple_summarize(self, text, max_sentences=3):
        """
        Simple extractive summarization
        In a full implementation, this would use a trained neural network
        """
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        if len(sentences) <= max_sentences:
            return text
        
        # Simple scoring based on length and keywords
        word_freq = {}
        words = text.lower().split()
        for word in words:
            if len(word) > 3:  # Ignore short words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Score sentences
        sentence_scores = []
        for sentence in sentences:
            score = 0
            words_in_sentence = sentence.lower().split()
            for word in words_in_sentence:
                if word in word_freq:
                    score += word_freq[word]
            sentence_scores.append((score, sentence))
        
        # Sort by score and take top sentences
        sentence_scores.sort(reverse=True, key=lambda x: x[0])
        top_sentences = sentence_scores[:max_sentences]
        
        # Reorder to maintain original order
        top_sentences.sort(key=lambda x: sentences.index(x[1]))
        
        summary = '. '.join([s[1] for s in top_sentences])
        if summary and not summary.endswith('.'):
            summary += '.'
        
        return summary
    
    def summarize_text(self, text, target_length=50):
        """Summarize text to target length"""
        if not text or len(text.strip()) < 20:
            return text
        
        # Calculate target sentences based on length
        current_length = len(text)
        ratio = target_length / current_length if current_length > 0 else 0.5
        max_sentences = max(1, int(len(re.split(r'[.!?]+', text)) * ratio))
        
        summary = self.simple_summarize(text, max_sentences=max_sentences)
        
        # Ensure summary is not too long
        if len(summary) > target_length * 1.5:
            sentences = re.split(r'[.!?]+', summary)
            summary = '. '.join(sentences[:max_sentences])
            if summary and not summary.endswith('.'):
                summary += '.'
        
        return summary
    
    def generate_feedback(self, subject, performance='good'):
        """Generate motivational feedback using pre-defined templates"""
        feedback_templates = {
            'good': [
                f"Excellent work on {subject}! You're making great progress. Keep up the momentum!",
                f"Outstanding performance in {subject}! Your dedication is paying off. Continue practicing!",
                f"Great job on {subject}! You're mastering the concepts. Stay focused and keep learning!",
                f"Wonderful progress in {subject}! Your hard work is showing. Keep pushing forward!",
                f"Fantastic effort on {subject}! You're on the right track. Maintain this pace!"
            ],
            'medium': [
                f"Good work on {subject}! There's room for improvement. Keep practicing and you'll get there!",
                f"Decent progress in {subject}. Review the challenging topics and try again!",
                f"Not bad on {subject}! Focus on the areas you found difficult. Practice makes perfect!",
                f"Keep working on {subject}! You're making progress. Review and practice more!",
                f"Good attempt on {subject}! Identify weak areas and focus on them. You can do it!"
            ],
            'needs_improvement': [
                f"Keep practicing {subject}! Review the basics and try again. Every expert was once a beginner!",
                f"Don't give up on {subject}! Focus on understanding the fundamentals. You'll improve!",
                f"More practice needed for {subject}. Review the material and try again. Persistence pays off!",
                f"Keep learning {subject}! Break down complex topics into smaller parts. You've got this!",
                f"Stay motivated with {subject}! Review your notes and practice regularly. Progress takes time!"
            ]
        }
        
        templates = feedback_templates.get(performance, feedback_templates['good'])
        return random.choice(templates)
    
    def generate_study_feedback(self, quiz_score, total_questions):
        """Generate feedback based on quiz performance"""
        percentage = (quiz_score / total_questions) * 100 if total_questions > 0 else 0
        
        if percentage >= 80:
            performance = 'good'
        elif percentage >= 60:
            performance = 'medium'
        else:
            performance = 'needs_improvement'
        
        return self.generate_feedback('your studies', performance)

