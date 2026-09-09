/**
 * Frontend Logic for AI Career Assistant
 * Updated:
 * 1. Prominent explicit percentage display for 5-Roles (no missing numbers).
 * 2. Full comparison scores for ALL mock JDs with category filtering.
 * 3. Top 3 Job recommendation highlights.
 * 4. Custom JD direct comparison view.
 */

document.addEventListener("DOMContentLoaded", () => {
    // Mode tabs
    const tabStandard = document.getElementById("tabStandard");
    const tabCustomJD = document.getElementById("tabCustomJD");
    const customJDSection = document.getElementById("customJDSection");
    const customJDInput = document.getElementById("customJDInput");
    const btnText = document.getElementById("btnText");

    // Stepper elements
    const step3Title = document.getElementById("step3Title");
    const step3Desc = document.getElementById("step3Desc");
    const step4Title = document.getElementById("step4Title");
    const step4Desc = document.getElementById("step4Desc");

    // File inputs
    const dropzone = document.getElementById("dropzone");
    const resumeInput = document.getElementById("resumeInput");
    const browseBtn = document.getElementById("browseBtn");
    const selectedFileName = document.getElementById("selectedFileName");
    const fileNameText = selectedFileName.querySelector(".file-name-text");
    const removeFileBtn = document.getElementById("removeFileBtn");
    const analyzeBtn = document.getElementById("analyzeBtn");

    // Sections
    const processingSection = document.getElementById("processingSection");
    const resultsSection = document.getElementById("resultsSection");
    const standardResultsView = document.getElementById("standardResultsView");
    const customJDResultsView = document.getElementById("customJDResultsView");

    // Role filter select
    const roleFilter = document.getElementById("roleFilter");

    let currentMode = "standard";
    let currentFile = null;
    let allComparedJobsCache = [];

    // --- Mode Tab Switching ---
    tabStandard.addEventListener("click", () => {
        currentMode = "standard";
        tabStandard.classList.add("active");
        tabCustomJD.classList.remove("active");
        customJDSection.classList.add("hidden");
        btnText.textContent = "Analyze Resume & Compare All JDs";

        step3Title.textContent = "Evaluating 5 Industry Roles";
        step3Desc.textContent = "PromptTemplate | ChatModel Runnable Chain";
        step4Title.textContent = "LangChain FAISS Vector Search";
        step4Desc.textContent = "Comparing similarity across every mock JD";

        validateCanSubmit();
    });

    tabCustomJD.addEventListener("click", () => {
        currentMode = "custom";
        tabCustomJD.classList.add("active");
        tabStandard.classList.remove("active");
        customJDSection.classList.remove("hidden");
        btnText.textContent = "Compare Resume Against Target JD";

        step3Title.textContent = "LangChain FAISS Vector Embedding";
        step3Desc.textContent = "Inbuilt similarity search with Gemini Embeddings";
        step4Title.textContent = "Skill Gap & Match Deep Analysis";
        step4Desc.textContent = "Evaluating alignment, missing skills & advice";

        validateCanSubmit();
    });

    customJDInput.addEventListener("input", () => {
        validateCanSubmit();
    });

    // Filter for All JDs table
    roleFilter.addEventListener("change", () => {
        renderAllJdsGrid(allComparedJobsCache, roleFilter.value);
    });

    // --- File Drag & Drop ---
    browseBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        resumeInput.click();
    });

    dropzone.addEventListener("click", () => {
        resumeInput.click();
    });

    ["dragenter", "dragover"].forEach(name => {
        dropzone.addEventListener(name, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.add("drag-over");
        });
    });

    ["dragleave", "drop"].forEach(name => {
        dropzone.addEventListener(name, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.remove("drag-over");
        });
    });

    dropzone.addEventListener("drop", (e) => {
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            handleFileSelection(e.dataTransfer.files[0]);
        }
    });

    resumeInput.addEventListener("change", (e) => {
        if (e.target.files && e.target.files.length > 0) {
            handleFileSelection(e.target.files[0]);
        }
    });

    removeFileBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        clearFile();
    });

    function handleFileSelection(file) {
        currentFile = file;
        fileNameText.textContent = `${file.name} (${(file.size / (1024 * 1024)).toFixed(2)} MB)`;
        selectedFileName.classList.remove("hidden");
        validateCanSubmit();
    }

    function clearFile() {
        currentFile = null;
        resumeInput.value = "";
        selectedFileName.classList.add("hidden");
        validateCanSubmit();
    }

    function validateCanSubmit() {
        if (!currentFile) {
            analyzeBtn.disabled = true;
            return;
        }
        if (currentMode === "custom" && (!customJDInput.value || customJDInput.value.trim().length < 20)) {
            analyzeBtn.disabled = true;
            return;
        }
        analyzeBtn.disabled = false;
    }

    // --- Stepper Helper ---
    function setStep(stepNum) {
        for (let i = 1; i <= 4; i++) {
            const el = document.getElementById(`step${i}`);
            if (i < stepNum) {
                el.className = "step-item done";
            } else if (i === stepNum) {
                el.className = "step-item active";
            } else {
                el.className = "step-item";
            }
        }
    }

    // --- Submit Analysis ---
    analyzeBtn.addEventListener("click", async () => {
        if (!currentFile) return;

        analyzeBtn.disabled = true;
        processingSection.classList.remove("hidden");
        resultsSection.classList.add("hidden");
        setStep(1);

        const t1 = setTimeout(() => setStep(2), 1200);
        const t2 = setTimeout(() => setStep(3), 2800);
        const t3 = setTimeout(() => setStep(4), 5000);

        const formData = new FormData();
        formData.append("file", currentFile);

        if (currentMode === "custom" && customJDInput.value.trim()) {
            formData.append("custom_jd", customJDInput.value.trim());
        }

        try {
            const response = await fetch("/api/analyze", {
                method: "POST",
                body: formData
            });

            clearTimeout(t1);
            clearTimeout(t2);
            clearTimeout(t3);
            setStep(4);

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(data.error || "Failed to analyze resume.");
            }

            renderCandidateHeader(data.candidate || {});

            if (data.mode === "custom_jd") {
                renderCustomJDResults(data.custom_jd_analysis || {});
                standardResultsView.classList.add("hidden");
                customJDResultsView.classList.remove("hidden");
            } else {
                renderStandardResults(data);
                customJDResultsView.classList.add("hidden");
                standardResultsView.classList.remove("hidden");
            }

            processingSection.classList.add("hidden");
            resultsSection.classList.remove("hidden");
            resultsSection.scrollIntoView({ behavior: "smooth" });

        } catch (err) {
            alert("Error: " + err.message);
            processingSection.classList.add("hidden");
        } finally {
            validateCanSubmit();
        }
    });

    // --- Renderers ---
    function renderCandidateHeader(candidate) {
        const name = candidate.candidate_name || "Candidate";
        document.getElementById("candidateName").textContent = name;

        const initials = name.split(" ").map(w => w[0]).join("").toUpperCase().slice(0, 2) || "CA";
        document.getElementById("candidateAvatar").textContent = initials;

        const email = candidate.email || "Not specified";
        const phone = candidate.phone || "";
        document.getElementById("candidateContact").textContent = phone ? `${email} • ${phone}` : email;
        document.getElementById("candidateExp").textContent = candidate.total_experience_years || "0";
        document.getElementById("candidateSummary").textContent = candidate.summary || "No summary available.";

        const skillsContainer = document.getElementById("candidateSkills");
        skillsContainer.innerHTML = "";
        (candidate.skills || []).forEach(skill => {
            const span = document.createElement("span");
            span.className = "skill-pill";
            span.textContent = skill;
            skillsContainer.appendChild(span);
        });
    }

    function renderStandardResults(data) {
        // 1. 5 Roles Cards with Explicit Percentage
        const rolesGrid = document.getElementById("rolesGrid");
        rolesGrid.innerHTML = "";
        (data.role_scores || []).forEach(item => {
            const pct = parseInt(item.match_percentage) || 50;
            let scoreClass = "score-med";
            if (pct >= 70) scoreClass = "score-high";
            else if (pct < 45) scoreClass = "score-low";

            const card = document.createElement("div");
            card.className = `role-card ${scoreClass}`;
            card.innerHTML = `
                <div class="role-title">${item.role}</div>
                <div class="role-percentage-badge">
                    <span class="role-percentage-label">Match Score</span>
                    <span class="role-percentage-value">${pct}<span class="pct-symbol">%</span></span>
                </div>
                <div class="score-bar-bg">
                    <div class="score-bar-fill" style="width: ${pct}%"></div>
                </div>
                <div class="role-rationale">${item.rationale || ""}</div>
            `;
            rolesGrid.appendChild(card);
        });

        // 2. Top 3 Recommended Jobs
        const topJobsGrid = document.getElementById("topJobsGrid");
        topJobsGrid.innerHTML = "";
        (data.top_recommended_jobs || []).forEach(job => {
            const matchedPills = (job.matched_skills || [])
                .map(s => `<span class="matched-pill">${s}</span>`)
                .join("");

            const card = document.createElement("div");
            card.className = "job-card";
            card.innerHTML = `
                <div class="job-rank-badge">#${job.rank} Match</div>
                <h4 class="job-title">${job.title}</h4>
                <div class="job-company">${job.company} • ${job.location || "Remote"}</div>
                <div class="job-match-pill">
                    🎯 ${job.match_score}% Profile Match
                </div>
                <p class="job-description">${job.description}</p>
                <div class="job-skills-matched">
                    <span class="matched-skills-label">Matched Skills:</span>
                    <div class="matched-pill-list">
                        ${matchedPills || '<span class="matched-pill">Foundational alignment</span>'}
                    </div>
                </div>
            `;
            topJobsGrid.appendChild(card);
        });

        // 3. Cache and Render ALL Compared Jobs
        allComparedJobsCache = data.all_compared_jobs || [];
        roleFilter.value = "ALL";
        renderAllJdsGrid(allComparedJobsCache, "ALL");
    }

    function renderAllJdsGrid(jobs, filterRole) {
        const allJdsGrid = document.getElementById("allJdsGrid");
        allJdsGrid.innerHTML = "";

        const filtered = filterRole === "ALL" 
            ? jobs 
            : jobs.filter(j => j.role_category === filterRole);

        if (filtered.length === 0) {
            allJdsGrid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 24px;">No job descriptions found for category: ${filterRole}</div>`;
            return;
        }

        filtered.forEach(job => {
            const score = parseInt(job.match_score) || 50;
            let badgeClass = "badge-score-med";
            if (score >= 70) badgeClass = "badge-score-high";
            else if (score < 50) badgeClass = "badge-score-low";

            const item = document.createElement("div");
            item.className = "all-jd-item";
            item.innerHTML = `
                <div class="all-jd-top">
                    <h5 class="all-jd-title">${job.title}</h5>
                    <span class="all-jd-score-badge ${badgeClass}">${score}% Match</span>
                </div>
                <div class="all-jd-company">${job.company} • ${job.location || "Remote"}</div>
                <span class="all-jd-cat-tag">${job.role_category}</span>
                <div class="all-jd-skills-row">
                    ${(job.matched_skills || []).slice(0, 3).map(s => `<span class="all-jd-mini-pill">${s}</span>`).join("")}
                </div>
            `;
            allJdsGrid.appendChild(item);
        });
    }

    function renderCustomJDResults(analysis) {
        const score = analysis.match_percentage || 70;
        document.getElementById("customScoreNum").textContent = score;
        document.getElementById("customVerdictText").textContent = analysis.executive_verdict || "Assessment completed.";
        document.getElementById("semanticScoreVal").textContent = `${analysis.semantic_similarity_score || score}%`;

        // Matched Skills
        const matchedContainer = document.getElementById("customMatchedSkills");
        matchedContainer.innerHTML = "";
        (analysis.matched_skills || []).forEach(skill => {
            const pill = document.createElement("span");
            pill.className = "skill-pill";
            pill.textContent = skill;
            matchedContainer.appendChild(pill);
        });

        // Missing Skills
        const missingContainer = document.getElementById("customMissingSkills");
        missingContainer.innerHTML = "";
        (analysis.missing_skills || []).forEach(skill => {
            const pill = document.createElement("span");
            pill.className = "missing-pill";
            pill.textContent = skill;
            missingContainer.appendChild(pill);
        });

        // Strengths
        const strengthsList = document.getElementById("customStrengthsList");
        strengthsList.innerHTML = "";
        (analysis.strengths || []).forEach(item => {
            const li = document.createElement("li");
            li.textContent = item;
            strengthsList.appendChild(li);
        });

        // Gaps
        const gapsList = document.getElementById("customGapsList");
        gapsList.innerHTML = "";
        (analysis.gaps_and_recommendations || []).forEach(item => {
            const li = document.createElement("li");
            li.textContent = item;
            gapsList.appendChild(li);
        });
    }
});
