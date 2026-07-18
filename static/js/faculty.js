// Faculty Dashboard JavaScript

let currentGradeData = null;

// Load My Students
async function loadMyStudents() {
    const container = document.getElementById('my-students-container');
    container.innerHTML = '<div class="loading">Loading students...</div>';
    
    try {
        const response = await fetch('/api/faculty/my-students');
        const result = await response.json();
        
        if (result.success) {
            displayMyStudents(result.students);
            populateStudentSelector(result.students);
        } else {
            container.innerHTML = '<div class="empty-state"><p>Error loading students</p></div>';
        }
    } catch (error) {
        container.innerHTML = '<div class="empty-state"><p>Error loading students</p></div>';
    }
}

// Display My Students
function displayMyStudents(students) {
    const container = document.getElementById('my-students-container');
    
    if (students.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>📝 No students assigned yet. Go to "Assign Student" tab to add students.</p></div>';
        return;
    }
    
    let html = '';
    students.forEach(student => {
        html += `
            <div class="student-item">
                <div class="student-header">
                    <div>
                        <div class="submission-title">${student.name}</div>
                        <div class="student-id">ID: ${student.user_id}</div>
                    </div>
                    <button class="btn btn-primary" onclick="viewStudentWork('${student.user_id}')">
                        View Submissions
                    </button>
                </div>
                <div class="submission-details">
                    <div class="detail-row">
                        <span class="detail-label">Username:</span>
                        <span class="detail-value">${student.username}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Email:</span>
                        <span class="detail-value">${student.email}</span>
                    </div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// Populate Student Selector for Grading
function populateStudentSelector(students) {
    const select = document.getElementById('grade-student-select');
    if (!select) return;
    
    select.innerHTML = '<option value="">-- Choose a student --</option>';
    students.forEach(student => {
        const option = document.createElement('option');
        option.value = student.user_id;
        option.textContent = `${student.name} (${student.user_id})`;
        select.appendChild(option);
    });
}

// View Student Work (switch to grade tab)
function viewStudentWork(studentId) {
    // Switch to grade tab
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    
    document.querySelector('[data-tab="grade"]').classList.add('active');
    document.getElementById('grade-tab').classList.add('active');
    
    // Select student in dropdown
    document.getElementById('grade-student-select').value = studentId;
    loadStudentSubmissions(studentId);
}

// Load All Students for Assignment
async function loadAllStudents() {
    const container = document.getElementById('all-students-container');
    container.innerHTML = '<div class="loading">Loading students...</div>';
    
    try {
        const response = await fetch('/api/faculty/students');
        const result = await response.json();
        
        if (result.success) {
            displayAllStudents(result.students);
        } else {
            container.innerHTML = '<div class="empty-state"><p>Error loading students</p></div>';
        }
    } catch (error) {
        container.innerHTML = '<div class="empty-state"><p>Error loading students</p></div>';
    }
}

// Display All Students
function displayAllStudents(students) {
    const container = document.getElementById('all-students-container');
    
    if (students.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>📝 No students registered yet.</p></div>';
        return;
    }
    
    let html = '';
    students.forEach(student => {
        html += `
            <div class="student-item">
                <div class="student-header">
                    <div>
                        <div class="submission-title">${student.name}</div>
                        <div class="student-id">ID: ${student.user_id}</div>
                    </div>
                    <button class="btn btn-success" onclick="assignStudent('${student.user_id}')">
                        Assign
                    </button>
                </div>
                <div class="submission-details">
                    <div class="detail-row">
                        <span class="detail-label">Username:</span>
                        <span class="detail-value">${student.username}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Email:</span>
                        <span class="detail-value">${student.email}</span>
                    </div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// Assign Student
async function assignStudent(studentId) {
    try {
        const response = await fetch('/api/faculty/assign-student', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ student_id: studentId })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast(result.message, 'success');
            loadAllStudents(); // Refresh list
            loadMyStudents(); // Refresh my students
        } else {
            showToast(result.message, 'error');
        }
    } catch (error) {
        showToast('An error occurred. Please try again.', 'error');
    }
}

// Search Students
const searchInput = document.getElementById('student-search');
if (searchInput) {
    searchInput.addEventListener('input', debounce((e) => {
        const searchTerm = e.target.value.toLowerCase();
        const studentItems = document.querySelectorAll('.student-item');
        
        studentItems.forEach(item => {
            const text = item.textContent.toLowerCase();
            if (text.includes(searchTerm)) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    }, 300));
}

// Load Student Submissions
async function loadStudentSubmissions(studentId) {
    const container = document.getElementById('student-submissions-container');
    container.innerHTML = '<div class="loading">Loading submissions...</div>';
    
    try {
        const response = await fetch(`/api/faculty/student-submissions/${studentId}`);
        const result = await response.json();
        
        if (result.success) {
            displayStudentSubmissions(result.submissions, studentId);
        } else {
            container.innerHTML = `<div class="empty-state"><p>${result.message}</p></div>`;
        }
    } catch (error) {
        container.innerHTML = '<div class="empty-state"><p>Error loading submissions</p></div>';
    }
}

// Display Student Submissions
function displayStudentSubmissions(submissions, studentId) {
    const container = document.getElementById('student-submissions-container');
    
    const hasSubmissions = submissions.projects.length > 0 || 
                          submissions.internships.length > 0 || 
                          submissions.seminars.length > 0;
    
    if (!hasSubmissions) {
        container.innerHTML = '<div class="empty-state"><p>📝 This student has no submissions yet.</p></div>';
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
                        <div style="display: flex; gap: 0.5rem; align-items: center;">
                            ${proj.marks ? 
                                `<span class="marks-badge graded">✓ ${proj.marks}/100</span>` : 
                                `<span class="marks-badge not-graded">⏳ Not Graded</span>`
                            }
                            <button class="btn btn-primary" onclick="openGradeModal('project', '${proj.project_id}', '${proj.title}', ${proj.marks || 0})">
                                ${proj.marks ? 'Update' : 'Grade'}
                            </button>
                        </div>
                    </div>
                    <div class="submission-details">
                        ${proj.description ? `<div class="detail-row"><span class="detail-label">Description:</span><span class="detail-value">${proj.description}</span></div>` : ''}
                        <div class="detail-row"><span class="detail-label">Status:</span><span class="detail-value">${proj.status}</span></div>
                        ${proj.start_date ? `<div class="detail-row"><span class="detail-label">Duration:</span><span class="detail-value">${formatDate(proj.start_date)} to ${formatDate(proj.end_date)}</span></div>` : ''}
                        ${proj.github_link ? `<div class="detail-row"><span class="detail-label">GitHub:</span><span class="detail-value"><a href="${proj.github_link}" target="_blank">${proj.github_link}</a></span></div>` : ''}
                        ${proj.live_link ? `<div class="detail-row"><span class="detail-label">Live Link:</span><span class="detail-value"><a href="${proj.live_link}" target="_blank">${proj.live_link}</a></span></div>` : ''}
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
                        <div style="display: flex; gap: 0.5rem; align-items: center;">
                            ${intern.marks ? 
                                `<span class="marks-badge graded">✓ ${intern.marks}/100</span>` : 
                                `<span class="marks-badge not-graded">⏳ Not Graded</span>`
                            }
                            <button class="btn btn-primary" onclick="openGradeModal('internship', '${intern.internship_id}', '${intern.company_name} - ${intern.position}', ${intern.marks || 0})">
                                ${intern.marks ? 'Update' : 'Grade'}
                            </button>
                        </div>
                    </div>
                    <div class="submission-details">
                        <div class="detail-row"><span class="detail-label">Status:</span><span class="detail-value">${intern.status}</span></div>
                        ${intern.start_date ? `<div class="detail-row"><span class="detail-label">Duration:</span><span class="detail-value">${formatDate(intern.start_date)} to ${formatDate(intern.end_date)}</span></div>` : ''}
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
                        <div style="display: flex; gap: 0.5rem; align-items: center;">
                            ${sem.marks ? 
                                `<span class="marks-badge graded">✓ ${sem.marks}/100</span>` : 
                                `<span class="marks-badge not-graded">⏳ Not Graded</span>`
                            }
                            <button class="btn btn-primary" onclick="openGradeModal('seminar', '${sem.seminar_id}', '${sem.topic}', ${sem.marks || 0})">
                                ${sem.marks ? 'Update' : 'Grade'}
                            </button>
                        </div>
                    </div>
                    <div class="submission-details">
                        ${sem.description ? `<div class="detail-row"><span class="detail-label">Description:</span><span class="detail-value">${sem.description}</span></div>` : ''}
                        ${sem.seminar_date ? `<div class="detail-row"><span class="detail-label">Date:</span><span class="detail-value">${formatDate(sem.seminar_date)}</span></div>` : ''}
                        ${sem.venue ? `<div class="detail-row"><span class="detail-label">Venue:</span><span class="detail-value">${sem.venue}</span></div>` : ''}
                    </div>
                </div>
            `;
        });
    }
    
    container.innerHTML = html;
}

// Student Selector Change Event
document.getElementById('grade-student-select')?.addEventListener('change', (e) => {
    const studentId = e.target.value;
    if (studentId) {
        loadStudentSubmissions(studentId);
    } else {
        document.getElementById('student-submissions-container').innerHTML = '<div class="empty-state"><p>👆 Select a student to view their submissions</p></div>';
    }
});

// Open Grade Modal
function openGradeModal(type, id, title, currentMarks) {
    currentGradeData = { type, id, title };
    
    const modal = document.getElementById('gradeModal');
    const detailsDiv = document.getElementById('grade-item-details');
    const marksInput = document.getElementById('grade-marks');
    
    const typeLabels = {
        'project': '📁 Project',
        'internship': '💼 Internship',
        'seminar': '🎤 Seminar'
    };
    
    detailsDiv.innerHTML = `
        <div class="info-box">
            <p><strong>${typeLabels[type]}</strong></p>
            <p>${title}</p>
            <p style="font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.5rem;">ID: ${id}</p>
        </div>
    `;
    
    marksInput.value = currentMarks > 0 ? currentMarks : '';
    modal.classList.add('active');
}

// Close Grade Modal
function closeGradeModal() {
    const modal = document.getElementById('gradeModal');
    modal.classList.remove('active');
    currentGradeData = null;
    document.getElementById('grade-marks').value = '';
}

// Submit Grade
async function submitGrade() {
    if (!currentGradeData) return;
    
    const marks = parseInt(document.getElementById('grade-marks').value);
    
    if (isNaN(marks) || marks < 0 || marks > 100) {
        showToast('Please enter marks between 0 and 100', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/faculty/grade', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                submission_type: currentGradeData.type,
                submission_id: currentGradeData.id,
                marks: marks
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast(result.message, 'success');
            closeGradeModal();
            // Reload submissions
            const studentId = document.getElementById('grade-student-select').value;
            if (studentId) {
                loadStudentSubmissions(studentId);
            }
        } else {
            showToast(result.message, 'error');
        }
    } catch (error) {
        showToast('An error occurred. Please try again.', 'error');
    }
}

// Close modal when clicking outside
document.getElementById('gradeModal')?.addEventListener('click', (e) => {
    if (e.target.id === 'gradeModal') {
        closeGradeModal();
    }
});

// Auto-load data when tabs are clicked
document.addEventListener('DOMContentLoaded', () => {
    const studentsTab = document.querySelector('[data-tab="students"]');
    const assignTab = document.querySelector('[data-tab="assign"]');
    const gradeTab = document.querySelector('[data-tab="grade"]');
    
    if (studentsTab) {
        studentsTab.addEventListener('click', loadMyStudents);
        // Load on initial page load
        loadMyStudents();
    }
    
    if (assignTab) {
        assignTab.addEventListener('click', loadAllStudents);
    }
    
    if (gradeTab) {
        gradeTab.addEventListener('click', loadMyStudents); // Load students for selector
    }
});
