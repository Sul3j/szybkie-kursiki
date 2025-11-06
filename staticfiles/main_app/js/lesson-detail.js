document.addEventListener('DOMContentLoaded', function() {
    // Automatically add copy buttons to all code blocks
    document.querySelectorAll('.codehilite').forEach(codeBlock => {
        // Check if button already exists
        if (codeBlock.querySelector('.copy-btn')) {
            return;
        }

        const pre = codeBlock.querySelector('pre');
        if (!pre) return;

        // Create copy button
        const copyBtn = document.createElement('button');
        copyBtn.className = 'copy-btn';
        copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
        copyBtn.setAttribute('aria-label', 'Kopiuj kod');
        copyBtn.setAttribute('title', 'Kopiuj kod');

        // Add button to code block
        codeBlock.style.position = 'relative';
        codeBlock.appendChild(copyBtn);
    });

    // Handle copy button clicks
    document.querySelectorAll('.codehilite .copy-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const codeBlock = this.closest('.codehilite').querySelector('pre').innerText;
            navigator.clipboard.writeText(codeBlock)
                .then(() => {
                    const originalHTML = this.innerHTML;
                    this.innerHTML = '<i class="fas fa-check"></i>';
                    this.style.background = 'rgba(72, 187, 120, 0.3)';
                    this.style.borderColor = 'rgba(72, 187, 120, 0.5)';
                    this.style.color = '#48bb78';

                    setTimeout(() => {
                        this.innerHTML = originalHTML;
                        this.style.background = '';
                        this.style.borderColor = '';
                        this.style.color = '';
                    }, 2000);
                })
                .catch(err => {
                    console.error('Błąd kopiowania: ', err);
                    const originalHTML = this.innerHTML;
                    this.innerHTML = '<i class="fas fa-times"></i>';
                    this.style.background = 'rgba(239, 68, 68, 0.3)';
                    this.style.borderColor = 'rgba(239, 68, 68, 0.5)';
                    this.style.color = '#ef4444';
                    setTimeout(() => {
                        this.innerHTML = originalHTML;
                        this.style.background = '';
                        this.style.borderColor = '';
                        this.style.color = '';
                    }, 2000);
                });
        });
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