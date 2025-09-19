 function setupToggle(buttonId, inputId) {
            const toggleBtn = document.getElementById(buttonId);
            const input = document.getElementById(inputId);

            toggleBtn.addEventListener("click", () => {
                if (input.type === "password") {
                    input.type = "text";
                    toggleBtn.textContent = "🙈"; // Monkey eye closed
                } else {
                    input.type = "password";
                    toggleBtn.textContent = "👁️"; // Normal eye
                }
            });
        }

        setupToggle("togglePassword", "password");
        setupToggle("toggleConfirm", "confirm");