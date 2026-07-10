// ======================================================
// LaundryBot V7 Enterprise
// AI Chat Javascript
// Enterprise V2
// ======================================================

const chatBox = document.getElementById("chat-box");
const questionBox = document.getElementById("question");


// ======================================================
// History
// ======================================================

function saveHistory() {

    localStorage.setItem(
        "laundrybot_chat",
        chatBox.innerHTML
    );

}

function loadHistory() {

    const history = localStorage.getItem(
        "laundrybot_chat"
    );

    if (history) {

        chatBox.innerHTML = history;

        scrollBottom();

    }

}

function clearHistory() {

    if (!confirm("ต้องการล้างประวัติการสนทนา ?"))
        return;

    localStorage.removeItem("laundrybot_chat");

    chatBox.innerHTML = "";

}


// ======================================================
// Scroll
// ======================================================

function scrollBottom() {

    chatBox.scrollTop = chatBox.scrollHeight;

}


// ======================================================
// Escape HTML
// ======================================================

function escapeHtml(text) {

    return String(text ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");

}


// ======================================================
// Copy
// ======================================================

async function copyAnswer(text) {

    try {

        await navigator.clipboard.writeText(text);

        alert("✅ คัดลอกคำตอบแล้ว");

    }

    catch {

        alert("❌ ไม่สามารถคัดลอกได้");

    }

}


// ======================================================
// User Message
// ======================================================

function addUser(message) {

    chatBox.insertAdjacentHTML(

        "beforeend",

`
<div class="user-message">

    <div class="user-bubble">

        ${escapeHtml(message)}

    </div>

</div>
`

    );

    saveHistory();

    scrollBottom();

}


// ======================================================
// Citation
// ======================================================

function buildCitation(sources = []) {

    if (!Array.isArray(sources) || sources.length === 0)
        return "";

    const unique = [];

    const seen = new Set();

    sources.forEach(src => {

        const key = `${src.filename}-${src.page}`;

        if (!seen.has(key)) {

            seen.add(key);

            unique.push(src);

        }

    });

    let html = `

<hr>

<div class="citation mt-3">

<div class="fw-bold mb-3">

📄 เอกสารอ้างอิง (${unique.length})

</div>

`;

    unique.forEach(src => {

        const filename = escapeHtml(src.filename);

        const page = src.page || 1;

        const score = src.score
            ? `<span class="badge bg-success ms-2">Score ${src.score}</span>`
            : "";

        html += `

<div class="card mb-2 shadow-sm">

<div class="card-body">

<div class="fw-semibold">

${filename}

${score}

</div>

<div class="text-muted">

Page ${page}

</div>

<div class="mt-2">

<a

class="btn btn-sm btn-primary"

target="_blank"

href="/documents/viewer?file=${encodeURIComponent(filename)}&page=${page}">

📄 เปิด PDF

</a>

</div>

</div>

</div>

`;

    });

    html += "</div>";

    return html;

}


// ======================================================
// AI Message
// ======================================================

function addAI(answer, sources = []) {

    const id = "copy_" + Date.now();

    chatBox.insertAdjacentHTML(

        "beforeend",

`
<div class="ai-message">

<div class="ai-bubble">

<div class="fw-bold mb-2">

🤖 LaundryBot AI

</div>

<div>

${String(answer).replace(/\n/g, "<br>")}

</div>

<div class="mt-3">

<button

id="${id}"

class="btn btn-sm btn-outline-secondary">

📋 Copy

</button>

</div>

${buildCitation(sources)}

</div>

</div>
`

    );

    document
        .getElementById(id)
        .addEventListener(
            "click",
            () => copyAnswer(answer)
        );

    saveHistory();

    scrollBottom();

}


// ======================================================
// Loading
// ======================================================

function loading() {

    chatBox.insertAdjacentHTML(

        "beforeend",

`
<div

id="loading"

class="loading">

🤖 LaundryBot AI กำลังค้นหาข้อมูล...

</div>
`

    );

    scrollBottom();

}

function stopLoading() {

    document
        .getElementById("loading")
        ?.remove();

}


// ======================================================
// Ask AI
// ======================================================

async function askAI() {

    const question = questionBox.value.trim();

    if (!question)
        return;

    addUser(question);

    questionBox.value = "";

    questionBox.disabled = true;

    loading();

    try {

        const response = await fetch(

            "/ai/chat",

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    question

                })

            }

        );

        const result = await response.json();

        stopLoading();

        if (!response.ok) {

            throw new Error(

                result.message || "Server Error"

            );

        }

        addAI(

            result.answer,

            result.sources || []

        );

    }

    catch (err) {

        stopLoading();

        addAI(

            "❌ " + err.message,

            []

        );

    }

    finally {

        questionBox.disabled = false;

        questionBox.focus();

    }

}


// ======================================================
// Keyboard
// ======================================================

questionBox.addEventListener(

    "keydown",

    function (e) {

        if (e.key === "Enter" && !e.shiftKey) {

            e.preventDefault();

            askAI();

        }

    }

);


// ======================================================
// Start
// ======================================================

loadHistory();

questionBox.focus();