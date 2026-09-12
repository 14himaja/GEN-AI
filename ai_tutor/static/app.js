/**
 * AI Personal Tutor - Interactive Frontend Controller
 * ===================================================
 * Implements:
 * 1. Day / Night theme toggle (Warm Cream Light vs Warm Espresso Dark).
 * 2. Diagnostic Assessment Results Stage (Strengths & Weaknesses before plan).
 * 3. Drag & Drop Curriculum Customizer with handle (⋮⋮), delete, and add topic.
 * 4. Auto-saving Student Study Notes widget on sidebar.
 * 5. Persistent Study History & Memory Log (Tracks what was taught, questions answered, and scores).
 */

let currentThreadId = null;
let currentGraphState = null;
let currentInterrupt = null;
let currentPlan = [];
let hasReviewedDiagnosticResults = false;
let draggedIndex = null;
let studyHistory = [];
try {
  const savedHist = localStorage.getItem("ai_tutor_study_history");
  if (savedHist) studyHistory = JSON.parse(savedHist);
} catch (e) {
  studyHistory = [];
}

function saveStudyHistory() {
  try {
    localStorage.setItem("ai_tutor_study_history", JSON.stringify(studyHistory));
  } catch (e) {
    console.warn("Could not persist study history to localStorage", e);
  }
}

window.deleteHistoryItem = function(idx) {
  if (idx >= 0 && idx < studyHistory.length) {
    studyHistory.splice(idx, 1);
    saveStudyHistory();
    updateHistoryUI();
  }
};

// DOM Elements: Navigation & Stages
const sessionStatusText = document.getElementById("session-status-text");

// Drawers & Header Buttons
const themeToggleBtn = document.getElementById("btn-theme-toggle");
const themeIcon = document.getElementById("theme-icon");
const themeLabel = document.getElementById("theme-label");
const btnOpenHistory = document.getElementById("btn-open-history");
const closeHistoryDrawerBtn = document.getElementById("close-history-drawer-btn");
const studyHistoryDrawer = document.getElementById("study-history-drawer");
const historyTimelineContainer = document.getElementById("study-history-timeline");
const historyBadgeCount = document.getElementById("history-badge-count");

// Stages
const stageSetup = document.getElementById("stage-setup");
const stageDiagnostic = document.getElementById("stage-diagnostic");
const stageDiagnosticResults = document.getElementById("stage-diagnostic-results");
const stagePlanApproval = document.getElementById("stage-plan-approval");
const stageTeaching = document.getElementById("stage-teaching");
const stageQuiz = document.getElementById("stage-quiz");
const stageQuizResult = document.getElementById("stage-quiz-result");
const stageFinalReport = document.getElementById("stage-final-report");

const allStages = [
  stageSetup,
  stageDiagnostic,
  stageDiagnosticResults,
  stagePlanApproval,
  stageTeaching,
  stageQuiz,
  stageQuizResult,
  stageFinalReport
];

function showStage(stageElement) {
  allStages.forEach(s => {
    if (s) {
      s.classList.remove("active");
    }
  });
  if (stageElement) {
    stageElement.classList.add("active");
  }
}

function updateStepper(stepNumber) {
  for (let i = 1; i <= 4; i++) {
    const el = document.getElementById(`step-nav-${i}`);
    if (!el) continue;
    el.classList.remove("active", "completed");
    if (i < stepNumber) {
      el.classList.add("completed");
    } else if (i === stepNumber) {
      el.classList.add("active");
    }
  }
}

// ---------------------------------------------------------------------------
// 1. Light / Dark Theme Switcher
// ---------------------------------------------------------------------------

function applyTheme(theme) {
  if (theme === "dark") {
    document.documentElement.setAttribute("data-theme", "dark");
    if (themeIcon) themeIcon.textContent = "☀️";
    if (themeLabel) themeLabel.textContent = "Light";
  } else {
    document.documentElement.removeAttribute("data-theme");
    if (themeIcon) themeIcon.textContent = "🌙";
    if (themeLabel) themeLabel.textContent = "Dark";
  }
  localStorage.setItem("ai_tutor_theme", theme);
}

// Initialize theme
const savedTheme = localStorage.getItem("ai_tutor_theme") || "light";
applyTheme(savedTheme);

if (themeToggleBtn) {
  themeToggleBtn.addEventListener("click", () => {
    const isDark = document.documentElement.getAttribute("data-theme") === "dark";
    applyTheme(isDark ? "light" : "dark");
  });
}

// ---------------------------------------------------------------------------
// 2. Student Notes Notepad (Auto-Saving to LocalStorage + Disk Backend)
// ---------------------------------------------------------------------------

const notesTextarea = document.getElementById("student-notes-textarea");
const notesCharCount = document.getElementById("notes-char-count");
const notesSaveStatus = document.getElementById("notes-save-status");
const btnCopyNotes = document.getElementById("btn-copy-notes");
const btnDownloadTxt = document.getElementById("btn-download-txt");
const btnDownloadDocx = document.getElementById("btn-download-docx");
const btnClearNotes = document.getElementById("btn-clear-notes");

function downloadNotesFormat(fmt) {
  const notes = notesTextarea ? (notesTextarea.value || "") : "";
  if (!notes.trim()) {
    alert("Your study notes are currently empty. Jot down some notes first!");
    return;
  }
  
  if (currentThreadId) {
    window.location.href = `/api/session/${currentThreadId}/notes/download?format=${fmt}`;
  } else {
    window.location.href = `/api/notes/download?format=${fmt}`;
  }
}

let notesSaveTimeout = null;

async function syncNotesToBackend(notesContent) {
  try {
    const endpoint = currentThreadId ? `/api/session/${currentThreadId}/notes` : `/api/notes/save`;
    const res = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ notes: notesContent })
    });
    if (res.ok && notesSaveStatus) {
      notesSaveStatus.textContent = "Saved to Disk ✓";
      notesSaveStatus.style.background = "var(--accent-sage-light)";
      notesSaveStatus.style.color = "var(--accent-sage)";
    }
  } catch (err) {
    console.warn("Backend notes sync notice:", err);
  }
}

