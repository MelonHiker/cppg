// Helper to switch between tab contents
document.querySelectorAll(".tab-button").forEach(btn => {
    btn.addEventListener("click", function () {
        const tab = this.getAttribute("data-tab");
        document.querySelectorAll(".tab-content").forEach(content => {
            content.classList.add("hidden");
        });
        document.getElementById(tab).classList.remove("hidden");
    });
});
  
// Generate Tutorial button handler
document.getElementById("generate-tutorial").addEventListener("click", async function () {
    // Read problem data from hidden JSON
    const problemData = JSON.parse(document.getElementById("problem-data").textContent);
    
    const button = this;
    button.disabled = true;
    button.textContent = "Generating...";
    
    try {
        const response = await fetch("/generate-tutorial", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(problemData)
        });
        const data = await response.json();
        if(data.error) {
            alert("Error: " + data.error);
        } else {
            document.getElementById("solution-explanation-edit").value = data.solution_explanation;
            document.getElementById("time-complexity-edit").value = data.time_complexity;
            document.getElementById("space-complexity-edit").value = data.space_complexity;
            document.querySelectorAll("textarea").forEach(t => t.dispatchEvent(new Event('input', { bubbles: true, cancelable: true })));
            renderContent();
        }
    } catch (error) {
        alert("Failed to generate solution:" + error.message);
    } finally {
        button.disabled = false;
        button.textContent = "Generate Solution";
    }
});

// Generate Solution button handler
document.getElementById("generate-solution").addEventListener("click", async function () {
    // Alert if tutorial-tab's solution-explanation is empty.
    const solutionExplanation = document.getElementById("solution-explanation-edit").value.trim();
    if (!solutionExplanation) {
        alert("Solution explanation in Tutorial cannot be empty.");
        return;
    }
    const button = this;
    const editor = document.getElementById("solution-editor");
    const language = document.getElementById("language-select").value;
    
    // Read problem data from hidden JSON
    const problemData = JSON.parse(document.getElementById("problem-data").textContent);
    
    button.disabled = true;
    button.textContent = "Generating...";
    
    try {
        const response = await fetch("/generate-solution", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ problem: problemData, language: language })
        });
        const data = await response.json();
        if(data.error) {
            alert("Error: " + data.error);
        } else {
            editor.value = data.solution;
        }
    } catch (error) {
        alert("Failed to generate solution:" + error.message);
    } finally {
        button.disabled = false;
        button.textContent = "Generate Solution";
    }
});
  
// Generate Test button handler
document.getElementById("generate-test").addEventListener("click", async function () {
    const button = this;
    const editor = document.getElementById("test-editor");

    // Read problem data from hidden JSON
    const problemData = JSON.parse(document.getElementById("problem-data").textContent);
    
    button.disabled = true;
    button.textContent = "Generating...";
    
    try {
        const response = await fetch("/generate-test", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(problemData)
        });
        const data = await response.json();
        if(data.error) {
            alert("Error: " + data.error);
        } else {
            editor.value = data.test_script;
        }
    } catch (error) {
        alert("Failed to generate test script:" + error.message);
    } finally {
        button.disabled = false;
        button.textContent = "Generate Test Script";
    }
});

// Debounce helper function.
function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

// Debounced renderContent function (adjust wait time as needed, e.g., 300ms)
const debouncedRenderContent = debounce(renderContent, 300);

// Attach input event listeners to elements in Statement and Tutorial tabs.
document.addEventListener("DOMContentLoaded", function() {
    // For Statement tab editable fields.
    const statementElements = [
        "title-edit",
        "time-limit-edit",
        "memory-limit-edit",
        "description-edit",
        "input-specifications-edit",
        "output-specifications-edit",
        "note-edit"
    ];
    statementElements.forEach(id => {
        const elem = document.getElementById(id);
        if(elem) {
            elem.addEventListener("input", debouncedRenderContent);
        }
    });

    // For examples
    document.querySelectorAll(".example-edit .example-pair").forEach(pair => {
        const inputArea = pair.querySelector(".example-input");
        const outputArea = pair.querySelector(".example-output");
        if (inputArea) {
            inputArea.addEventListener("input", debouncedRenderContent);
        }
        if (outputArea) {
            outputArea.addEventListener("input", debouncedRenderContent);
        }
    });
    
    // For Tutorial tab editable fields.
    const tutorialElements = [
        "solution-explanation-edit",
        "time-complexity-edit",
        "space-complexity-edit",
        "tags-edit"
    ];
    tutorialElements.forEach(id => {
        const elem = document.getElementById(id);
        if(elem) {
            elem.addEventListener("input", debouncedRenderContent);
        }
    });
});

// Provided markdown and LaTeX rendering functions
function parseMarkdown(text) {
    var scripts = text.match(/<script[^>]*>([\s\S]*?)<\/script>/gi);
    text = marked.parse(text);
    return text.replace(/<script[^>]*>([\s\S]*?)<\/script>/gi, m => scripts.shift());
}

