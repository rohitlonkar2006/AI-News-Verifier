
const urlTab = document.getElementById("urlTab");
const manualTab = document.getElementById("manualTab");
const urlPanel = document.getElementById("urlPanel");
const manualPanel = document.getElementById("manualPanel");

const urlInput = document.getElementById("urlInput");
const titleInput = document.getElementById("titleInput");
const articleInput = document.getElementById("articleInput");

const analyzeBtn = document.getElementById("analyzeBtn");
const manualBtn = document.getElementById("manualBtn");

const skeleton = document.getElementById("skeleton");
const result = document.getElementById("result");
const toastContainer = document.getElementById("toastContainer");
const loadingOverlay = document.getElementById("loadingOverlay");
const loadingStatus = document.getElementById("loadingStatus");
const loadingBar = document.getElementById("loadingBar");

const characterCount = document.getElementById("characterCount");

if (loadingOverlay) loadingOverlay.classList.add("hidden");
if (skeleton) skeleton.classList.add("hidden");


function toast(message, type = "success") {
    if (!toastContainer) return;

    const div = document.createElement("div");
    div.className = `toast ${type}`;
    
    const iconSvg = type === "error" 
        ? `<svg width="18" height="18" fill="none" stroke="#ef4444" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>`
        : `<svg width="18" height="18" fill="none" stroke="#10b981" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`;

    div.innerHTML = `${iconSvg}<span>${message}</span>`;
    toastContainer.appendChild(div);

    requestAnimationFrame(() => {
        div.classList.add("reveal");
    });

    setTimeout(() => {
        div.classList.remove("reveal");
        div.style.transform = "translateX(100px) scale(0.9)";
        div.style.opacity = "0";
        
        setTimeout(() => { 
            div.remove(); 
        }, 400);
    }, 3500);
}


const steps = [
    "Fetching payload...",
    "Parsing text arrays...",
    "Running Deep Learning Core...",
    "Analyzing Patterns...",
    "Finalizing dashboard view..."
];
let loadingTimer;

function showLoading() {
    if (loadingOverlay) loadingOverlay.classList.remove("hidden");
    if (skeleton) skeleton.classList.add("hidden");
    if (result) result.classList.add("hidden");

    let i = 0;
    if (loadingBar) loadingBar.style.width = "5%";
    if (loadingStatus) loadingStatus.innerHTML = steps[0];

    loadingTimer = setInterval(() => {
        i++;
        if (i >= steps.length) {
            clearInterval(loadingTimer);
            return;
        }
        if (loadingStatus) loadingStatus.innerHTML = steps[i];
        if (loadingBar) loadingBar.style.width = ((i + 1) / steps.length * 100) + "%";
    }, 600);
}

function hideLoading() {
    clearInterval(loadingTimer);
    if (loadingOverlay) loadingOverlay.classList.add("hidden");
    if (skeleton) skeleton.classList.add("hidden");
}


urlTab.onclick = () => {
    urlTab.classList.add("active");
    manualTab.classList.remove("active");
    urlPanel.classList.add("active");
    manualPanel.classList.remove("active");
};

manualTab.onclick = () => {
    manualTab.classList.add("active");
    urlTab.classList.remove("active");
    manualPanel.classList.add("active");
    urlPanel.classList.remove("active");
};

articleInput.addEventListener("input", () => {
    characterCount.innerText = `${articleInput.value.length} Characters`;
});

function chip(wordObj, type) {
    const literalWord = typeof wordObj === 'object' ? (wordObj.word || "") : wordObj;
    return `<span class="${type}">${literalWord}</span>`;
}


