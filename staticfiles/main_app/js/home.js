document.addEventListener('DOMContentLoaded', function() {
    const codeRain = document.querySelector('.code-rain');

    if (codeRain) {
        // Characters for code rain
        const characters = '01';
        const symbols = '{}[]()<>=+-*/%&|!?.;:';
        const keywords = ['def', 'int', 'for', 'if', 'var', 'let', 'new', 'try'];

        // Create code rain drops
        function createRainDrop() {
            const drop = document.createElement('span');

            // Mix of single chars and keywords
            if (Math.random() > 0.7) {
                drop.textContent = keywords[Math.floor(Math.random() * keywords.length)];
            } else {
                const char = Math.random() > 0.5 ?
                    characters[Math.floor(Math.random() * characters.length)] :
                    symbols[Math.floor(Math.random() * symbols.length)];
                drop.textContent = char;
            }

            drop.style.left = Math.random() * 100 + '%';
            drop.style.animationDuration = (Math.random() * 2 + 1.5) + 's';
            drop.style.animationDelay = Math.random() * 0.5 + 's';
            drop.style.fontSize = (Math.random() * 6 + 12) + 'px';

            codeRain.appendChild(drop);

            setTimeout(() => {
                drop.remove();
            }, 4000);
        }

        // Initialize with more drops
        for (let i = 0; i < 80; i++) {
            setTimeout(() => createRainDrop(), i * 50);
        }

        // Create new drops more frequently
        setInterval(createRainDrop, 150);
    }

    // Posts slider
    function initPostsSlider() {
        const slider = document.querySelector('.posts-slider');
        if (!slider) return;

        const track = slider.querySelector('.posts-track');
        const prevBtn = document.querySelector('.posts-prev');
        const nextBtn = document.querySelector('.posts-next');
        const cards = track.querySelectorAll('.post-card');
        const dotsContainer = document.querySelector('.posts-dots');

        if (cards.length === 0) return;

        const isMobile = window.innerWidth <= 768;

        if (isMobile) {
            // Mobile: touch scrolling with dots
            if (dotsContainer) {
                dotsContainer.innerHTML = '';

                // Show scroll hint animation on first visit
                let hasScrolled = false;
                if (cards.length > 1) {
                    setTimeout(() => {
                        if (!hasScrolled) {
                            slider.scrollTo({
                                left: 50,
                                behavior: 'smooth'
                            });
                            setTimeout(() => {
                                slider.scrollTo({
                                    left: 0,
                                    behavior: 'smooth'
                                });
                            }, 600);
                        }
                    }, 1000);
                }

                slider.addEventListener('scroll', () => {
                    hasScrolled = true;
                }, { once: true });

                cards.forEach((card, index) => {
                    const dot = document.createElement('div');
                    dot.className = 'dot';
                    if (index === 0) dot.classList.add('active');

                    dot.addEventListener('click', () => {
                        // Add haptic-like feedback
                        dot.style.transform = 'scale(0.9)';
                        setTimeout(() => {
                            dot.style.transform = '';
                        }, 100);

                        card.scrollIntoView({
                            behavior: 'smooth',
                            inline: 'center',
                            block: 'nearest'
                        });
                    });

                    dotsContainer.appendChild(dot);
                });

                // Update active dot on scroll
                let scrollTimer;
                slider.addEventListener('scroll', () => {
                    clearTimeout(scrollTimer);
                    scrollTimer = setTimeout(() => {
                        const scrollLeft = slider.scrollLeft;
                        const sliderCenter = scrollLeft + (slider.offsetWidth / 2);

                        let activeIndex = 0;
                        let minDistance = Infinity;

                        cards.forEach((card, index) => {
                            const cardLeft = card.offsetLeft;
                            const cardCenter = cardLeft + (card.offsetWidth / 2);
                            const distance = Math.abs(cardCenter - sliderCenter);

                            if (distance < minDistance) {
                                minDistance = distance;
                                activeIndex = index;
                            }
                        });

                        const dots = dotsContainer.querySelectorAll('.dot');
                        dots.forEach((dot, index) => {
                            dot.classList.toggle('active', index === activeIndex);
                        });
                    }, 50);
                });
            }
        } else {
            // Desktop: button navigation
            if (prevBtn && nextBtn) {
                let currentIndex = 0;
                const slidesToShow = window.innerWidth >= 1024 ? 2 : 1;

                function updateSlider() {
                    const cardWidth = cards[0].offsetWidth;
                    const gap = 30;
                    const offset = -(currentIndex * (cardWidth + gap));
                    track.style.transform = `translateX(${offset}px)`;

                    prevBtn.disabled = currentIndex === 0;
                    nextBtn.disabled = currentIndex >= cards.length - slidesToShow;
                    prevBtn.style.opacity = currentIndex === 0 ? '0.3' : '1';
                    nextBtn.style.opacity = currentIndex >= cards.length - slidesToShow ? '0.3' : '1';
                }

                prevBtn.addEventListener('click', () => {
                    if (currentIndex > 0) {
                        currentIndex--;
                        updateSlider();
                    }
                });

                nextBtn.addEventListener('click', () => {
                    if (currentIndex < cards.length - slidesToShow) {
                        currentIndex++;
                        updateSlider();
                    }
                });

                updateSlider();
            }
        }
    }

    initPostsSlider();

    // Video Slider
    function initVideoSlider() {
        const slider = document.querySelector('.video-slider');
        if (!slider) return;

        const track = slider.querySelector('.video-track');
        const prevBtn = document.querySelector('.video-prev');
        const nextBtn = document.querySelector('.video-next');
        const cards = track.querySelectorAll('.video-card');
        const dotsContainer = document.querySelector('.video-dots');

        if (cards.length === 0) return;

        const isMobile = window.innerWidth <= 768;

        if (isMobile) {
            // Mobile: touch scrolling with dots
            if (dotsContainer) {
                dotsContainer.innerHTML = '';

                // Show scroll hint animation on first visit
                let hasScrolled = false;
                if (cards.length > 1) {
                    setTimeout(() => {
                        if (!hasScrolled) {
                            slider.scrollTo({
                                left: 50,
                                behavior: 'smooth'
                            });
                            setTimeout(() => {
                                slider.scrollTo({
                                    left: 0,
                                    behavior: 'smooth'
                                });
                            }, 600);
                        }
                    }, 1500);
                }

                slider.addEventListener('scroll', () => {
                    hasScrolled = true;
                }, { once: true });

                cards.forEach((card, index) => {
                    const dot = document.createElement('div');
                    dot.className = 'dot';
                    if (index === 0) dot.classList.add('active');

                    dot.addEventListener('click', () => {
                        // Add haptic-like feedback
                        dot.style.transform = 'scale(0.9)';
                        setTimeout(() => {
                            dot.style.transform = '';
                        }, 100);

                        card.scrollIntoView({
                            behavior: 'smooth',
                            inline: 'center',
                            block: 'nearest'
                        });
                    });

                    dotsContainer.appendChild(dot);
                });

                // Update active dot on scroll
                let scrollTimer;
                slider.addEventListener('scroll', () => {
                    clearTimeout(scrollTimer);
                    scrollTimer = setTimeout(() => {
                        const scrollLeft = slider.scrollLeft;
                        const sliderCenter = scrollLeft + (slider.offsetWidth / 2);

                        let activeIndex = 0;
                        let minDistance = Infinity;

                        cards.forEach((card, index) => {
                            const cardLeft = card.offsetLeft;
                            const cardCenter = cardLeft + (card.offsetWidth / 2);
                            const distance = Math.abs(cardCenter - sliderCenter);

                            if (distance < minDistance) {
                                minDistance = distance;
                                activeIndex = index;
                            }
                        });

                        const dots = dotsContainer.querySelectorAll('.dot');
                        dots.forEach((dot, index) => {
                            dot.classList.toggle('active', index === activeIndex);
                        });
                    }, 50);
                });
            }
        } else {
            // Desktop: button navigation
            if (prevBtn && nextBtn) {
                let currentIndex = 0;
                const slidesToShow = window.innerWidth >= 1024 ? 2 : 1;

                function updateSlider() {
                    const cardWidth = cards[0].offsetWidth;
                    const gap = 30;
                    const offset = -(currentIndex * (cardWidth + gap));
                    track.style.transform = `translateX(${offset}px)`;

                    prevBtn.disabled = currentIndex === 0;
                    nextBtn.disabled = currentIndex >= cards.length - slidesToShow;
                    prevBtn.style.opacity = currentIndex === 0 ? '0.3' : '1';
                    nextBtn.style.opacity = currentIndex >= cards.length - slidesToShow ? '0.3' : '1';
                }

                prevBtn.addEventListener('click', () => {
                    if (currentIndex > 0) {
                        currentIndex--;
                        updateSlider();
                    }
                });

                nextBtn.addEventListener('click', () => {
                    if (currentIndex < cards.length - slidesToShow) {
                        currentIndex++;
                        updateSlider();
                    }
                });

                updateSlider();
            }
        }
    }

    initVideoSlider();
});