function updateProblemData() {
    const problem = {};
    // Statement tab fields
    problem.title = document.getElementById("title-edit").value;
    problem.time_limit = document.getElementById("time-limit-edit").value;
    problem.memory_limit = document.getElementById("memory-limit-edit").value;
    problem.description = document.getElementById("description-edit").value;
    problem.input_specifications = document.getElementById("input-specifications-edit").value;
    problem.output_specifications = document.getElementById("output-specifications-edit").value;
    
    // Collect examples from the edit part
    problem.examples = [];
    document.querySelectorAll(".example-edit .example-pair").forEach(pair => {
        const inputArea = pair.querySelector(".example-input");
        const outputArea = pair.querySelector(".example-output");
        if (inputArea && outputArea) {
            problem.examples.push({
                input: inputArea.value,
                output: outputArea.value
            });
        }
    });
    
    problem.note = document.getElementById("note-edit").value;
    
    // Tutorial tab fields
    problem.solution_explanation = document.getElementById("solution-explanation-edit").value;
    problem.time_complexity = document.getElementById("time-complexity-edit").value;
    problem.space_complexity = document.getElementById("space-complexity-edit").value;
    problem.tags = document.getElementById("tags-edit").value;
    
    // Update hidden element with serialized JSON
    document.getElementById("problem-data").textContent = JSON.stringify(problem);
}

function renderContent() {
    const sections = [
        "title",
        "time-limit",
        "memory-limit",
        "description",
        "input-specifications",
        "output-specifications",
        "note",
        "solution-explanation",
        "time-complexity",
        "space-complexity"
    ];

    sections.forEach(id => {
        const previewDiv = document.getElementById(id + "-preview");
        const editElem = document.getElementById(id + "-edit");
        if (previewDiv && editElem) {
            previewDiv.innerHTML = parseMarkdown(editElem.value);
            if (typeof MathJax !== "undefined" && MathJax.Hub) {
                MathJax.Hub.Queue(["Typeset", MathJax.Hub, previewDiv]);
            }
        }
    });
    
    // Update examples
    const exampleInputs = document.querySelectorAll(".example-input");
    const exampleOutputs = document.querySelectorAll(".example-output");
    exampleInputs.forEach((textarea, index) => {
        const pre = document.querySelectorAll(".example-preview pre")[index * 2];
        pre.textContent = textarea.value;
    });
    exampleOutputs.forEach((textarea, index) => {
        const pre = document.querySelectorAll(".example-preview pre")[index * 2 + 1];
        pre.textContent = textarea.value;
    });

    // Update basic fields in Statement tab.
    document.getElementById("title-preview").textContent = document.getElementById("title-edit").value;
    document.getElementById("time-limit-preview").textContent = document.getElementById("time-limit-edit").value;
    document.getElementById("memory-limit-preview").textContent = document.getElementById("memory-limit-edit").value;
    
    // Update Tags.
    if(document.getElementById("tags-edit")) {
        document.getElementById("tags-preview").textContent = document.getElementById("tags-edit").value;
    }
    
    // Finally update the hidden JSON data
    updateProblemData();
}

// Optionally call renderContent() on window load.
window.addEventListener("load", renderContent);

// Handle font size slider
document.querySelector("#solution #font-size-slider").addEventListener("input", (e) => {
    document.getElementById("solution-editor").style.fontSize = `${e.target.value}px`;
});
document.querySelector("#test #font-size-slider").addEventListener("input", (e) => {
    document.getElementById("test-editor").style.fontSize = `${e.target.value}px`;
});

document.getElementById("run-solution").addEventListener("click", async function () {
    const editor = document.getElementById("solution-editor");
    const language = document.getElementById("language-select").value;
    const stdinInput = document.getElementById("execution-stdin").value;
    const outputElem = document.getElementById("execution-output");

    this.disabled = true;
    this.textContent = "Running...";
    try {
        const response = await fetch("/run-solution", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                code: editor.value,
                language: language,
                stdin_input: stdinInput
            })
        });
        const data = await response.json();
        outputElem.value = data.error_message ? data.error_message : data.execution_output;
    } catch (error) {
        outputElem.value = "Error: " + error.message;
    } finally {
        this.disabled = false;
        this.textContent = "Run";
    }
});

