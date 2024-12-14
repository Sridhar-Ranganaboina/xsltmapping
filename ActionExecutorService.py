<script>
    const scriptContent = \"const validateDateInputs = () => {\\n\
        const dateInputs = document.querySelectorAll(\\\".date-input\\\");\\n\
        const datePattern = /^(0[1-9]|1[0-2])(\\/([0-2][0-9]|3[01]))?(\\/\\d{4})?$|^\\d{4}$/;\\n\
        dateInputs.forEach(input => {\\n\
            // Restrict allowed characters on typing\\n\
            input.addEventListener(\\\"input\\\", function () {\\n\
                this.value = this.value.replace(/[^0-9\\/]/g, \\\"\\\"); // Allow only digits and slashes\\n\
            });\\n\
            // Validate the format on blur\\n\
            input.addEventListener(\\\"blur\\\", function () {\\n\
                if (datePattern.test(this.value)) {\\n\
                    this.setCustomValidity(\\\"\");  // Clear error\\n\
                    this.style.borderColor = \\\"green\\\";\\n\
                } else {\\n\
                    this.setCustomValidity(\\\"Invalid date format!\\\");\\n\
                    this.style.borderColor = \\\"red\\\";\\n\
                }\\n\
            });\\n\
        });\\n\
    };\\n\
    // Apply validation globally\\n\
    document.addEventListener(\\\"DOMContentLoaded\\\", validateDateInputs);\";

    // Dynamically add the escaped script content
    const script = document.createElement(\"script\");
    script.textContent = scriptContent;
    document.body.appendChild(script);
</script>
