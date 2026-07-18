// Student Dashboard JavaScript

// Submit Project Form
document.getElementById('projectForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        title: document.getElementById('project_title').value,
        description: document.getElementById('project_desc').value,
        start_date: document.getElementById('project_start').value,
        end_date: document.getElementById('project_end').value,
        status: document.getElementById('project_status').value,
        github_link: document.getElementById('project_github').value,
        live_link: document.getElementById('project_live').value
    };
    
    try {
        const response = await fetch('/api/student/submit-project', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast(result.message, 'success');
            document.getElementById('projectForm').reset();
        } else {
            showToast(result.message, 'error');
        }
    } catch (error) {
        showToast('An error occurred. Please try again.', 'error');
    }
});

// Submit Internship Form
document.getElementById('internshipForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        company_name: document.getElementById('intern_company').value,
        position: document.getElementById('intern_position').value,
        start_date: document.getElementById('intern_start').value,
        end_date: document.getElementById('intern_end').value,
        status: document.getElementById('intern_status').value
    };
    
    try {
        const response = await fetch('/api/student/apply-internship', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast(result.message, 'success');
            document.getElementById('internshipForm').reset();
        } else {
            showToast(result.message, 'error');
        }
    } catch (error) {
        showToast('An error occurred. Please try again.', 'error');
    }
});

// Submit Seminar Form
document.getElementById('seminarForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        topic: document.getElementById('seminar_topic').value,
        description: document.getElementById('seminar_desc').value,
        seminar_date: document.getElementById('seminar_date').value,
        venue: document.getElementById('seminar_venue').value
    };
    
    try {
        const response = await fetch('/api/student/present-seminar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast(result.message, 'success');
            document.getElementById('seminarForm').reset();
        } else {
            showToast(result.message, 'error');
        }
    } catch (error) {
        showToast('An error occurred. Please try again.', 'error');
    }
});

// Load Submissions
async function loadSubmissions() {
    const container = document.getElementById('submissions-container');
    container.innerHTML = '<div class="loading">Loading submissions...</div>';
    
    try {
        const response = await fetch('/api/student/submissions');
        const result = await response.json();
        
        if (result.success) {
            displaySubmissions(result.submissions);
        } else {
            container.innerHTML = '<div class="empty-state"><p>Error loading submissions</p></div>';
        }
    } catch (error) {
        container.innerHTML = '<div class="empty-state"><p>Error loading submissions</p></div>';
    }
}

