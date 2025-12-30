// AI Study Pal - Frontend JavaScript

let currentSchedule = [];
let currentSubject = '';

document.getElementById('studyForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    
    // Show loading
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');
    
    try {
        const response = await fetch('/generate', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.error) {
            alert('Error: ' + data.error);
            document.getElementById('loading').classList.add('hidden');
            return;
        }
        
        // Store data
        currentSchedule = data.study_plan;
        currentSubject = data.subject;
        
        // Display results
        displayResults(data);
        
        // Hide loading, show results
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('results').classList.remove('hidden');
        
        // Scroll to results
        document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
        
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
        document.getElementById('loading').classList.add('hidden');
    }
});

function displayResults(data) {
    // Display schedule
    displaySchedule(data.study_plan);
    
    // Display quiz
    displayQuiz(data.quiz);
    
    // Display summary if available
    if (data.summary) {
        document.getElementById('summarySection').classList.remove('hidden');
        document.getElementById('summary').innerHTML = `<div class="summary-box">${data.summary}</div>`;
    } else {
        document.getElementById('summarySection').classList.add('hidden');
    }
    
    // Display tips
    displayTips(data.tips);
    
    // Display resources
    displayResources(data.resources);
    
    // Display feedback
    displayFeedback(data.feedback);
}

function displaySchedule(schedule) {
    const scheduleDiv = document.getElementById('schedule');
    scheduleDiv.innerHTML = '';
    
    if (schedule.length === 0) {
        scheduleDiv.innerHTML = '<p>No schedule generated.</p>';
        return;
    }
    
    schedule.forEach((session, index) => {
        const sessionDiv = document.createElement('div');
        sessionDiv.className = 'schedule-item';
        
        const activities = session.activities ? session.activities.join(', ') : '';
        
        sessionDiv.innerHTML = `
            <strong>Session ${index + 1}</strong><br>
            <strong>Date:</strong> ${session.date} (${session.day})<br>
            <strong>Time:</strong> ${session.time}<br>
            <strong>Duration:</strong> ${session.duration}<br>
            <strong>Topic:</strong> ${session.topic}<br>
            <strong>Activities:</strong> ${activities}
        `;
        
        scheduleDiv.appendChild(sessionDiv);
    });
}

function displayQuiz(quiz) {
    const quizDiv = document.getElementById('quiz');
    quizDiv.innerHTML = '';
    
    if (!quiz || quiz.length === 0) {
        quizDiv.innerHTML = '<p>No quiz generated.</p>';
        return;
    }
    
    quiz.forEach((q, index) => {
        const quizItem = document.createElement('div');
        quizItem.className = 'quiz-item';
        
        const difficultyClass = q.difficulty === 'easy' ? 'difficulty-easy' : 'difficulty-medium';
        
        let optionsHtml = '<ul class="quiz-options">';
        q.options.forEach((option, optIndex) => {
            const isCorrect = optIndex === q.correct;
            const correctClass = isCorrect ? 'correct' : '';
            optionsHtml += `<li class="${correctClass}">${String.fromCharCode(65 + optIndex)}. ${option} ${isCorrect ? '✓' : ''}</li>`;
        });
        optionsHtml += '</ul>';
        
        quizItem.innerHTML = `
            <h3>Question ${index + 1}: ${q.question}</h3>
            <span class="difficulty-badge difficulty-${q.difficulty}">${q.difficulty}</span>
            ${optionsHtml}
        `;
        
        quizDiv.appendChild(quizItem);
    });
}

function displayTips(tips) {
    const tipsDiv = document.getElementById('tips');
    tipsDiv.innerHTML = '';
    
    if (!tips || tips.length === 0) {
        tipsDiv.innerHTML = '<p>No tips generated.</p>';
        return;
    }
    
    tips.forEach((tip, index) => {
        const tipDiv = document.createElement('div');
        tipDiv.className = 'tip-item';
        tipDiv.innerHTML = `<strong>${index + 1}.</strong> ${tip}`;
        tipsDiv.appendChild(tipDiv);
    });
}

function displayResources(resources) {
    const resourcesDiv = document.getElementById('resources');
    resourcesDiv.innerHTML = '';
    
    if (!resources || resources.length === 0) {
        resourcesDiv.innerHTML = '<p>No resources available.</p>';
        return;
    }
    
    resources.forEach((resource) => {
        const resourceDiv = document.createElement('div');
        resourceDiv.className = 'resource-item';
        resourceDiv.innerHTML = `
            <div>
                <a href="${resource.url}" target="_blank">${resource.name}</a>
                <div class="resource-type">${resource.type}</div>
            </div>
        `;
        resourcesDiv.appendChild(resourceDiv);
    });
}

function displayFeedback(feedback) {
    const feedbackDiv = document.getElementById('feedback');
    feedbackDiv.innerHTML = `<div class="feedback-box">${feedback}</div>`;
}

// Download schedule as CSV
document.getElementById('downloadBtn').addEventListener('click', async () => {
    if (currentSchedule.length === 0) {
        alert('No schedule to download.');
        return;
    }
    
    try {
        const response = await fetch('/download_schedule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                schedule: currentSchedule,
                subject: currentSubject
            })
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${currentSubject}_study_schedule.csv`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } else {
            const error = await response.json();
            alert('Error downloading schedule: ' + error.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while downloading the schedule.');
    }
});


