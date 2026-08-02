/* ==========================================================
   AI Spam Email Classifier
   Professional UI
   Part 3A-3
========================================================== */

document.addEventListener("DOMContentLoaded", () => {

    // ==========================
    // Theme Toggle
    // ==========================

    const body = document.body;
    const themeBtn = document.getElementById("themeToggle");

    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "dark") {
        body.classList.add("dark-mode");

        if (themeBtn) {
            themeBtn.innerHTML =
                '<i class="bi bi-sun-fill"></i>';
        }
    }

    if (themeBtn) {

        themeBtn.addEventListener("click", () => {

            body.classList.toggle("dark-mode");

            if (body.classList.contains("dark-mode")) {

                localStorage.setItem("theme", "dark");

                themeBtn.innerHTML =
                    '<i class="bi bi-sun-fill"></i>';

            } else {

                localStorage.setItem("theme", "light");

                themeBtn.innerHTML =
                    '<i class="bi bi-moon-stars-fill"></i>';

            }

        });

    }

    // ==========================
    // Character Counter
    // ==========================

    const textarea = document.querySelector("textarea");

    if (textarea) {

        const counter = document.createElement("small");

        counter.style.display = "block";
        counter.style.marginTop = "8px";
        counter.style.color = "#6b7280";

        textarea.parentNode.appendChild(counter);

        function updateCounter() {

            counter.innerHTML =
                textarea.value.length + " Characters";

        }

        updateCounter();

        textarea.addEventListener(
            "input",
            updateCounter
        );

    }

    // ==========================
    // Progress Bar Animation
    // ==========================

    const progress =
        document.querySelector(".progress-bar");

    if (progress) {

        const value =
            progress.getAttribute("aria-valuenow");

        progress.style.width = "0%";

        setTimeout(() => {

            progress.style.width = value + "%";

        }, 300);

    }

    // ==========================
    // Fade Animation
    // ==========================

    const cards = document.querySelectorAll(
        ".glass-card, .feature-card"
    );

    cards.forEach((card, index) => {

        card.style.opacity = 0;

        card.style.transform = "translateY(40px)";

        setTimeout(() => {

            card.style.transition =
                ".7s ease";

            card.style.opacity = 1;

            card.style.transform =
                "translateY(0px)";

        }, index * 180);

    });

    // ==========================
    // Form Loading
    // ==========================

    const form =
        document.querySelector("form");

    if (form) {

        form.addEventListener("submit", () => {

            const button =
                form.querySelector("button");

            button.disabled = true;

            button.innerHTML =

                `<span class="spinner-border spinner-border-sm me-2"></span>
                 Scanning Email...`;

        });

    }

    // ==========================
    // Scroll To Top Button
    // ==========================

    const topButton =
        document.createElement("button");

    topButton.innerHTML =
        '<i class="bi bi-arrow-up"></i>';

    topButton.id = "topButton";

    topButton.style.position = "fixed";
    topButton.style.bottom = "25px";
    topButton.style.right = "25px";
    topButton.style.width = "50px";
    topButton.style.height = "50px";
    topButton.style.border = "none";
    topButton.style.borderRadius = "50%";
    topButton.style.background = "#4f46e5";
    topButton.style.color = "#fff";
    topButton.style.cursor = "pointer";
    topButton.style.display = "none";
    topButton.style.zIndex = "999";
    topButton.style.boxShadow =
        "0 10px 20px rgba(0,0,0,.2)";

    document.body.appendChild(topButton);

    window.addEventListener("scroll", () => {

        if (window.scrollY > 300) {

            topButton.style.display = "block";

        } else {

            topButton.style.display = "none";

        }

    });

    topButton.addEventListener("click", () => {

        window.scrollTo({

            top: 0,

            behavior: "smooth"

        });

    });

    // ==========================
    // Auto Focus
    // ==========================

    if (textarea) {

        textarea.focus();

    }

    // ==========================
    // Toast Notification
    // ==========================

    const prediction =
        document.querySelector(".result-icon");

    if (prediction) {

        const toast =
            document.createElement("div");

        toast.innerHTML =
            "Prediction Completed Successfully";

        toast.style.position = "fixed";
        toast.style.top = "20px";
        toast.style.right = "20px";
        toast.style.background = "#10b981";
        toast.style.color = "#fff";
        toast.style.padding = "15px 20px";
        toast.style.borderRadius = "10px";
        toast.style.boxShadow =
            "0 10px 20px rgba(0,0,0,.2)";
        toast.style.zIndex = "9999";

        document.body.appendChild(toast);

        setTimeout(() => {

            toast.remove();

        }, 3000);

    }

    // ==========================
    // Hero Icon Hover
    // ==========================

    const hero =
        document.querySelector(".hero-icon");

    if (hero) {

        hero.addEventListener("mousemove", () => {

            hero.style.transform =
                "scale(1.05) rotate(5deg)";

        });

        hero.addEventListener("mouseleave", () => {

            hero.style.transform =
                "scale(1) rotate(0deg)";

        });

    }

});