async function loadNotes() {
  const cachedNotes = localStorage.getItem("ai_tutor_student_notes");
  if (notesTextarea) {
    if (cachedNotes) {
      notesTextarea.value = cachedNotes;
      if (notesCharCount) notesCharCount.textContent = `${cachedNotes.length} chars`;
    }
    
    try {
      const endpoint = currentThreadId ? `/api/session/${currentThreadId}/notes` : `/api/notes/latest`;
      const res = await fetch(endpoint);
      if (res.ok) {
        const data = await res.json();
        if (data.notes && !cachedNotes) {
          notesTextarea.value = data.notes;
          localStorage.setItem("ai_tutor_student_notes", data.notes);
          if (notesCharCount) notesCharCount.textContent = `${data.notes.length} chars`;
        }
      }
    } catch (e) {
      // Offline fallback
    }
  }
}

loadNotes();

if (notesTextarea) {
  notesTextarea.addEventListener("input", () => {
    const val = notesTextarea.value;
    localStorage.setItem("ai_tutor_student_notes", val);
    if (notesCharCount) notesCharCount.textContent = `${val.length} chars`;
    if (notesSaveStatus) {
      notesSaveStatus.textContent = "Saving...";
      notesSaveStatus.style.background = "var(--accent-honey-light)";
      notesSaveStatus.style.color = "var(--accent-honey)";
    }

    clearTimeout(notesSaveTimeout);
    notesSaveTimeout = setTimeout(() => {
      syncNotesToBackend(val);
    }, 500);
  });

  if (btnCopyNotes) {
    btnCopyNotes.addEventListener("click", () => {
      if (!notesTextarea.value) return;
      navigator.clipboard.writeText(notesTextarea.value);
      btnCopyNotes.textContent = "Copied!";
      setTimeout(() => { btnCopyNotes.textContent = "Copy"; }, 1400);
    });
  }

  if (btnDownloadTxt) {
    btnDownloadTxt.addEventListener("click", () => downloadNotesFormat("txt"));
  }

  if (btnDownloadDocx) {
    btnDownloadDocx.addEventListener("click", () => downloadNotesFormat("docx"));
  }

  if (btnClearNotes) {
    btnClearNotes.addEventListener("click", () => {
      if (confirm("Clear all your study notes?")) {
        notesTextarea.value = "";
        localStorage.removeItem("ai_tutor_student_notes");
        syncNotesToBackend("");
        if (notesCharCount) notesCharCount.textContent = "0 chars";
        if (notesSaveStatus) {
          notesSaveStatus.textContent = "Saved ✓";
          notesSaveStatus.style.background = "var(--accent-sage-light)";
          notesSaveStatus.style.color = "var(--accent-sage)";
        }
      }
    });
  }
}

// ---------------------------------------------------------------------------
// 3. Study History & Memory Log Recorder
// ---------------------------------------------------------------------------

function recordLessonHistory(topic, content) {
  if (!topic) return;
  // Avoid duplicate back-to-back entries
  const last = studyHistory[studyHistory.length - 1];
  if (last && last.type === "lesson" && last.topic === topic) return;

  studyHistory.push({
    type: "lesson",
    topic: topic,
    summary: content.summary || "",
    explanation: content.explanation || "",
    concepts: content.concepts || [],
    example: content.example || "",
    time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
  });
  saveStudyHistory();
  updateHistoryUI();
}

function recordQuizHistory(topic, lastResult, questions, studentAnswers) {
  const score = lastResult.score || 0;
  const passed = lastResult.passed ?? (score >= 70);
  const attempts = lastResult.attempts || 1;
  const maxAttempts = lastResult.max_attempts || 2;
  const maxReached = lastResult.max_attempts_reached || (!passed && attempts >= maxAttempts);

  studyHistory.push({
    type: "quiz",
    topic: topic,
    score: score,
    passed: passed,
    attempts: attempts,
    max_attempts: maxAttempts,
    max_attempts_reached: maxReached,
    feedback: lastResult.feedback || "",
    questions: questions || [],
    answers: studentAnswers || [],
    review_details: lastResult.review_details || [],
    time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
  });
  saveStudyHistory();
  updateHistoryUI();
}

