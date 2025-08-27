// Simple JS to enhance UI interactions
document.addEventListener("DOMContentLoaded", function() {
    console.log("Custom JS loaded ✅");

    // Auto-dismiss flash messages after 4 sec
    let alerts = document.querySelectorAll(".alert");
    if (alerts) {
        setTimeout(() => {
            alerts.forEach(alert => {
                alert.style.transition = "opacity 0.5s";
                alert.style.opacity = "0";
                setTimeout(() => alert.remove(), 500);
            });
        }, 4000);
    }

    // Highlight clicked row in dashboard
    let rows = document.querySelectorAll("table.table tbody tr");
    rows.forEach(row => {
        row.addEventListener("click", () => {
            rows.forEach(r => r.classList.remove("table-active"));
            row.classList.add("table-active");
        });
    });

    function scrollToHash() {
        if (window.location.hash === "#upload") {
            const el = document.getElementById("upload");
            if (el) {
                el.scrollIntoView({ behavior: "smooth", block: "start" });
            }
        }
    }
    function scrollToTop() {
        window.scrollTo({ top: 0, behavior: "smooth" });
    }

    // Initial check and on hash changes
    scrollToHash();
    window.addEventListener("hashchange", scrollToHash);

    // Intercept navbar Upload click to ensure smooth scroll even when already on /dashboard
    const uploadLink = document.getElementById("nav-upload");
    if (uploadLink) {
        uploadLink.addEventListener("click", (e) => {
            e.preventDefault();
            if (location.pathname.endsWith("/dashboard")) {
                // Force re-scroll even if hash already set
                history.replaceState(null, "", "#upload");
                scrollToHash();
            } else {
                window.location.href = "/dashboard#upload";
            }
        });
    }

    const dashboardLink = document.getElementById("nav-dashboard");
    if (dashboardLink) {
        dashboardLink.addEventListener("click", (e) => {
            e.preventDefault();
            if (location.pathname.endsWith("/dashboard")) {
                // Remove hash and scroll to top
                history.replaceState(null, "", "/dashboard");
                scrollToTop();
            } else {
                window.location.href = "/dashboard";
            }
        });
    }

    // Word count for abstract textarea
    const abstractTextarea = document.getElementById("abstract-content");
    const wordCountEl = document.getElementById("word-count");
    if (abstractTextarea && wordCountEl) {
        const updateCount = () => {
            const text = abstractTextarea.value.trim();
            const words = text.length ? text.split(/\s+/).filter(Boolean) : [];
            wordCountEl.textContent = String(words.length);
        };
        abstractTextarea.addEventListener("input", updateCount);
        updateCount();
    }

    // View modal logic
    const viewButtons = document.querySelectorAll('.view-abs-btn');
    if (viewButtons.length) {
        viewButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const title = btn.getAttribute('data-title') || 'Abstract';
                const content = btn.getAttribute('data-content') || '';
                const date = btn.getAttribute('data-date') || '';
                const modalTitle = document.getElementById('viewAbsTitle');
                const modalContent = document.getElementById('viewAbsContent');
                const modalMeta = document.getElementById('viewAbsMeta');
                if (modalTitle && modalContent && modalMeta) {
                    modalTitle.textContent = title;
                    modalContent.textContent = content;
                    modalMeta.textContent = date ? `Uploaded at: ${date}` : '';
                    const modalEl = document.getElementById('viewAbsModal');
                    if (modalEl) {
                        const bsModal = new bootstrap.Modal(modalEl);
                        bsModal.show();
                    }
                }
            });
        });
    }
});
