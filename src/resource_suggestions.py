"""
Resource Suggestion System
Uses K-means clustering to group topics and suggest resources
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pickle
import os


class ResourceSuggester:
    """Suggests study resources using K-means clustering"""
    
    def __init__(self, model_dir='models'):
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
        self.vectorizer = TfidfVectorizer(max_features=50, stop_words='english')
        self.clusterer = None
        self.is_trained = False
        
    def prepare_clustering_data(self, df):
        """Prepare data for clustering"""
        # Combine subject and topic for better clustering
        texts = (df['subject'] + ' ' + df['topic'] + ' ' + df['text']).tolist()
        X = self.vectorizer.fit_transform(texts).toarray()
        return X
    
    def train_clusterer(self, df, n_clusters=3):
        """Train K-means clusterer"""
        X = self.prepare_clustering_data(df)
        
        # Determine optimal number of clusters
        best_score = -1
        best_n = n_clusters
        
        for n in range(2, min(6, len(df))):
            kmeans = KMeans(n_clusters=n, random_state=42, n_init=10)
            labels = kmeans.fit_predict(X)
            if len(set(labels)) > 1:  # Need at least 2 clusters
                score = silhouette_score(X, labels)
                if score > best_score:
                    best_score = score
                    best_n = n
        
        # Train with best n_clusters
        self.clusterer = KMeans(n_clusters=best_n, random_state=42, n_init=10)
        self.clusterer.fit(X)
        
        # Save model
        model_path = os.path.join(self.model_dir, 'clusterer.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(self.clusterer, f)
        
        vectorizer_path = os.path.join(self.model_dir, 'resource_vectorizer.pkl')
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        
        self.is_trained = True
        
        return {
            'n_clusters': best_n,
            'silhouette_score': best_score
        }
    
    def load_models(self):
        """Load pre-trained models"""
        model_path = os.path.join(self.model_dir, 'clusterer.pkl')
        vectorizer_path = os.path.join(self.model_dir, 'resource_vectorizer.pkl')
        
        if os.path.exists(model_path) and os.path.exists(vectorizer_path):
            with open(model_path, 'rb') as f:
                self.clusterer = pickle.load(f)
            with open(vectorizer_path, 'rb') as f:
                self.vectorizer = pickle.load(f)
            self.is_trained = True
            return True
        return False
    
    def suggest_resources(self, subject, topic=None):
        """Suggest study resources based on subject and topic"""
        # Resource database
        resources_db = {
            'Mathematics': [
                {'name': 'Khan Academy - Math', 'url': 'https://www.khanacademy.org/math', 'type': 'Video Tutorials'},
                {'name': 'Math is Fun', 'url': 'https://www.mathsisfun.com', 'type': 'Interactive Lessons'},
                {'name': 'Wolfram Alpha', 'url': 'https://www.wolframalpha.com', 'type': 'Problem Solver'},
                {'name': 'Brilliant - Math', 'url': 'https://brilliant.org/courses/math', 'type': 'Practice Problems'}
            ],
            'Science': [
                {'name': 'Khan Academy - Science', 'url': 'https://www.khanacademy.org/science', 'type': 'Video Tutorials'},
                {'name': 'National Geographic', 'url': 'https://www.nationalgeographic.com', 'type': 'Educational Content'},
                {'name': 'Science Daily', 'url': 'https://www.sciencedaily.com', 'type': 'News & Articles'},
                {'name': 'NASA Education', 'url': 'https://www.nasa.gov/education', 'type': 'Educational Resources'}
            ],
            'History': [
                {'name': 'History.com', 'url': 'https://www.history.com', 'type': 'Articles & Videos'},
                {'name': 'BBC History', 'url': 'https://www.bbc.co.uk/history', 'type': 'Educational Content'},
                {'name': 'National Archives', 'url': 'https://www.archives.gov/education', 'type': 'Primary Sources'},
                {'name': 'Crash Course History', 'url': 'https://www.youtube.com/crashcourse', 'type': 'Video Series'}
            ],
            'default': [
                {'name': 'Coursera', 'url': 'https://www.coursera.org', 'type': 'Online Courses'},
                {'name': 'edX', 'url': 'https://www.edx.org', 'type': 'Online Courses'},
                {'name': 'YouTube Education', 'url': 'https://www.youtube.com/education', 'type': 'Video Tutorials'},
                {'name': 'Wikipedia', 'url': 'https://www.wikipedia.org', 'type': 'Reference'}
            ]
        }
        
        # Get resources for subject
        if subject in resources_db:
            resources = resources_db[subject]
        else:
            resources = resources_db['default']
        
        # Return top 3-4 resources
        return resources[:4]
    
    def get_cluster_resources(self, text):
        """Get resources based on text clustering"""
        if not self.is_trained:
            return self.suggest_resources('default')
        
        # Transform text and predict cluster
        X = self.vectorizer.transform([text.lower()]).toarray()
        cluster = self.clusterer.predict(X)[0]
        
        # Map cluster to subject (simplified)
        # In a real implementation, you'd maintain a mapping
        return self.suggest_resources('default')