function render(data) {
    try {
        document.getElementById("newsTitle").innerText = data.title || "Untitled Extraction";
        document.getElementById("summary").innerText = data.summary || "No summary compiled.";
        document.getElementById("threshold").innerText = data.threshold !== undefined ? data.threshold : "0.53";

        const badge = document.getElementById("predictionBadge");
        const classification = (data.prediction || "FAKE").toUpperCase();
        badge.innerText = classification;
        badge.className = classification === "REAL" ? "badge real" : "badge fake";

        const gauge = document.getElementById("gaugeProgress");
        if (gauge) {
            gauge.style.stroke = classification === "REAL" ? "#10b981" : "#ef4444";
        }

        const reasonList = document.getElementById("reasons");
        reasonList.innerHTML = "";
        if (data.reasons && Array.isArray(data.reasons)) {
            data.reasons.forEach(reason => {
                const li = document.createElement("li");
                li.innerText = reason;
                reasonList.appendChild(li);
            });
        }

        document.getElementById("positiveWords").innerHTML = (data.supporting_words || [])
            .map(x => chip(x, "positive")).join("");

        document.getElementById("negativeWords").innerHTML = (data.opposing_words || [])
            .map(x => chip(x, "negative")).join("");

        let articleHtml = data.article || "";
        if (data.highlight_phrases && Array.isArray(data.highlight_phrases)) {
            data.highlight_phrases.forEach(p => {
                if (!p || typeof p !== "string") return;
                const escaped = p.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
                articleHtml = articleHtml.replace(
                    new RegExp(escaped, "gi"),
                    `<mark>${p}</mark>`
                );
            });
        }
        document.getElementById("article").innerHTML = articleHtml;

        const confidenceVal = parseFloat(data.confidence) || 0;
        const realVal = parseFloat(data.real_probability) || 0;
        const fakeVal = parseFloat(data.fake_probability) || 0;

        animateNumber("gaugeValue", confidenceVal);
        animateGauge(confidenceVal);
        animateBars(realVal, fakeVal);
        animateNumber("realPercent", realVal);
        animateNumber("fakePercent", fakeVal);

        result.classList.remove("hidden");
        result.classList.add("fade-in");
    } catch (renderError) {
        console.error("Dashboard Render Interface Error:", renderError);
        toast("Failed to parse the processed data structure cleanly.", "error");
    }
}

async function request(endpoint, payload) {
    showLoading();
    try {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();

        if (!data.success) {
            hideLoading();
            toast(data.message || "An operational processing error occurred.", "error");
            return;
        }
        
        render(data);
        hideLoading(); 
    } catch (err) {
        hideLoading();
        toast("Server communication broken.", "error");
        console.error("Transmission Error Context:", err);
    }
}

analyzeBtn.onclick = () => {
    const urlValue = urlInput.value.trim();

    if (urlValue === "") {
        toast("Enter URL", "error");
        return;
    }

    const urlPattern = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/i;
    
    if (!urlPattern.test(urlValue)) {
        toast("Please provide a valid URL address format.", "error");
        return;
    }

    request("/extract", { url: urlValue });
};

manualBtn.onclick = () => {
    if (titleInput.value.trim() === "" || articleInput.value.trim() === "") {
        toast("Fill all fields.", "error");
        return;
    }
    request("/predict_manual", {
        title: titleInput.value.trim(),
        article: articleInput.value.trim()
    });
};

document.getElementById("copyBtn").onclick = function(e) {
    const text = document.getElementById("article").innerText;
    const copyButton = document.getElementById("copyBtn");
    
    navigator.clipboard.writeText(text).then(() => {
        const existingBadge = document.querySelector(".copy-alert-badge");
        if (existingBadge) existingBadge.remove();

        const badge = document.createElement("div");
        badge.className = "copy-alert-badge";
        badge.innerText = "Copied to Clipboard!";
        
        copyButton.parentElement.appendChild(badge);
        badge.style.right = "0px";

        requestAnimationFrame(() => {
            badge.classList.add("show");
        });

        setTimeout(() => {
            badge.classList.remove("show");
            badge.style.transform = "translateY(-45px) scale(0.9)";
            badge.style.opacity = "0";
            
            setTimeout(() => { badge.remove(); }, 400);
        }, 2000);

    }).catch((err) => {
        toast("Copy execution failed.", "error");
        console.error("Clipboard Copy Error:", err);
    });
};

function animateNumber(id, value, suffix = "%") {
    const element = document.getElementById(id);
    if (!element) return;
    
    const targetValue = parseFloat(value);
    if (isNaN(targetValue)) {
        element.innerHTML = value + suffix;
        return;
    }

    let start = 0;
    const duration = 1200;
    const step = targetValue / (duration / 16);

    const interval = setInterval(() => {
        start += step;
        if (start >= targetValue) {
            start = targetValue;
            clearInterval(interval);
        }
        element.innerHTML = start.toFixed(1) + suffix;
    }, 16);
}

function animateGauge(confidence) {
    const circle = document.getElementById("gaugeProgress");
    if (!circle) return;
    const targetValue = parseFloat(confidence) || 0;
    const radius = 92;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (targetValue / 100 * circumference);
    circle.style.strokeDashoffset = offset;
}

function animateBars(real, fake) {
    setTimeout(() => {
        const realBar = document.getElementById("realBar");
        const fakeBar = document.getElementById("fakeBar");
        const cleanReal = parseFloat(real) || 0;
        const cleanFake = parseFloat(fake) || 0;
        if (realBar) realBar.style.width = cleanReal + "%";
        if (fakeBar) fakeBar.style.width = cleanFake + "%";
    }, 300);
}