function updateHistoryUI() {
  if (historyBadgeCount) {
    historyBadgeCount.textContent = studyHistory.length;
  }
  if (!historyTimelineContainer) return;

  const currentNotes = notesTextarea ? notesTextarea.value.trim() : "";
  const notesCardHtml = currentNotes ? `
    <div class="history-notes-summary-card">
      <div class="history-card-header" style="margin-bottom: 8px;">
        <span class="step-tag" style="background: var(--accent-honey-light); color: var(--accent-honey);">📝 My Saved Study Notes</span>
        <div style="display: flex; gap: 6px;">
          <button type="button" class="btn-ctrl" onclick="downloadNotesFormat('txt')">📄 Notepad (.txt)</button>
          <button type="button" class="btn-ctrl" onclick="downloadNotesFormat('docx')">📝 Word (.docx)</button>
        </div>
      </div>
      <div class="history-notes-text">${currentNotes.replace(/</g, "&lt;").replace(/>/g, "&gt;")}</div>
    </div>
  ` : "";

  if (studyHistory.length === 0) {
    historyTimelineContainer.innerHTML = `
      ${notesCardHtml}
      <div class="empty-history-notice">No study activity recorded yet. As you study and take quizzes, your progress log will appear here.</div>
    `;
    return;
  }

  historyTimelineContainer.innerHTML = notesCardHtml + studyHistory.map((item, idx) => {
    if (item.type === "lesson") {
      return `
        <div class="history-topic-card">
          <div class="history-card-header">
            <div>
              <span class="step-tag">Lesson Taught</span>
              <div class="history-topic-title">${item.topic}</div>
            </div>
            <div class="history-card-top-actions">
              <span class="text-muted" style="font-size: 0.78rem;">${item.time}</span>
              <button type="button" class="btn-delete-log-item" title="Delete this study log" onclick="deleteHistoryItem(${idx})">✕</button>
            </div>
          </div>
          <div class="history-summary-box">
            <strong>Core Explanation:</strong>
            <p>${item.explanation ? item.explanation.slice(0, 190) + '...' : 'Lesson completed.'}</p>
          </div>
          ${item.concepts && item.concepts.length ? `
            <div style="font-size: 0.8rem; color: var(--text-secondary);">
              <strong>Key Takeaways:</strong>
              <ul style="padding-left: 18px; margin-top: 4px;">
                ${item.concepts.slice(0, 3).map(c => `<li>${c}</li>`).join("")}
              </ul>
            </div>
          ` : ''}
        </div>
      `;
    } else {
      let statusTagHtml = '';
      if (item.max_attempts_reached) {
        statusTagHtml = `<span class="history-score-tag failed">Max Attempts (${item.attempts}/${item.max_attempts}) • Advanced</span>`;
      } else if (item.passed) {
        statusTagHtml = `<span class="history-score-tag passed">${item.score}% PASSED (Att. ${item.attempts}/${item.max_attempts})</span>`;
      } else {
        statusTagHtml = `<span class="history-score-tag failed">${item.score}% REVISION (Att. ${item.attempts}/${item.max_attempts})</span>`;
      }

      const details = item.review_details && item.review_details.length ? item.review_details : null;

      return `
        <div class="history-topic-card">
          <div class="history-card-header">
            <div>
              <span class="step-tag">Quiz Submission</span>
              <div class="history-topic-title">${item.topic}</div>
            </div>
            <div class="history-card-top-actions">
              ${statusTagHtml}
              <button type="button" class="btn-delete-log-item" title="Delete this study log" onclick="deleteHistoryItem(${idx})">✕</button>
            </div>
          </div>
          <p style="font-size: 0.84rem; color: var(--text-secondary); margin-bottom: 8px;">${item.feedback}</p>
          <div class="history-qa-list">
            ${details ? details.map((d, qIdx) => `
              <div class="history-qa-item">
                <div class="history-qa-question">Q${qIdx + 1}: ${d.question}</div>
                <div class="history-qa-answer">
                  <span class="qa-badge ${d.is_correct ? 'correct' : 'wrong'}">${d.is_correct ? '✓ Correct' : '✗ Incorrect'}</span>
                  <span>Your Answer: <em>${d.student_answer_text}</em></span>
                </div>
                ${!d.is_correct ? `
                  <div class="history-qa-correct">
                    <span class="qa-badge correct">✓ Correct Solution</span>
                    <span><strong>${d.correct_answer_text}</strong></span>
                  </div>
                ` : ''}
                ${d.explanation ? `
                  <div class="history-qa-explanation">
                    💡 <strong>Explanation:</strong> ${d.explanation}
                  </div>
                ` : ''}
              </div>
            `).join("") : (item.questions || []).map((q, qIdx) => {
              const userAnsIdx = item.answers && item.answers[qIdx] !== undefined ? item.answers[qIdx] : -1;
              const isCorrect = userAnsIdx === q.correct_option;
              const userAnsText = q.options && q.options[userAnsIdx] ? q.options[userAnsIdx] : 'Unanswered';
              const correctAnsText = q.options && q.options[q.correct_option] ? q.options[q.correct_option] : 'N/A';
              const explanationText = q.explanation || '';
              return `
                <div class="history-qa-item">
                  <div class="history-qa-question">Q${qIdx + 1}: ${q.question}</div>
                  <div class="history-qa-answer">
                    <span class="qa-badge ${isCorrect ? 'correct' : 'wrong'}">${isCorrect ? '✓ Correct' : '✗ Incorrect'}</span>
                    <span>Your Answer: <em>${userAnsText}</em></span>
                  </div>
                  ${!isCorrect ? `
                    <div class="history-qa-correct">
                      <span class="qa-badge correct">✓ Correct Solution</span>
                      <span><strong>${correctAnsText}</strong></span>
                    </div>
                  ` : ''}
                  ${explanationText ? `
                    <div class="history-qa-explanation">
                      💡 <strong>Explanation:</strong> ${explanationText}
                    </div>
                  ` : ''}
                </div>
              `;
            }).join("")}
          </div>
        </div>
      `;
    }
  }).reverse().join("");
}

if (btnOpenHistory) {
  btnOpenHistory.addEventListener("click", () => {
    updateHistoryUI();
    if (studyHistoryDrawer) studyHistoryDrawer.classList.add("open");
  });
}

if (closeHistoryDrawerBtn) {
  closeHistoryDrawerBtn.addEventListener("click", () => {
    if (studyHistoryDrawer) studyHistoryDrawer.classList.remove("open");
  });
}

// Clear All Study Logs
const btnClearHistory = document.getElementById("btn-clear-history");
if (btnClearHistory) {
  btnClearHistory.addEventListener("click", () => {
    if (studyHistory.length === 0) {
      alert("Study history log is already empty.");
      return;
    }
    if (confirm("Are you sure you want to delete all previous study logs?")) {
      studyHistory = [];
      saveStudyHistory();
      updateHistoryUI();
    }
  });
}

// ---------------------------------------------------------------------------
// 4. Sidebar Updates
// ---------------------------------------------------------------------------