// Display Submissions
function displaySubmissions(submissions) {
    const container = document.getElementById('submissions-container');
    
    const hasSubmissions = submissions.projects.length > 0 || 
                          submissions.internships.length > 0 || 
                          submissions.seminars.length > 0;
    
    if (!hasSubmissions) {
        container.innerHTML = '<div class="empty-state"><p>📝 No submissions yet. Start by submitting your work!</p></div>';
        return;
    }
    
    let html = '';
    
    // Display Projects
    if (submissions.projects.length > 0) {
        html += '<h3 style="margin-bottom: 1rem; color: var(--primary-color);">📁 Projects</h3>';
        submissions.projects.forEach(proj => {
            html += `
                <div class="submission-item">
                    <div class="submission-header">
                        <div>
                            <div class="submission-title">${proj.title}</div>
                            <div class="submission-id">ID: ${proj.project_id}</div>
                        </div>
                        ${proj.marks ? 
                            `<span class="marks-badge graded">✓ ${proj.marks}/100</span>` : 
                            `<span class="marks-badge not-graded">⏳ Not Graded</span>`
                        }
                    </div>
                    <div class="submission-details">
                        ${proj.description ? `<div class="detail-row"><span class="detail-label">Description:</span><span class="detail-value">${proj.description}</span></div>` : ''}
                        <div class="detail-row"><span class="detail-label">Status:</span><span class="detail-value">${proj.status}</span></div>
                        ${proj.start_date ? `<div class="detail-row"><span class="detail-label">Duration:</span><span class="detail-value">${formatDate(proj.start_date)} to ${formatDate(proj.end_date)}</span></div>` : ''}
                        ${proj.github_link ? `<div class="detail-row"><span class="detail-label">GitHub:</span><span class="detail-value"><a href="${proj.github_link}" target="_blank">${proj.github_link}</a></span></div>` : ''}
                        ${proj.live_link ? `<div class="detail-row"><span class="detail-label">Live Link:</span><span class="detail-value"><a href="${proj.live_link}" target="_blank">${proj.live_link}</a></span></div>` : ''}
                        ${proj.graded_by ? `<div class="detail-row"><span class="detail-label">Graded by:</span><span class="detail-value">${proj.graded_by}</span></div>` : ''}
                    </div>
                </div>
            `;
        });
    }
    
    // Display Internships
    if (submissions.internships.length > 0) {
        html += '<h3 style="margin-top: 2rem; margin-bottom: 1rem; color: var(--primary-color);">💼 Internships</h3>';
        submissions.internships.forEach(intern => {
            html += `
                <div class="submission-item">
                    <div class="submission-header">
                        <div>
                            <div class="submission-title">${intern.company_name} - ${intern.position}</div>
                            <div class="submission-id">ID: ${intern.internship_id}</div>
                        </div>
                        ${intern.marks ? 
                            `<span class="marks-badge graded">✓ ${intern.marks}/100</span>` : 
                            `<span class="marks-badge not-graded">⏳ Not Graded</span>`
                        }
                    </div>
                    <div class="submission-details">
                        <div class="detail-row"><span class="detail-label">Status:</span><span class="detail-value">${intern.status}</span></div>
                        ${intern.start_date ? `<div class="detail-row"><span class="detail-label">Duration:</span><span class="detail-value">${formatDate(intern.start_date)} to ${formatDate(intern.end_date)}</span></div>` : ''}
                        ${intern.graded_by ? `<div class="detail-row"><span class="detail-label">Graded by:</span><span class="detail-value">${intern.graded_by}</span></div>` : ''}
                    </div>
                </div>
            `;
        });
    }
    
    // Display Seminars
    if (submissions.seminars.length > 0) {
        html += '<h3 style="margin-top: 2rem; margin-bottom: 1rem; color: var(--primary-color);">🎤 Seminars</h3>';
        submissions.seminars.forEach(sem => {
            html += `
                <div class="submission-item">
                    <div class="submission-header">
                        <div>
                            <div class="submission-title">${sem.topic}</div>
                            <div class="submission-id">ID: ${sem.seminar_id}</div>
                        </div>
                        ${sem.marks ? 
                            `<span class="marks-badge graded">✓ ${sem.marks}/100</span>` : 
                            `<span class="marks-badge not-graded">⏳ Not Graded</span>`
                        }
                    </div>
                    <div class="submission-details">
                        ${sem.description ? `<div class="detail-row"><span class="detail-label">Description:</span><span class="detail-value">${sem.description}</span></div>` : ''}
                        ${sem.seminar_date ? `<div class="detail-row"><span class="detail-label">Date:</span><span class="detail-value">${formatDate(sem.seminar_date)}</span></div>` : ''}
                        ${sem.venue ? `<div class="detail-row"><span class="detail-label">Venue:</span><span class="detail-value">${sem.venue}</span></div>` : ''}
                        ${sem.graded_by ? `<div class="detail-row"><span class="detail-label">Graded by:</span><span class="detail-value">${sem.graded_by}</span></div>` : ''}
                    </div>
                </div>
            `;
        });
    }
    
    container.innerHTML = html;
}

// Auto-load submissions when view tab is clicked
document.addEventListener('DOMContentLoaded', () => {
    const viewTab = document.querySelector('[data-tab="view"]');
    if (viewTab) {
        viewTab.addEventListener('click', loadSubmissions);
    }
});
