console.log("NEW SCRIPT LOADED");
// =========================
// Elements
// =========================

const uploadBtn = document.getElementById("uploadBtn");
const sendBtn = document.getElementById("sendBtn");
const summaryBtn = document.getElementById("summaryBtn");
let selectedDocuments = [];

const fileInput = document.getElementById("fileInput");
const uploadStatus = document.getElementById("uploadStatus");

const questionInput = document.getElementById("question");
const messages = document.getElementById("messages");

const retrievalStatus = document.getElementById("retrievalStatus");
const summaryStatus = document.getElementById("summaryStatus");
const learningStatus = document.getElementById("learningStatus");
const documentsList = document.getElementById("documentsList");


// =========================
// Add Chat Message
// =========================

function addMessage(text, type,sources=[]) {

    const wrapper = document.createElement("div");

    wrapper.className = type === "user"
        ? "message-row user-row"
        : "message-row";

    const avatar = document.createElement("div");

    avatar.className = type === "user"
        ? "avatar user-avatar"
        : "avatar ai-avatar";

    avatar.innerHTML = type === "user"
    ? "👤"
    : "🤖";

    const bubble = document.createElement("div");

    bubble.className = type === "user"
        ? "user-message"
        : "bot-message";

    if(type==="user"){

    bubble.innerHTML=`

        <div class="message-header">
            You
        </div>

        <div class="message-content">
            ${text}
        </div>

    `;

}else{

    bubble.innerHTML=`

        <div class="message-top">

            <div class="message-header">
                Multi-Agent Assistant
            </div>

            <button class="copy-btn">📋</button>

        </div>

        <div class="message-content markdown-body">
            ${marked.parse(text)}
        </div>
        ${sources.length > 0 ? `

<div class="sources">

    <h4>📚 Sources</h4>

    ${sources.map(source => `

        <div class="source-item">

            📄 ${source.file}
            &nbsp;&nbsp;
            Page ${source.page}

        </div>

    `).join("")}

</div>

` : ""}

    `;

}

    if(type === "user"){

        wrapper.appendChild(bubble);
        wrapper.appendChild(avatar);

    }

    else{

        wrapper.appendChild(avatar);
        wrapper.appendChild(bubble);

    }

    if(type==="bot"){

    const copyBtn = bubble.querySelector(".copy-btn");

    copyBtn.addEventListener("click",()=>{

        navigator.clipboard.writeText(text);

        copyBtn.textContent="✅";

        setTimeout(()=>{

            copyBtn.textContent="📋";

        },1500);

    });

}

    messages.appendChild(wrapper);

    messages.scrollTop = messages.scrollHeight;

}
function showThinking(){

    const wrapper = document.createElement("div");

    wrapper.className = "message-row";

    wrapper.id = "thinking";

    wrapper.innerHTML = `
        <div class="avatar ai-avatar">🤖</div>

        <div class="bot-message">

            <div class="message-header">
                Multi-Agent Assistant
            </div>

            <div class="typing">

                <span></span>
                <span></span>
                <span></span>

            </div>

        </div>
    `;

    messages.appendChild(wrapper);

    messages.scrollTop = messages.scrollHeight;

}
function removeThinking(){

    const thinking = document.getElementById("thinking");

    if(thinking){

        thinking.remove();

    }

}

// =========================
// Update Agent Status
// =========================

function setStatus(retrieval, summary, learning){

    updateAgent(retrievalStatus, retrieval);

    updateAgent(summaryStatus, summary);

    updateAgent(learningStatus, learning);

}
function updateAgent(element, status){

    element.textContent = status;

    element.classList.remove(
        "status-idle",
        "status-working",
        "status-completed"
    );

    if(status === "Idle"){

        element.classList.add("status-idle");

    }

    else if(
        status.includes("Searching") ||
        status.includes("Summarizing") ||
        status.includes("Learning") ||
        status === "Working..."
    ){

        element.classList.add("status-working");

    }

    else{

        element.classList.add("status-completed");

    }

}

// =========================
// Upload File
// =========================

uploadBtn.addEventListener("click", () => {

    fileInput.click();

});


fileInput.addEventListener("change", async () => {

    const file = fileInput.files[0];

    if(!file) return;

    const formData = new FormData();

    formData.append("file", file);

    uploadBtn.disabled = true;

    uploadBtn.textContent = "Uploading...";

    showUploadProgress(10);

    try{

        showUploadProgress(30);

        const response = await fetch("/upload",{

            method:"POST",

            body:formData

        });

        showUploadProgress(70);

        const data = await response.json();

        if(response.ok){

            showUploadProgress(100);

            showUploadSuccess(file.name);

            await loadDocuments();

            selectedDocuments=[file.name];
            // Automatically check the uploaded document
            document.querySelectorAll("#documentsList input").forEach(cb => {
                cb.checked = (cb.value === file.name);
            });
            

            addMessage(
                `✅ Document uploaded successfully.\n📄 Selected document: ${file.name}`,
                "bot"
            );

        }

        else{

            addMessage(
                data.detail || "Upload failed.",
                "bot"
            );

        }

    }

    catch(error){

        console.error(error);

        addMessage(
            "Server error while uploading.",
            "bot"
        );

    }

    uploadBtn.disabled = false;

    uploadBtn.textContent = "📤 Upload Document";

    fileInput.value = "";

});

