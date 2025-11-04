document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const filterTags = document.querySelectorAll('.filter-tag');
    const courseCards = document.querySelectorAll('.course-card');
    
    if (searchInput) {
        searchInput.addEventListener('input', filterCourses);
    }
    
    filterTags.forEach(tag => {
        tag.addEventListener('click', function() {
            filterTags.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            filterCourses();
        });
    });
    
    function filterCourses() {
        const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
        const activeFilter = document.querySelector('.filter-tag.active').dataset.filter;
        
        let visibleCount = 0;
        
        courseCards.forEach(card => {
            const title = card.querySelector('.course-title').textContent.toLowerCase();
            const description = card.querySelector('.course-description').textContent.toLowerCase();
            const tags = card.dataset.tags.toLowerCase();
            
            const matchesSearch = title.includes(searchTerm) || 
                                description.includes(searchTerm) || 
                                tags.includes(searchTerm);
            
            const matchesFilter = activeFilter === 'all' || 
                                tags.includes(activeFilter);
            
            if (matchesSearch && matchesFilter) {
                card.style.display = 'flex';
                card.classList.add('revealed'); // Ensure revealed class for filtered cards
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });
        
        const emptyMessage = document.querySelector('.course-grid-empty');
        if (visibleCount === 0) {
            if (!emptyMessage) {
                const grid = document.querySelector('.courses-grid');
                const message = document.createElement('div');
                message.className = 'course-grid-empty';
                message.innerHTML = '<p>Brak kursów spełniających kryteria wyszukiwania</p>';
                grid.appendChild(message);
            }
        } else if (emptyMessage) {
            emptyMessage.remove();
        }
    }
    
    if (searchInput || filterTags.length > 0) {
        filterCourses();
    }

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

    // Special handling for section headers
    const sectionHeaders = document.querySelectorAll('.section-header');
    sectionHeaders.forEach(header => {
        header.classList.add('scroll-reveal');
        scrollRevealObserver.observe(header);
    });
});