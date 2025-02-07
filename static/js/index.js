window.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("problem-form");
    form.addEventListener("submit", function(event) {
        const skill1 = form.skill1.value;
        const skill2 = form.skill2.value;
        const minDiff = parseInt(form.minDiff.value, 10);
        const maxDiff = parseInt(form.maxDiff.value, 10);
        const minAllowed = 800;
        const maxAllowed = 3500;

        if (skill1 === skill2) {
            alert("Skill 1 and Skill 2 must be different.");
            event.preventDefault();
            return false;
        }
        if (minDiff < minAllowed || minDiff > maxAllowed || maxDiff < minAllowed || maxDiff > maxAllowed) {
            alert("Difficulty must be between 800 and 3500.");
            event.preventDefault();
            return false;
        }
        if (minDiff > maxDiff) {
            alert("Minimum difficulty cannot be greater than maximum difficulty.");
            event.preventDefault();
            return false;
        }
        // Show the loading overlay when the form is submitted.
        document.getElementById("loading-overlay").style.display = "flex";
        return true;
    });
});

// textarea with auto-resize
document.querySelectorAll("textarea").forEach(function(textarea) {
    textarea.style.height = textarea.scrollHeight + "px";
    textarea.style.overflowY = "hidden";
  
    textarea.addEventListener("input", function() {
      this.style.height = "auto";
      this.style.height = this.scrollHeight + "px";
    });
});