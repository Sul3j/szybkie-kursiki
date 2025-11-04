document.addEventListener('DOMContentLoaded', function() {
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        const score = parseFloat(progressBar.getAttribute('data-score'));
        const circumference = 339.292;
        const offset = circumference - (circumference * score / 100);

        progressBar.style.transition = 'stroke-dashoffset 1.5s ease-in-out';
        progressBar.style.strokeDashoffset = offset;
    }

    const elements = document.querySelectorAll('.question-result');
    elements.forEach((el, index) => {
        setTimeout(() => {
            el.style.opacity = 1;
            el.style.transform = 'translateY(0)';
        }, 300 + (index * 150));
    });

    // Scroll Reveal Animations
    const scrollRevealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    // Observe all elements with scroll-reveal classes
    const revealElements = document.querySelectorAll(
        '.scroll-reveal, .scroll-reveal-left, .scroll-reveal-right, .scroll-reveal-scale'
    );

    revealElements.forEach(element => {
        scrollRevealObserver.observe(element);
    });
});