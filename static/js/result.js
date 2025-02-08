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
  
// Generate Solution button handler
document.getElementById("generate-solution").addEventListener("click", async function () {
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
        "input-constraints-edit",
        "output-constraints-edit",
        "note-edit"
    ];
    statementElements.forEach(id => {
        const elem = document.getElementById(id);
        if(elem) {
            elem.addEventListener("input", debouncedRenderContent);
        }
    });
    
    // For Tutorial tab editable fields.
    const tutorialElements = [
        "solution-in-natural-language-edit",
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

    // Download statement as PDF using jsPDF.html()
    document.getElementById("download-statement").addEventListener("click", function() {
        generatePDF("#statement .right-panel", "statement.pdf");
    });

    // Download tutorial as PDF using jsPDF.html()
    document.getElementById("download-tutorial").addEventListener("click", function() {
        generatePDF("#tutorial .right-panel", "tutorial.pdf");
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
    problem.input_constraints = document.getElementById("input-constraints-edit").value;
    problem.output_constraints = document.getElementById("output-constraints-edit").value;
    
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
    problem.solution_in_natural_language = document.getElementById("solution-in-natural-language-edit").value;
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
        "input-constraints",
        "output-constraints",
        "note",
        "solution-in-natural-language",
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

function generatePDF(selector, filename) {
    const panel = document.querySelector(selector);
    if (!panel) return;
    
    // Clone the content so we don't affect the live DOM.
    const clone = panel.cloneNode(true);
    
    // Open a new window for printing.
    const printWindow = window.open('', '', 'width=800,height=600');
    
    // Write a basic HTML document that includes your CSS and Paged.js.
    printWindow.document.write(`
        <!DOCTYPE html>
        <html>
          <head>
            <meta charset="utf-8">
            <title>${filename}</title>
            <link rel="stylesheet" href="/static/css/styles.css">
            <script src="https://unpkg.com/pagedjs/dist/paged.polyfill.js"></script>
          </head>
          <body>
            <div id="print-content">
              ${clone.innerHTML}
            </div>
          </body>
        </html>
    `);
    printWindow.document.close();
    
    // Give Paged.js time to process the content (adjust timeout as needed).
    setTimeout(() => {
        printWindow.focus();
        printWindow.print();
        printWindow.close();
    }, 1000);
}