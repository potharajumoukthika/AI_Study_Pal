"""
AI Study Pal - Flask Web Application
Main application file integrating all components
"""

from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import os
from datetime import datetime, timedelta
import io
import csv
import random

from src.data_processing import DataProcessor
from src.ml_quiz_generator import QuizGenerator
from src.dl_summarizer import TextSummarizer
from src.nlp_tips import StudyTipsGenerator
from src.resource_suggestions import ResourceSuggester

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ai-study-pal-secret-key'

# Initialize components
data_processor = DataProcessor()
quiz_generator = QuizGenerator()
summarizer = TextSummarizer()
tips_generator = StudyTipsGenerator()
resource_suggester = ResourceSuggester()

# Initialize models on startup
def initialize_models():
    """Initialize and train models if needed"""
    print("Initializing AI Study Pal...")
    
    # Load or create dataset
    df = data_processor.load_educational_texts()
    df_clean = data_processor.clean_text_data(df)
    
    # Train or load ML models
    if not quiz_generator.load_models():
        print("Training quiz generator...")
        quiz_generator.train_difficulty_classifier(df_clean)
    
    # Train or load resource suggester
    if not resource_suggester.load_models():
        print("Training resource suggester...")
        resource_suggester.train_clusterer(df_clean)
    
    print("Initialization complete!")