function updateSidebar() {
  if (!currentGraphState || !currentGraphState.values) return;
  const values = currentGraphState.values;
  const student = values.student || {};

  document.getElementById("profile-name").textContent = student.name || "Student";
  document.getElementById("profile-subject").textContent = student.subject || "Subject";
  document.getElementById("profile-goal").textContent = student.goal || "Exam Prep";
  document.getElementById("profile-level-badge").textContent = values.current_difficulty || student.level || "Beginner";

  // Attempts display in profile
  const maxAttempts = values.max_quiz_attempts || student.max_quiz_attempts || 2;
  const topicAttempts = values.quiz_attempts_for_topic || 0;
  const attemptsEl = document.getElementById("profile-attempts-display");
  if (attemptsEl) {
    if (values.current_topic && topicAttempts > 0) {
      attemptsEl.textContent = `Attempt ${topicAttempts} / ${maxAttempts}`;
    } else {
      attemptsEl.textContent = `Max ${maxAttempts} / topic`;
    }
  }

  // Curriculum progress
  const plan = currentPlan.length > 0 ? currentPlan : (values.learning_plan || []);
  const completed = values.completed_topics || [];
  const current = values.current_topic;

  document.getElementById("progress-counter").textContent = `${completed.length} / ${plan.length}`;

  const listContainer = document.getElementById("curriculum-list-items");
  if (plan.length === 0) {
    listContainer.innerHTML = `<li class="empty-list-notice">Plan will appear after diagnostic check...</li>`;
    return;
  }

  listContainer.innerHTML = plan.map((topic, idx) => {
    const isDone = completed.includes(topic);
    const isCurrent = topic === current;
    let className = "curriculum-item";
    if (isDone) className += " done";
    if (isCurrent) className += " current";

    return `
      <li class="${className}">
        <span class="status-icon">${isDone ? '✓' : (idx + 1)}</span>
        <span>${topic}</span>
      </li>
    `;
  }).join("");
}

// ---------------------------------------------------------------------------
// 5. Flow Orchestrator & State Handler
// ---------------------------------------------------------------------------

function handleGraphState(stateResponse) {
  currentGraphState = stateResponse;
  currentInterrupt = stateResponse.current_interrupt;
  updateSidebar();

  // Workflow finished
  if (stateResponse.is_finished || stateResponse.values?.final_report) {
    sessionStatusText.textContent = "All Topics Completed!";
    renderFinalReport(stateResponse.values.final_report);
    return;
  }

  // Active Human-in-the-Loop Interrupt
  if (currentInterrupt) {
    sessionStatusText.textContent = "Action Required";
    
    if (currentInterrupt.action === "take_diagnostic_quiz") {
      updateStepper(2);
      renderDiagnosticTest(currentInterrupt, stateResponse.values);
    } else if (currentInterrupt.action === "review_learning_plan") {
      // REQUIREMENT 2: Show Diagnostic Assessment Strengths & Weaknesses FIRST!
      if (!hasReviewedDiagnosticResults) {
        updateStepper(2);
        renderDiagnosticResults(currentInterrupt, stateResponse.values);
      } else {
        updateStepper(3);
        renderPlanReview(currentInterrupt, stateResponse.values);
      }
    } else if (currentInterrupt.action === "take_quiz") {
      updateStepper(4);
      renderTeaching(stateResponse.values);
    }
    return;
  }

  // If teaching content is ready
  if (stateResponse.values?.teaching_content) {
    updateStepper(4);
    renderTeaching(stateResponse.values);
  }
}

// ---------------------------------------------------------------------------
// 6. Stage Renderers
// ---------------------------------------------------------------------------

// A. Step 2: Diagnostic Baseline Test
function renderDiagnosticTest(interruptData, stateValues) {
  showStage(stageDiagnostic);

  const subject = interruptData.subject || stateValues.student?.subject || "Subject";
  const questions = interruptData.questions || [];

  const badge = document.getElementById("diagnostic-subject-badge");
  if (badge) badge.textContent = subject;

  const title = document.getElementById("diagnostic-title");
  if (title) title.textContent = `${subject}: Quick Knowledge Check`;

  const container = document.getElementById("diagnostic-questions-list");
  if (!container) return;

  if (questions.length === 0) {
    container.innerHTML = `<p class="text-muted">No diagnostic questions found. Click below to continue.</p>`;
    return;
  }

  container.innerHTML = questions.map((q, qIdx) => `
    <div class="question-block">
      <h4>${qIdx + 1}. ${q.question}</h4>
      <div class="options-group">
        ${q.options.map((opt, optIdx) => `
          <label class="option-label">
            <input type="radio" name="diag_q_${qIdx}" value="${optIdx}">
            <span>${opt}</span>
          </label>
        `).join("")}
      </div>
    </div>
  `).join("");
}

// B. Step 2.5: Diagnostic Assessment Results (STRENGTHS & WEAKNESSES BREAKDOWN)
function renderDiagnosticResults(interruptData, stateValues) {
  showStage(stageDiagnosticResults);

  const scorePill = document.getElementById("diagnostic-results-score-pill");
  const score = interruptData.initial_score ?? stateValues.initial_score ?? 75;
  if (scorePill) scorePill.textContent = `Baseline Score: ${score}%`;

  const strongList = document.getElementById("diag-strong-list");
  const weakList = document.getElementById("diag-weak-list");

  const strong = interruptData.strong_topics || stateValues.strong_topics || [];
  const weak = interruptData.weak_topics || stateValues.weak_topics || [];

  if (strongList) {
    strongList.innerHTML = strong.length ? strong.map(t => `
      <li>
        <strong>${t}</strong>
        <span class="badge-accent" style="margin-left: auto;">Solid Foundation</span>
      </li>
    `).join("") : `<li>General computer science intuition</li>`;
  }

  if (weakList) {
    weakList.innerHTML = weak.length ? weak.map(t => `
      <li>
        <strong>${t}</strong>
        <span class="badge-accent" style="margin-left: auto; color: var(--accent-terracotta);">High Priority</span>
      </li>
    `).join("") : `<li>No critical weaknesses detected; advancing to core syllabus.</li>`;
  }

  const trajText = document.getElementById("diag-trajectory-text");
  if (trajText) {
    if (weak.length > 0) {
      trajText.textContent = `The planner will place ${weak.slice(0, 2).join(" and ")} at the very top of your schedule, ensuring you master high-priority areas before continuing.`;
    } else {
      trajText.textContent = `You demonstrated solid baseline mastery. The curriculum is optimized for comprehensive concept coverage and practical engineering mastery.`;
    }
  }
}

