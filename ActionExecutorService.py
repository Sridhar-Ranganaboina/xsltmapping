 <script>
        const scriptContent = `
        const validateDateInputs = () => {
            const dateInputs = document.querySelectorAll(".date-input");
            const datePattern = /^(0[1-9]|1[0-2])(\\/([0-2][0-9]|3[01]))?(\\/\\d{4})?$|^\\d{4}$/;

            dateInputs.forEach(input => {
                input.addEventListener("input", function (e) {
                    // Allow only digits and slashes while typing
                    this.value = this.value.replace(/[^0-9\\/]/g, "");

                    // Validate the format
                    if (datePattern.test(this.value)) {
                        this.setCustomValidity("");  // Clear error
                        this.style.borderColor = "green";
                    } else {
                        this.setCustomValidity("Invalid date format!");
                        this.style.borderColor = "red";
                    }
                });
            });
        };

        // Apply validation globally
        document.addEventListener("DOMContentLoaded", validateDateInputs);
        `;

        // Dynamically inject the escaped script
        const script = document.createElement("script");
        script.textContent = scriptContent;
        document.body.appendChild(script);
    </script>