# Initialize on startup
initialize_models()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_study_plan():
    """Generate study plan and all features"""
    try:
        # Get user inputs
        subject = request.form.get('subject', '').strip()
        hours = float(request.form.get('hours', 0))
        scenario = request.form.get('scenario', 'exam_prep')
        user_text = request.form.get('text', '').strip()
        
        if not subject or hours <= 0:
            return jsonify({'error': 'Please provide valid subject and study hours'}), 400
        
        # Save user input
        data_processor.save_user_input(subject, hours, scenario, user_text)
        
        # Generate study plan
        study_plan = generate_study_schedule(subject, hours, scenario)
        
        # Generate quiz
        quiz = quiz_generator.generate_quiz(subject, num_questions=5)
        
        # Generate summary if text provided
        summary = None
        if user_text:
            summary = summarizer.summarize_text(user_text, target_length=50)
        
        # Generate study tips
        tips = tips_generator.generate_comprehensive_tips(user_text, subject)
        
        # Get resource suggestions
        resources = resource_suggester.suggest_resources(subject)
        
        # Generate feedback
        feedback = summarizer.generate_feedback(subject, 'good')
        
        return jsonify({
            'success': True,
            'study_plan': study_plan,
            'quiz': quiz,
            'summary': summary,
            'tips': tips,
            'resources': resources,
            'feedback': feedback,
            'subject': subject,
            'hours': hours
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_study_schedule(subject, total_hours, scenario):
    """Generate a study schedule"""
    schedule = []
    
    # Determine study sessions based on scenario
    if scenario == 'exam_prep':
        days = 7  # 1 week
        sessions_per_day = 2
    elif scenario == 'homework':
        days = 3  # 3 days
        sessions_per_day = 1
    elif scenario == 'regular_study':
        days = 5  # 5 days
        sessions_per_day = 1
    else:
        days = 5
        sessions_per_day = 1
    
    total_sessions = days * sessions_per_day
    hours_per_session = total_hours / total_sessions if total_sessions > 0 else total_hours
    
    # Study topics based on subject (shuffled for variety)
    topics = get_study_topics(subject)
    random.shuffle(topics)  # Shuffle topics for random order
    
    current_date = datetime.now()
    session_num = 0
    
    for day in range(days):
        for session in range(sessions_per_day):
            if session_num >= total_sessions:
                break
            
            session_date = current_date + timedelta(days=day)
            # Use modulo to cycle through topics, but shuffle first for variety
            topic = topics[session_num % len(topics)] if topics else f"{subject} Topic {session_num + 1}"
            
            schedule.append({
                'date': session_date.strftime('%Y-%m-%d'),
                'day': session_date.strftime('%A'),
                'time': f"{9 + session * 3}:00 AM" if session == 0 else f"{2 + session * 2}:00 PM",
                'duration': f"{hours_per_session:.1f} hours",
                'topic': topic,
                'activities': get_activities_for_topic(topic, subject)
            })
            
            session_num += 1
        
        if session_num >= total_sessions:
            break
    
    return schedule

def get_study_topics(subject):
    """Get study topics for a subject with randomization"""
    import random
    
    # Expanded topic banks for each subject
    topics_map = {
        'Mathematics': [
            'Algebra Basics', 'Linear Equations', 'Quadratic Equations', 'Polynomials', 
            'Geometry Fundamentals', 'Triangles & Angles', 'Circles & Areas', 'Coordinate Geometry',
            'Trigonometry', 'Calculus Basics', 'Derivatives', 'Integrals',
            'Statistics & Probability', 'Data Analysis', 'Problem Solving Strategies',
            'Number Systems', 'Fractions & Decimals', 'Percentages', 'Ratios & Proportions'
        ],
        'Science': [
            'Scientific Method', 'Lab Safety', 'Measurement & Units', 'Data Collection',
            'Physics Fundamentals', 'Forces & Motion', 'Energy & Work', 'Waves & Sound',
            'Chemistry Basics', 'Atoms & Molecules', 'Chemical Reactions', 'Periodic Table',
            'Biology Fundamentals', 'Cell Structure', 'Genetics', 'Ecology',
            'Earth Science', 'Weather & Climate', 'Astronomy Basics'
        ],
        'History': [
            'Timeline Review', 'Chronological Events', 'Historical Periods', 'Ancient Civilizations',
            'World Wars', 'Revolutionary Movements', 'Political Systems', 'Economic History',
            'Cultural Developments', 'Social Changes', 'Important Figures', 'Key Battles',
            'Document Analysis', 'Primary Sources', 'Historical Interpretation', 'Cause & Effect',
            'Geography & History', 'Trade Routes', 'Colonization & Independence'
        ],
        'English': [
            'Reading Comprehension', 'Text Analysis', 'Literary Devices', 'Poetry Analysis',
            'Grammar Fundamentals', 'Parts of Speech', 'Sentence Structure', 'Punctuation',
            'Vocabulary Building', 'Word Roots', 'Synonyms & Antonyms', 'Context Clues',
            'Writing Skills', 'Essay Writing', 'Creative Writing', 'Research Writing',
            'Literature Analysis', 'Character Study', 'Theme & Symbolism', 'Narrative Techniques'
        ],
        'Physics': [
            'Mechanics', 'Kinematics', 'Dynamics', 'Energy & Momentum',
            'Thermodynamics', 'Heat & Temperature', 'Laws of Thermodynamics',
            'Electromagnetism', 'Electric Fields', 'Magnetic Fields', 'Circuits',
            'Waves & Optics', 'Sound Waves', 'Light & Reflection', 'Refraction',
            'Modern Physics', 'Quantum Mechanics', 'Relativity', 'Nuclear Physics'
        ],
        'Chemistry': [
            'Atomic Structure', 'Periodic Table', 'Chemical Bonding', 'Molecular Geometry',
            'Stoichiometry', 'Chemical Equations', 'Reaction Types', 'Balancing Equations',
            'Acids & Bases', 'pH Scale', 'Titration', 'Buffer Solutions',
            'Organic Chemistry', 'Hydrocarbons', 'Functional Groups', 'Biochemistry',
            'Thermochemistry', 'Reaction Rates', 'Equilibrium', 'Electrochemistry'
        ],
        'Biology': [
            'Cell Biology', 'Cell Structure', 'Cell Division', 'Cellular Respiration',
            'Genetics', 'DNA & RNA', 'Protein Synthesis', 'Inheritance Patterns',
            'Evolution', 'Natural Selection', 'Speciation', 'Phylogeny',
            'Ecology', 'Ecosystems', 'Food Webs', 'Population Dynamics',
            'Human Anatomy', 'Organ Systems', 'Physiology', 'Disease & Immunity'
        ],
        'default': [
            'Fundamentals', 'Key Concepts', 'Core Principles', 'Basic Theory',
            'Practice Problems', 'Application Exercises', 'Problem Solving',
            'Review Notes', 'Summary Creation', 'Concept Mapping',
            'Self-Assessment', 'Practice Tests', 'Review Sessions'
        ]
    }
    
    # Normalize subject name
    subject_lower = subject.lower()
    matched_subject = None
    
    # Match subject
    for key in topics_map.keys():
        if key.lower() == subject_lower or subject_lower in key.lower() or key.lower() in subject_lower:
            matched_subject = key
            break
    
    # Check variations
    subject_variations = {
        'math': 'Mathematics', 'maths': 'Mathematics',
        'chem': 'Chemistry', 'bio': 'Biology', 'phys': 'Physics',
        'hist': 'History', 'eng': 'English', 'sci': 'Science'
    }
    
    if not matched_subject and subject_lower in subject_variations:
        matched_subject = subject_variations[subject_lower]
    
    # Get topics for matched subject
    if matched_subject and matched_subject in topics_map:
        available_topics = topics_map[matched_subject].copy()
    else:
        available_topics = topics_map['default'].copy()
    
    # Shuffle and return 8-12 random topics
    random.shuffle(available_topics)
    return available_topics[:random.randint(8, min(12, len(available_topics)))]

def get_activities_for_topic(topic, subject):
    """Get subject-specific activities for a study topic"""
    import random
    
    # Subject-specific activity templates
    activity_templates = {
        'Mathematics': [
            f"Solve 10 practice problems on {topic}",
            f"Review formulas and theorems related to {topic}",
            f"Create example problems for {topic}",
            f"Work through step-by-step solutions",
            f"Practice mental math for {topic}",
            f"Complete worksheets on {topic}",
            f"Watch tutorial videos on {topic}",
            f"Explain {topic} concepts to someone else",
            f"Create flashcards for {topic} formulas",
            f"Solve word problems involving {topic}"
        ],
        'Science': [
            f"Review key concepts of {topic}",
            f"Create diagrams for {topic}",
            f"Conduct experiments related to {topic}",
            f"Read scientific articles on {topic}",
            f"Take notes on {topic} terminology",
            f"Create concept maps for {topic}",
            f"Watch educational videos on {topic}",
            f"Practice labeling diagrams for {topic}",
            f"Review lab procedures for {topic}",
            f"Write summaries of {topic} experiments"
        ],
        'History': [
            f"Create timeline for {topic}",
            f"Read primary sources on {topic}",
            f"Analyze historical documents on {topic}",
            f"Research key figures in {topic}",
            f"Map geographical locations for {topic}",
            f"Create cause-effect charts for {topic}",
            f"Write essays on {topic} significance",
            f"Compare different perspectives on {topic}",
            f"Review historical context of {topic}",
            f"Create presentations on {topic}"
        ],
        'English': [
            f"Read passages related to {topic}",
            f"Practice grammar exercises on {topic}",
            f"Write essays incorporating {topic}",
            f"Analyze literary devices in {topic}",
            f"Build vocabulary for {topic}",
            f"Practice reading comprehension on {topic}",
            f"Create writing samples for {topic}",
            f"Review literary analysis of {topic}",
            f"Practice spelling and usage for {topic}",
            f"Discuss themes related to {topic}"
        ],
        'Physics': [
            f"Solve physics problems on {topic}",
            f"Review formulas for {topic}",
            f"Conduct experiments on {topic}",
            f"Create diagrams for {topic} concepts",
            f"Practice unit conversions for {topic}",
            f"Work through derivations for {topic}",
            f"Review lab reports on {topic}",
            f"Solve numerical problems on {topic}",
            f"Create concept summaries for {topic}",
            f"Practice problem-solving strategies for {topic}"
        ],
        'Chemistry': [
            f"Balance chemical equations for {topic}",
            f"Review periodic table for {topic}",
            f"Practice naming compounds in {topic}",
            f"Conduct lab experiments on {topic}",
            f"Create molecular models for {topic}",
            f"Solve stoichiometry problems for {topic}",
            f"Review reaction mechanisms for {topic}",
            f"Practice calculations for {topic}",
            f"Create study guides for {topic}",
            f"Review safety procedures for {topic}"
        ],
        'Biology': [
            f"Label diagrams for {topic}",
            f"Review cell structures in {topic}",
            f"Create concept maps for {topic}",
            f"Study anatomical structures for {topic}",
            f"Review biological processes in {topic}",
            f"Practice terminology for {topic}",
            f"Create flashcards for {topic}",
            f"Review lab procedures for {topic}",
            f"Study classification systems for {topic}",
            f"Create visual summaries for {topic}"
        ],
        'default': [
            f"Review {topic} concepts",
            f"Complete practice exercises on {topic}",
            f"Take detailed notes on {topic}",
            f"Create summary of {topic}",
            f"Self-quiz on {topic} material",
            f"Watch educational content on {topic}",
            f"Discuss {topic} with study group",
            f"Create mind map for {topic}",
            f"Review previous notes on {topic}",
            f"Practice application of {topic}"
        ]
    }
    
    # Normalize subject
    subject_lower = subject.lower()
    matched_subject = None
    
    for key in activity_templates.keys():
        if key.lower() == subject_lower or subject_lower in key.lower() or key.lower() in subject_lower:
            matched_subject = key
            break
    
    subject_variations = {
        'math': 'Mathematics', 'maths': 'Mathematics',
        'chem': 'Chemistry', 'bio': 'Biology', 'phys': 'Physics',
        'hist': 'History', 'eng': 'English', 'sci': 'Science'
    }
    
    if not matched_subject and subject_lower in subject_variations:
        matched_subject = subject_variations[subject_lower]
    
    # Get activities for matched subject
    if matched_subject and matched_subject in activity_templates:
        available_activities = activity_templates[matched_subject].copy()
    else:
        available_activities = activity_templates['default'].copy()
    
    # Shuffle and return 3 random activities
    random.shuffle(available_activities)
    return available_activities[:3]

@app.route('/download_schedule', methods=['POST'])
def download_schedule():
    """Download study schedule as CSV"""
    try:
        data = request.get_json()
        schedule = data.get('schedule', [])
        subject = data.get('subject', 'Study')
        
        if not schedule:
            return jsonify({'error': 'No schedule data provided'}), 400
        
        # Create CSV
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Date', 'Day', 'Time', 'Duration', 'Topic', 'Activities'])
        
        # Write schedule rows
        for session in schedule:
            activities = ', '.join(session.get('activities', []))
            writer.writerow([
                session.get('date', ''),
                session.get('day', ''),
                session.get('time', ''),
                session.get('duration', ''),
                session.get('topic', ''),
                activities
            ])
        
        # Create file response
        output.seek(0)
        filename = f"{subject}_study_schedule_{datetime.now().strftime('%Y%m%d')}.csv"
        
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'AI Study Pal is running'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))