// =========================
// Ask Question
// =========================

sendBtn.addEventListener("click", askQuestion);

questionInput.addEventListener("keypress",(e)=>{

    if(e.key==="Enter"){

        askQuestion();

    }

});

// =========================
// Main Function
// =========================

async function askQuestion(){

    const question = questionInput.value.trim();

    if(question === "") return;

    addMessage(question, "user");

    questionInput.value = "";

    showThinking();

    await sleep(2000);

    setStatus("🔄 Working...", "⏳ Waiting", "⏳ Waiting");

    try{

        // Retrieval Agent
        await sleep(700);

        setStatus("✅ Completed", "🔄 Working...", "⏳ Waiting");

        await sleep(700);

        setStatus("✅ Completed", "✅ Completed", "🔄 Working...");

        const response = await fetch("/ask", {
            
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question,
                documents: selectedDocuments
            })

            });

        if (!response.ok) {
            throw new Error("Server Error: " + response.status);
        }   
        const data = await response.json();

        setStatus("✅ Completed", "✅ Completed", "✅ Completed");

        removeThinking();

        addMessage(
            data.answer,
            "bot",
            data.sources || []
        );

        setTimeout(() => {

            setStatus("Idle", "Idle", "Idle");

        }, 2000);

    }

    catch(error){
        console.error(error);
        removeThinking();

        addMessage(
            error.toString(),
            "bot"
        );

        setStatus("Idle", "Idle", "Idle");

    }

}
// ==========================================
// Upload Progress Card
// ==========================================

function showUploadProgress(percent){

    uploadStatus.innerHTML = `

    <div class="upload-card">

        <h4>Uploading PDF...</h4>

        <div class="progress">

            <div
                class="progress-bar"
                style="width:${percent}%">
            </div>

        </div>

        <p>${percent}% completed</p>

    </div>

    `;

}

function showUploadSuccess(filename){

    uploadStatus.innerHTML = `

    <div class="upload-card">

        <h4>✅ Upload Successful</h4>

        <p>${filename}</p>

        <p>Document indexed successfully.</p>

    </div>

    `;

}


// =========================
// Delay Function
// =========================

function sleep(ms){

    return new Promise(resolve=>setTimeout(resolve,ms));

}
// ==========================================
// THEME TOGGLE
// ==========================================

const themeToggle = document.getElementById("themeToggle");

const savedTheme = localStorage.getItem("theme");

if(savedTheme === "light"){

    document.body.classList.add("light");

    themeToggle.textContent = "🌙";

}else{

    document.body.classList.remove("light");

    themeToggle.textContent = "☀️";

}

themeToggle.addEventListener("click", () => {

    document.body.classList.toggle("light");

    if(document.body.classList.contains("light")){

        localStorage.setItem("theme","light");

        themeToggle.textContent = "🌙";

    }else{

        localStorage.setItem("theme","dark");

        themeToggle.textContent = "☀️";

    }

});
// =========================
// Summarize Paper
// =========================

summaryBtn.addEventListener("click", async () => {

    addMessage("📄 Generating summary of the uploaded paper...", "bot");

    try {

        const response = await fetch("/summarize");

        const data = await response.json();

        addMessage(data.summary, "bot");

    }

    catch (error) {

        addMessage(
            "❌ Unable to generate summary.",
            "bot"
        );

    }

});
async function loadDocuments() {

    const response = await fetch("/documents");
    const data = await response.json();

    documentsList.innerHTML = "";

    data.documents.forEach(doc => {

        const item = document.createElement("div");

        item.innerHTML = `
            <label>
                <input type="checkbox" value="${doc}">
                ${doc}
            </label>
        `;

        const checkbox = item.querySelector("input");

        checkbox.addEventListener("change", () => {

            // Clear previous selections
            selectedDocuments = [];

            // Collect all checked documents
            document
                .querySelectorAll("#documentsList input:checked")
                .forEach(cb => {
                    selectedDocuments.push(cb.value);
                });

            console.log( selectedDocuments);

            addMessage(
                "📄 Selected documents:<br>" +
                selectedDocuments.join("<br>"),
                "bot"
            );

        });

        documentsList.appendChild(item);

    });

}
loadDocuments();