// Helper to switch between tab contents
document.querySelectorAll(".tab-button").forEach(btn => {
    btn.addEventListener("click", function () {
      const tab = this.getAttribute("data-tab");
      document.querySelectorAll(".tab-content").forEach(content => {
        content.classList.add("hidden");
      });
      document.getElementById(tab).classList.remove("hidden");
      
      // When switching to the solution tab, update the statement preview.
      if (tab === "solution") {
          renderContent();
      }
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
    const sections = ['description', 'input-constraints', 'output-constraints', 'note', 'solution-in-natural-language'];

    sections.forEach(id => {
        const previewDiv = document.getElementById(id + "-preview");
        const editElem = document.getElementById(id + "-edit");
        if (previewDiv && editElem) {
            previewDiv.innerHTML = parseMarkdown(editElem.value);
            if (typeof MathJax !== "undefined" && MathJax.Hub) {
                MathJax.Hub.Queue(['Typeset', MathJax.Hub, previewDiv]);
            }
        }
    });
    
    // Update basic fields in Statement tab.
    document.getElementById("title-preview").textContent = document.getElementById("title-edit").value;
    document.getElementById("time-limit-preview").textContent = document.getElementById("time-limit-edit").value;
    document.getElementById("memory-limit-preview").textContent = document.getElementById("memory-limit-edit").value;

    // Render Time Complexity with LaTeX support in Tutorial tab.
    if(document.getElementById("time-complexity-edit")) {
        const tcPreview = document.getElementById("time-complexity-preview");
        tcPreview.innerHTML = parseMarkdown(document.getElementById("time-complexity-edit").value);
        if (typeof MathJax !== "undefined" && MathJax.Hub) {
            MathJax.Hub.Queue(['Typeset', MathJax.Hub, tcPreview]);
        }
    }
    
    // Render Space Complexity with LaTeX support in Tutorial tab.
    if(document.getElementById("space-complexity-edit")) {
        const scPreview = document.getElementById("space-complexity-preview");
        scPreview.innerHTML = parseMarkdown(document.getElementById("space-complexity-edit").value);
        if (typeof MathJax !== "undefined" && MathJax.Hub) {
            MathJax.Hub.Queue(['Typeset', MathJax.Hub, scPreview]);
        }
    }
    
    // Update Tags.
    if(document.getElementById("tags-edit")) {
        document.getElementById("tags-preview").textContent = document.getElementById("tags-edit").value;
    }
    
    // Copy statement preview into the Solution tab
    const statementRightPanel = document.querySelector("#statement .right-panel");
    const statementPreview = document.getElementById("statement-preview");
    if (statementRightPanel && statementPreview) {
        statementPreview.innerHTML = statementRightPanel.innerHTML;
    }
    
    // Finally update the hidden JSON data
    updateProblemData();
}

// Optionally call renderContent() on window load.
window.addEventListener("load", renderContent);

// textarea with auto-resize (excluding code-editor)
document.querySelectorAll("textarea:not(.code-editor)").forEach(function(textarea) {
    textarea.style.height = textarea.scrollHeight + "px";
    textarea.style.overflowY = "hidden";
  
    textarea.addEventListener("input", function() {
      this.style.height = "auto";
      this.style.height = this.scrollHeight + "px";
    });
});

// Handle font size slider
document.getElementById("font-size-slider").addEventListener("input", (e) => {
    document.getElementById("solution-editor").style.fontSize = `${e.target.value}px`;
});