// C. Step 3: Plan Review & Interactive Drag-and-Drop Customizer
function renderPlanReview(interruptData, stateValues) {
  showStage(stagePlanApproval);

  currentPlan = [...(interruptData.plan || stateValues.learning_plan || [])];

  const weakContainer = document.getElementById("weak-topics-list");
  const strongContainer = document.getElementById("strong-topics-list");
  const scorePill = document.getElementById("diagnostic-score-pill");

  const weak = interruptData.weak_topics || stateValues.weak_topics || [];
  const strong = interruptData.strong_topics || stateValues.strong_topics || [];
  const score = interruptData.initial_score ?? stateValues.initial_score;

  if (scorePill && score !== undefined) {
    scorePill.textContent = `Score: ${score}%`;
  }

  if (weakContainer) {
    weakContainer.innerHTML = weak.length ? weak.map(t => `<span>${t}</span>`).join("") : `<span>None detected</span>`;
  }
  if (strongContainer) {
    strongContainer.innerHTML = strong.length ? strong.map(t => `<span>${t}</span>`).join("") : `<span>None detected</span>`;
  }

  renderInteractivePlanList();
}

// Native HTML5 Drag and Drop Plan Customizer
function renderInteractivePlanList() {
  const container = document.getElementById("proposed-plan-items");
  const counter = document.getElementById("plan-topics-counter");
  if (counter) {
    counter.textContent = `${currentPlan.length} Topics`;
  }
  if (!container) return;

  if (currentPlan.length === 0) {
    container.innerHTML = `<div class="empty-history-notice">No topics currently in plan. Type above to add topics.</div>`;
    return;
  }

  container.innerHTML = currentPlan.map((topic, idx) => `
    <div class="plan-topic-item" draggable="true" data-index="${idx}">
      <div class="topic-item-left">
        <span class="drag-handle" title="Drag up or down to reorder">⋮⋮</span>
        <span class="topic-item-num">${idx + 1}</span>
        <span class="topic-item-title">${topic}</span>
      </div>
      <button type="button" class="btn-remove-topic" title="Remove Topic" onclick="removeTopic(${idx})">✕</button>
    </div>
  `).join("");

  // Attach Drag & Drop handlers
  const items = container.querySelectorAll(".plan-topic-item");
  items.forEach(item => {
    item.addEventListener("dragstart", (e) => {
      draggedIndex = parseInt(item.getAttribute("data-index"), 10);
      item.classList.add("dragging");
      e.dataTransfer.effectAllowed = "move";
      e.dataTransfer.setData("text/plain", draggedIndex);
    });

    item.addEventListener("dragend", () => {
      item.classList.remove("dragging");
      items.forEach(it => it.classList.remove("drag-over"));
    });

    item.addEventListener("dragover", (e) => {
      e.preventDefault();
      e.dataTransfer.dropEffect = "move";
      item.classList.add("drag-over");
    });

    item.addEventListener("dragleave", () => {
      item.classList.remove("drag-over");
    });

    item.addEventListener("drop", (e) => {
      e.preventDefault();
      item.classList.remove("drag-over");
      const targetIndex = parseInt(item.getAttribute("data-index"), 10);

      if (draggedIndex !== null && draggedIndex !== targetIndex && !isNaN(draggedIndex) && !isNaN(targetIndex)) {
        const movedItem = currentPlan.splice(draggedIndex, 1)[0];
        currentPlan.splice(targetIndex, 0, movedItem);
        draggedIndex = null;
        renderInteractivePlanList();
        updateSidebar();
      }
    });
  });
}

window.removeTopic = function(idx) {
  if (currentPlan.length <= 1) {
    alert("Your learning plan must have at least 1 topic.");
    return;
  }
  currentPlan.splice(idx, 1);
  renderInteractivePlanList();
  updateSidebar();
};

// D. Step 4: Lesson & Teaching View
function renderTeaching(stateValues) {
  showStage(stageTeaching);

  const topic = stateValues.current_topic || "Overview";
  const diff = stateValues.current_difficulty || "Normal";
  const content = stateValues.teaching_content || {};
  const isRevision = content.is_revision || stateValues.needs_revision;
  const attempts = stateValues.quiz_attempts_for_topic || 0;
  const maxAttempts = stateValues.max_quiz_attempts || 2;

  const badge = document.getElementById("lesson-topic-badge");
  if (badge) badge.textContent = `Active Topic`;

  const title = document.getElementById("lesson-title");
  if (title) title.textContent = topic;

  const diffBadge = document.getElementById("lesson-difficulty-badge");
  if (diffBadge) diffBadge.textContent = diff;

  // Handle Revision Banner
  const revBanner = document.getElementById("teaching-revision-banner");
  const revText = document.getElementById("teaching-revision-text");
  if (revBanner) {
    if (isRevision) {
      revBanner.style.display = "flex";
      if (revText) {
        revText.innerHTML = `<strong>Topic Revision (Attempt ${attempts + 1} of ${maxAttempts}):</strong> Score on previous attempt was below 70%. Review the simplified explanation and key takeaways below before retrying the quiz.`;
      }
    } else {
      revBanner.style.display = "none";
    }
  }

  const exp = document.getElementById("lesson-explanation");
  if (exp) exp.textContent = content.explanation || "Loading explanation...";

  const conceptsList = document.getElementById("lesson-concepts");
  if (conceptsList) {
    const concepts = content.concepts || [];
    conceptsList.innerHTML = concepts.map(c => `<li>${c}</li>`).join("");
  }

  const example = document.getElementById("lesson-example");
  if (example) example.textContent = content.example || "No example provided.";

  // Record lesson in Study History
  recordLessonHistory(topic, content);
}