// New run-test button handler for Test Tab multiple file generation
document.getElementById("run-test").addEventListener("click", async function () {
    const code = document.getElementById("test-editor").value;
    const filenameBase = document.getElementById("filename-input").value.trim();
    const startIndex = Number(document.getElementById("start-index").value);
    const endIndex = Number(document.getElementById("end-index").value);
    const filesContainer = document.getElementById("files-container");
    filesContainer.innerHTML = ""; // clear previous files

    if (!filenameBase || isNaN(startIndex) || isNaN(endIndex) || endIndex < startIndex) {
        filesContainer.innerHTML = "<p style='color:red;'>Please enter valid filename and index range.</p>";
        return;
    }

    // Process multiple executions
    let allFiles = [];
    for (let i = startIndex; i <= endIndex; i++) {
        try {
            const response = await fetch("/run-test", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ code: code, language: "python", stdin_input: "" })
            });
            const data = await response.json();
            if (data.error_message) {
                filesContainer.innerHTML = `<p style='color:red;'>Error: ${data.error_message}</p>`;
                return;
            }
            // Store file content along with computed filename
            //console.log(data.execution_output)
            const fileObj = {
                filename: `${filenameBase.replace(/\.[^/.]+$/, "")}_${i}${filenameBase.match(/\.[^/.]+$/) || ".txt"}`,
                content: data.execution_output
            };
            allFiles.push(fileObj);

            // Create file entry UI element
            const fileEntry = document.createElement("div");
            fileEntry.className = "file-entry";
            fileEntry.style.border = "1px solid #ccc";
            fileEntry.style.borderRadius = "8px";
            fileEntry.style.padding = "10px";
            fileEntry.style.marginBottom = "10px";
            fileEntry.style.display = "flex";
            fileEntry.style.justifyContent = "space-between";
            fileEntry.style.alignItems = "center";

            // Filename display
            const nameSpan = document.createElement("span");
            nameSpan.textContent = fileObj.filename;

            // Preview button
            const previewBtn = document.createElement("button");
            previewBtn.textContent = "Preview";
            previewBtn.onclick = () => alert(fileObj.content);

            // Download button
            const downloadBtn = document.createElement("button");
            downloadBtn.textContent = "Download";
            downloadBtn.onclick = () => {
                const blob = new Blob([fileObj.content], { type: "text/plain" });
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = fileObj.filename;
                a.click();
                URL.revokeObjectURL(url);
            };

            // Delete button
            const deleteBtn = document.createElement("button");
            deleteBtn.textContent = "Delete";
            deleteBtn.onclick = () => {
                fileEntry.remove();
            };

            // Append all UI elements to file entry
            fileEntry.appendChild(nameSpan);
            fileEntry.appendChild(previewBtn);
            fileEntry.appendChild(downloadBtn);
            fileEntry.appendChild(deleteBtn);

            // Append file entry to container
            filesContainer.appendChild(fileEntry);

        } catch (error) {
            filesContainer.innerHTML = `<p style='color:red;'>Execution failed: ${error.message}</p>`;
            return;
        }
    }

    // Store generated files in a global variable for download-all
    window.generatedTestFiles = allFiles;
});

// Download All Files Feature using JSZip
document.getElementById("download-all-files").addEventListener("click", function () {
    if (!window.generatedTestFiles || window.generatedTestFiles.length === 0) {
        alert("No files generated.");
        return;
    }
    // Create a zip file containing all generated files.
    let zip = new JSZip();
    window.generatedTestFiles.forEach(file => {
        zip.file(file.filename, file.content);
    });
    zip.generateAsync({ type: "blob" }).then(function (content) {
        const a = document.createElement("a");
        a.href = URL.createObjectURL(content);
        a.download = "test_case.zip";
        a.click();
        URL.revokeObjectURL(a.href);
    });
});

async function uploadToPolygon(problemData, polygonApiKey, polygonSecret) {
    const baseUrl = "https://polygon.codeforces.com/api";
    
    // Step 1: Authenticate (Polygon uses API key + secret for authentication)
    async function makeRequest(endpoint, params) {
        const queryParams = new URLSearchParams({ ...params, apiKey: polygonApiKey });
        
        const sortedParams = [...queryParams.entries()].sort().map(([key, value]) => `${key}=${value}`).join('&');
        const time = Math.floor(Date.now() / 1000);
        const apiSig = time + '/' + endpoint + '?' + sortedParams + '#' + polygonSecret;
        const hash = await crypto.subtle.digest("SHA-512", new TextEncoder().encode(apiSig));
        const apiSigHash = Array.from(new Uint8Array(hash)).map(b => b.toString(16).padStart(2, '0')).join('');

        queryParams.append("time", time);
        queryParams.append("apiSig", apiSigHash);

        const response = await fetch(`${baseUrl}/${endpoint}?${queryParams}`, {
            method: "POST"
        });

        return response.json();
    }

    try {
        const createProblemResponse = await makeRequest("problem.create", { name: problemData.title });
        if (!createProblemResponse || createProblemResponse.status !== "OK") {
            throw new Error("Failed to create problem: " + createProblemResponse.comment);
        }

        const problemId = createProblemResponse.result.problemId;

        await makeRequest("problem.updateStatement", {
            problemId,
            lang: "en",
            name: problemData.title,
            legend: problemData.description,
            input: problemData.input_specifications,
            output: problemData.output_specifications,
            tutorial: problemData.solution_explanation
        });

        for (let i = 0; i < problemData.examples.length; i++) {
            await makeRequest("problem.saveTest", {
                problemId,
                testIndex: i + 1,
                input: problemData.examples[i].input,
                output: problemData.examples[i].output
            });
        }

        alert("Problem uploaded successfully to Polygon!");
    } catch (error) {
        console.error("Error uploading problem:", error);
        alert("Failed to upload problem: " + error.message);
    }
}


document.getElementById("upload-polygon").addEventListener("click", async function () {
    const problemData = JSON.parse(document.getElementById("problem-data").textContent);
    const apiKey = prompt("Enter your Polygon API Key:");
    const secret = prompt("Enter your Polygon Secret:");
    await uploadToPolygon(problemData, apiKey, secret);
});