// E. Step 5: Topic Evaluation Quiz
function renderQuiz() {
  showStage(stageQuiz);

  const values = currentGraphState?.values || {};
  const topic = values.current_topic || "Topic";
  const maxAttempts = values.max_quiz_attempts || 2;
  const attempts = (values.quiz_attempts_for_topic || 0) + 1;
  const isFinal = attempts >= maxAttempts;
  const questions = currentInterrupt?.questions || values.current_quiz || [];

  const title = document.getElementById("quiz-topic-title");
  if (title) title.textContent = `${topic}: Evaluation Quiz`;

  const attemptBadge = document.getElementById("quiz-attempt-badge");
  if (attemptBadge) {
    attemptBadge.textContent = isFinal ? `Attempt ${attempts} of ${maxAttempts} (Final Attempt)` : `Attempt ${attempts} of ${maxAttempts}`;
    if (isFinal) {
      attemptBadge.classList.add("badge-attempt-final");
    } else {
      attemptBadge.classList.remove("badge-attempt-final");
    }
  }

  const revNotice = document.getElementById("revision-notice");
  const revText = document.getElementById("revision-feedback-text");
  if (revNotice) {
    const isRevision = values.needs_revision || currentInterrupt?.is_revision || attempts > 1;
    revNotice.style.display = isRevision ? "flex" : "none";
    if (revText) {
      revText.innerHTML = `<strong>Adaptive Evaluation (Attempt ${attempts} of ${maxAttempts}):</strong> ${isFinal ? 'This is your final quiz attempt for this topic. Passing score is 70%.' : 'Score 70% or higher to master this topic.'}`;
    }
  }

  const container = document.getElementById("quiz-questions-list");
  if (!container) return;

  container.innerHTML = questions.map((q, qIdx) => `
    <div class="question-block">
      <h4>${qIdx + 1}. ${q.question}</h4>
      <div class="options-group">
        ${q.options.map((opt, optIdx) => `
          <label class="option-label">
            <input type="radio" name="quiz_q_${qIdx}" value="${optIdx}">
            <span>${opt}</span>
          </label>
        `).join("")}
      </div>
    </div>
  `).join("");
}

// F. Step 6: Quiz Results & Routing
function renderQuizResult(lastResult, values) {
  showStage(stageQuizResult);

  const score = lastResult.score || 0;
  const passed = lastResult.passed ?? (score >= 70);
  const attempts = lastResult.attempts || values.quiz_attempts_for_topic || 1;
  const maxAttempts = lastResult.max_attempts || values.max_quiz_attempts || 2;
  const maxReached = lastResult.max_attempts_reached || (!passed && attempts >= maxAttempts);
  const currentTopicName = values.current_topic || lastResult.topic || "Topic";

  const scorePill = document.getElementById("result-score-pill");
  if (scorePill) {
    scorePill.textContent = `${score}%`;
    scorePill.className = `score-pill ${passed ? 'pass' : 'fail'}`;
  }

  // Render Explicit Attempt & Decision Banner
  const banner = document.getElementById("result-attempt-banner");
  const btnContinue = document.getElementById("btn-continue-workflow");

  if (banner) {
    if (passed) {
      banner.className = "alert-box alert-success";
      banner.innerHTML = `
        <div>
          <strong>🎉 Topic Mastered! (${score}%)</strong><br>
          <span>You successfully passed <em>${currentTopicName}</em> on Attempt ${attempts} of ${maxAttempts}. Outstanding work!</span>
        </div>
      `;
      if (btnContinue) {
        btnContinue.innerHTML = `Continue to Next Step <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>`;
      }
    } else if (maxReached) {
      banner.className = "alert-box alert-info";
      banner.innerHTML = `
        <div>
          <strong>📋 Maximum Attempts Reached (${attempts} of ${maxAttempts}):</strong><br>
          <span>You scored <strong>${score}%</strong>. You have completed all ${maxAttempts} allowed attempts for <em>${currentTopicName}</em>. Your answers and key takeaways are preserved in your <strong>Study History</strong> drawer. To maintain your forward momentum, we are advancing to the next topic.</span>
        </div>
      `;
      if (btnContinue) {
        btnContinue.innerHTML = `Advance to Next Topic <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>`;
      }
    } else {
      banner.className = "alert-box alert-warning";
      banner.innerHTML = `
        <div>
          <strong>⚠️ Revision Required (Score: ${score}%):</strong><br>
          <span>Passing threshold is 70%. You completed Attempt ${attempts} of ${maxAttempts} (<strong>${maxAttempts - attempts} retry remaining</strong>). The AI Tutor has prepared a simplified revision refresher to help you review before your final attempt.</span>
        </div>
      `;
      if (btnContinue) {
        btnContinue.innerHTML = `Proceed to Topic Revision (Attempt ${attempts + 1} of ${maxAttempts}) <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>`;
      }
    }
  }

  const msg = document.getElementById("result-feedback-message");
  if (msg) msg.textContent = lastResult.feedback || "";

  const strongList = document.getElementById("result-strong-list");
  if (strongList) {
    strongList.innerHTML = (lastResult.strong_concepts || []).map(c => `<li>✓ ${c}</li>`).join("") || "<li>None recorded</li>";
  }

  const weakList = document.getElementById("result-weak-list");
  if (weakList) {
    weakList.innerHTML = (lastResult.weak_concepts || []).map(c => `<li>⚡ ${c}</li>`).join("") || "<li>All objectives verified!</li>";
  }

  // 1. Render Question-by-Question Review with Correct Answers and Explanations
  const qaReviewList = document.getElementById("result-qa-review-list");
  const reviewDetails = lastResult.review_details;
  const questions = currentInterrupt?.questions || values.current_quiz || [];

  if (qaReviewList) {
    if (reviewDetails && reviewDetails.length > 0) {
      qaReviewList.innerHTML = reviewDetails.map((item, idx) => `
        <div class="qa-review-card ${item.is_correct ? 'correct' : 'incorrect'}">
          <div class="qa-card-question">Q${idx + 1}: ${item.question}</div>
          <div class="qa-card-answer-row">
            <span class="qa-badge ${item.is_correct ? 'correct' : 'wrong'}">${item.is_correct ? '✓ Correct' : '✗ Incorrect'}</span>
            <span>Your Answer: <em>${item.student_answer_text}</em></span>
          </div>
          ${!item.is_correct ? `
            <div class="qa-correct-box">
              <span>✓ <strong>Correct Answer:</strong> ${item.correct_answer_text}</span>
            </div>
          ` : ''}
          ${item.explanation ? `
            <div class="qa-explanation-box">
              💡 <strong>Explanation:</strong> ${item.explanation}
            </div>
          ` : ''}
        </div>
      `).join("");
    } else {
      const userAnswers = values.student_answers || [];
      qaReviewList.innerHTML = questions.map((q, idx) => {
        const studentAnsIdx = userAnswers[idx] !== undefined ? userAnswers[idx] : -1;
        const isCorrect = studentAnsIdx === q.correct_option;
        const studentAnsText = q.options && q.options[studentAnsIdx] ? q.options[studentAnsIdx] : 'Unanswered';
        const correctAnsText = q.options && q.options[q.correct_option] ? q.options[q.correct_option] : 'N/A';
        return `
          <div class="qa-review-card ${isCorrect ? 'correct' : 'incorrect'}">
            <div class="qa-card-question">Q${idx + 1}: ${q.question}</div>
            <div class="qa-card-answer-row">
              <span class="qa-badge ${isCorrect ? 'correct' : 'wrong'}">${isCorrect ? '✓ Correct' : '✗ Incorrect'}</span>
              <span>Your Answer: <em>${studentAnsText}</em></span>
            </div>
            ${!isCorrect ? `
              <div class="qa-correct-box">
                <span>✓ <strong>Correct Answer:</strong> ${correctAnsText}</span>
              </div>
            ` : ''}
            ${q.explanation ? `
              <div class="qa-explanation-box">
                💡 <strong>Explanation:</strong> ${q.explanation}
              </div>
            ` : ''}
          </div>
        `;
      }).join("");
    }
  }

  // 2. Render Targeted Revision Refresher Box
  const revBox = document.getElementById("result-revision-box");
  const revBody = document.getElementById("result-revision-body");
  if (revBox) {
    if (!passed) {
      revBox.style.display = "block";
      if (revBody) {
        const teaching = values.teaching_content || {};
        const concepts = teaching.concepts || [];
        const weak = lastResult.weak_concepts || [];

        let revIntro = '';
        if (maxReached) {
          revIntro = `<p>You have completed all ${maxAttempts} quiz attempts for <strong>${currentTopicName}</strong>. Review the targeted concepts and correct explanations above before advancing:</p>`;
        } else {
          revIntro = `<p><strong>Targeted Revision Refresher for ${currentTopicName}:</strong> Passing threshold is 70%. Carefully study the verified solutions above and key concepts below before your next attempt:</p>`;
        }

        let conceptsListHtml = '';
        if (concepts.length > 0) {
          conceptsListHtml = `
            <ul class="revision-takeaway-list">
              ${concepts.map(c => `<li>${c}</li>`).join("")}
            </ul>
          `;
        } else if (weak.length > 0) {
          conceptsListHtml = `
            <ul class="revision-takeaway-list">
              ${weak.map(w => `<li>Priority Concept: ${w}</li>`).join("")}
            </ul>
          `;
        }

        revBody.innerHTML = revIntro + conceptsListHtml;
      }
    } else {
      revBox.style.display = "none";
    }
  }

  // Record quiz in Study History
  recordQuizHistory(currentTopicName, lastResult, questions, values.student_answers);
}

// G. Step 7: Final Comprehensive Report
function renderFinalReport(report) {
  showStage(stageFinalReport);

  if (!report) return;

  document.getElementById("final-score-val").textContent = report.overall_score || 85;
  document.getElementById("final-topics-count").textContent = (report.topics_completed || []).length;
  document.getElementById("final-attempts-count").textContent = report.total_quiz_attempts || 1;

  const strongUl = document.getElementById("final-strong-areas");
  if (strongUl) {
    strongUl.innerHTML = (report.strong_areas || []).map(s => `<li>✓ ${s}</li>`).join("");
  }

  const recUl = document.getElementById("final-recommendations");
  if (recUl) {
    recUl.innerHTML = (report.recommended_revision || []).map(r => `<li>${r}</li>`).join("");
  }
}

// ---------------------------------------------------------------------------
// 7. Event Listeners & Actions
// ---------------------------------------------------------------------------

// Setup Form: Start Learning
const setupForm = document.getElementById("setup-form");
const subjectSelect = document.getElementById("input-subject-select");
const customSubjectWrapper = document.getElementById("custom-subject-wrapper");
const customSubjectInput = document.getElementById("input-custom-subject");

// Toggle custom subject input when selected
if (subjectSelect && customSubjectWrapper) {
  subjectSelect.addEventListener("change", () => {
    if (subjectSelect.value === "__custom__") {
      customSubjectWrapper.style.display = "block";
      if (customSubjectInput) customSubjectInput.focus();
    } else {
      customSubjectWrapper.style.display = "none";
    }
  });
}

if (setupForm) {
  setupForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const startBtn = document.getElementById("start-btn");
    startBtn.disabled = true;
    startBtn.textContent = "Starting Session...";

    hasReviewedDiagnosticResults = false;
    currentPlan = [];
    updateHistoryUI();

    let chosenSubject = "Operating Systems";
    if (subjectSelect) {
      if (subjectSelect.value === "__custom__" && customSubjectInput && customSubjectInput.value.trim()) {
        chosenSubject = customSubjectInput.value.trim();
      } else {
        chosenSubject = subjectSelect.value || "Operating Systems";
      }
    }

    const payload = {
      name: document.getElementById("input-name")?.value.trim() || "Himaja",
      subject: chosenSubject,
      level: document.getElementById("input-level")?.value || "Beginner",
      goal: document.getElementById("input-goal")?.value.trim() || "Semester Exam Prep",
      available_time: "Self-paced",
      max_quiz_attempts: parseInt(document.getElementById("input-attempts")?.value, 10) || 2,
      topics: []
    };

    try {
      const res = await fetch("/api/session/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (!res.ok) {
        throw new Error(`Server returned HTTP ${res.status}`);
      }
      const data = await res.json();
      currentThreadId = data.thread_id;
      sessionStatusText.textContent = `Session: #${currentThreadId}`;
      handleGraphState(data);
    } catch (err) {
      alert("Failed to start session: " + err.message);
    } finally {
      startBtn.disabled = false;
      startBtn.textContent = "Start Learning";
    }
  });
}

// Diagnostic Form Submit
const diagnosticForm = document.getElementById("diagnostic-form");
if (diagnosticForm) {
  diagnosticForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const btn = document.getElementById("btn-submit-diagnostic");
    btn.disabled = true;
    btn.textContent = "Analyzing Answers...";

    const questions = currentInterrupt?.questions || [];
    const selectedAnswers = [];
    let unselectedIndex = -1;

    questions.forEach((q, idx) => {
      const checked = document.querySelector(`input[name="diag_q_${idx}"]:checked`);
      if (!checked && unselectedIndex === -1) {
        unselectedIndex = idx;
      }
      selectedAnswers.push(checked ? parseInt(checked.value, 10) : -1);
    });

    if (unselectedIndex !== -1) {
      alert(`Please select an answer for Question ${unselectedIndex + 1} before submitting.`);
      btn.disabled = false;
      btn.textContent = "Submit & Create My Plan";
      return;
    }

    try {
      const res = await fetch(`/api/session/${currentThreadId}/resume`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume_payload: { answers: selectedAnswers } })
      });
      const data = await res.json();
      // REQUIREMENT 2: Show Diagnostic Assessment Strengths & Weaknesses FIRST!
      hasReviewedDiagnosticResults = false;
      handleGraphState(data);
    } catch (err) {
      alert("Error submitting diagnostic: " + err.message);
    } finally {
      btn.disabled = false;
      btn.textContent = "Submit & Create My Plan";
    }
  });
}

// Proceed from Diagnostic Results to Plan Customizer
const btnProceedToPlan = document.getElementById("btn-proceed-to-plan");
if (btnProceedToPlan) {
  btnProceedToPlan.addEventListener("click", () => {
    hasReviewedDiagnosticResults = true;
    updateStepper(3);
    renderPlanReview(currentInterrupt, currentGraphState.values);
  });
}

// Add Topic in Plan Customizer
const btnAddTopic = document.getElementById("btn-add-topic");
const inputNewTopic = document.getElementById("input-new-topic");

if (btnAddTopic && inputNewTopic) {
  btnAddTopic.addEventListener("click", () => {
    const val = inputNewTopic.value.trim();
    if (val) {
      currentPlan.push(val);
      inputNewTopic.value = "";
      renderInteractivePlanList();
      updateSidebar();
    }
  });

  inputNewTopic.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      btnAddTopic.click();
    }
  });
}

// Approve Plan & Begin Lessons
const btnApprovePlan = document.getElementById("btn-approve-plan");
if (btnApprovePlan) {
  btnApprovePlan.addEventListener("click", async () => {
    btnApprovePlan.disabled = true;
    btnApprovePlan.textContent = "Launching Lessons...";

    try {
      const res = await fetch(`/api/session/${currentThreadId}/resume`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          resume_payload: {
            approved: true,
            modified_plan: currentPlan
          }
        })
      });
      const data = await res.json();
      handleGraphState(data);
    } catch (err) {
      alert("Error approving plan: " + err.message);
    } finally {
      btnApprovePlan.disabled = false;
      btnApprovePlan.textContent = "Approve Plan & Start Lessons";
    }
  });
}

// Proceed to Quiz from Lesson
const btnGotoQuiz = document.getElementById("btn-goto-quiz");
if (btnGotoQuiz) {
  btnGotoQuiz.addEventListener("click", () => {
    renderQuiz();
  });
}

// Submit Topic Quiz Answers
const quizForm = document.getElementById("quiz-form");
if (quizForm) {
  quizForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const submitBtn = document.getElementById("btn-submit-quiz");
    submitBtn.disabled = true;
    submitBtn.textContent = "Grading Answers...";

    const questions = currentInterrupt?.questions || [];
    const selectedAnswers = [];
    let unselectedIndex = -1;

    questions.forEach((q, idx) => {
      const checked = document.querySelector(`input[name="quiz_q_${idx}"]:checked`);
      if (!checked && unselectedIndex === -1) {
        unselectedIndex = idx;
      }
      selectedAnswers.push(checked ? parseInt(checked.value, 10) : -1);
    });

    if (unselectedIndex !== -1) {
      alert(`Please select an answer for Question ${unselectedIndex + 1} before submitting.`);
      submitBtn.disabled = false;
      submitBtn.textContent = "Submit Answers";
      return;
    }

    try {
      const res = await fetch(`/api/session/${currentThreadId}/resume`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume_payload: { answers: selectedAnswers } })
      });
      const data = await res.json();
      currentGraphState = data;
      currentInterrupt = data.current_interrupt;
      updateSidebar();

      const lastRes = data.values?.last_quiz_result;
      renderQuizResult(lastRes, data.values);
    } catch (err) {
      alert("Error grading quiz: " + err.message);
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = "Submit Answers";
    }
  });
}

// Continue Workflow After Quiz Result
const btnContinue = document.getElementById("btn-continue-workflow");
if (btnContinue) {
  btnContinue.addEventListener("click", () => {
    if (currentGraphState) {
      handleGraphState(currentGraphState);
    }
  });
}

// Restart
const btnRestart = document.getElementById("btn-restart-session");
if (btnRestart) {
  btnRestart.addEventListener("click", () => {
    currentThreadId = null;
    currentGraphState = null;
    currentInterrupt = null;
    currentPlan = [];
    hasReviewedDiagnosticResults = false;
    updateHistoryUI();
    sessionStatusText.textContent = "Ready to Learn";
    showStage(stageSetup);
    updateStepper(1);
  });
}

// Download Study Notes & Final Report
const btnDownloadFinalTxt = document.getElementById("btn-download-final-txt");
const btnDownloadFinalDocx = document.getElementById("btn-download-final-docx");

if (btnDownloadFinalTxt) {
  btnDownloadFinalTxt.addEventListener("click", () => downloadNotesFormat("txt"));
}

if (btnDownloadFinalDocx) {
  btnDownloadFinalDocx.addEventListener("click", () => downloadNotesFormat("docx"));
}

// Initial UI sync for saved history & theme
updateHistoryUI();
