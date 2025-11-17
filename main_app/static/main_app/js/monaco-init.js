// Monaco Editor initialization for code blocks
(function() {
    'use strict';

    // Wait for Monaco to load
    function initMonaco() {
        require.config({
            paths: {
                'vs': 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs'
            }
        });

        require(['vs/editor/editor.main'], function() {
            // Check if dark mode is active - check both body and html
            const isDarkMode = document.body.classList.contains('dark-mode') ||
                              document.documentElement.classList.contains('dark-mode');
            const theme = isDarkMode ? 'vs-dark' : 'vs';

            console.log('Monaco initializing with theme:', theme, 'isDarkMode:', isDarkMode);

            // Find all Monaco code blocks
            const codeBlocks = document.querySelectorAll('.monaco-code-block');

            codeBlocks.forEach((block, index) => {
                const language = block.getAttribute('data-language') || 'plaintext';
                const code = block.getAttribute('data-code') || '';

                // Decode HTML entities
                const decodedCode = decodeHTMLEntities(code);

                // Create container with unique ID
                const editorId = `monaco-editor-${index}`;
                const lineCount = decodedCode.split('\n').length;

                // Add class based on line count
                let containerClass = 'monaco-editor-container';
                if (lineCount === 1) {
                    containerClass += ' single-line';
                } else if (lineCount === 2) {
                    containerClass += ' two-lines';
                }

                block.innerHTML = `<div id="${editorId}" class="${containerClass}"></div>`;

                // Get the container
                const container = document.getElementById(editorId);

                // Adjust height based on line count
                const lineHeight = 22;  // Increased to match Monaco's actual line height
                let calculatedHeight;
                if (lineCount === 1) {
                    calculatedHeight = 55;  // Compact for single line with padding
                } else if (lineCount === 2) {
                    calculatedHeight = 75;  // Medium for 2 lines with padding
                } else {
                    const minHeight = 100;
                    const padding = 60;  // Extra padding for editor chrome
                    // No max height - auto-adjust to content with extra padding
                    calculatedHeight = Math.max(minHeight, lineCount * lineHeight + padding);
                }

                container.style.height = `${calculatedHeight}px`;

                // Create editor
                const editor = monaco.editor.create(container, {
                    value: decodedCode,
                    language: language,
                    theme: theme,
                    readOnly: true,
                    minimap: { enabled: false },
                    scrollBeyondLastLine: false,
                    lineNumbers: 'on',
                    glyphMargin: false,
                    folding: true,
                    lineDecorationsWidth: 0,
                    lineNumbersMinChars: 3,
                    renderLineHighlight: 'none',
                    overviewRulerLanes: 0,
                    hideCursorInOverviewRuler: true,
                    overviewRulerBorder: false,
                    automaticLayout: true,
                    fontSize: 14,
                    fontFamily: "'Fira Code', 'Consolas', 'Monaco', 'Courier New', monospace",
                    fontLigatures: true,
                    contextmenu: false,
                    wordWrap: 'off',
                    // Completely disable vertical scrolling to prevent scroll blocking
                    scrollbar: {
                        vertical: 'hidden',
                        horizontal: 'auto',
                        useShadows: false,
                        horizontalScrollbarSize: 10,
                        alwaysConsumeMouseWheel: false,  // Don't capture mouse wheel events
                        handleMouseWheel: false  // Don't handle mouse wheel at all
                    }
                });

                // Prevent Monaco's scrollable overlay from capturing scroll events
                // This fixes the issue where page scroll gets blocked when mouse is over code blocks
                setTimeout(() => {
                    const domNode = editor.getDomNode();
                    if (domNode) {
                        // Find Monaco's scrollable element and disable vertical scroll capture
                        const scrollableElement = domNode.querySelector('.monaco-scrollable-element');
                        if (scrollableElement) {
                            scrollableElement.style.overflowY = 'hidden';
                        }
                    }
                }, 150);

                // Adjust height to actual content after layout
                setTimeout(() => {
                    const contentHeight = editor.getContentHeight();
                    container.style.height = `${contentHeight}px`;
                    editor.layout();
                }, 100);

                // Store editor reference for theme updates
                block.monacoEditor = editor;

                // Add copy button
                addCopyButton(block, decodedCode);
            });

            // Listen for theme changes
            observeThemeChanges();
        });
    }

    // Decode HTML entities
    function decodeHTMLEntities(text) {
        const textarea = document.createElement('textarea');
        textarea.innerHTML = text;
        return textarea.value;
    }

    // Add copy button to code block
    function addCopyButton(block, code) {
        const copyBtn = document.createElement('button');
        copyBtn.className = 'monaco-copy-btn';
        copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
        copyBtn.setAttribute('aria-label', 'Copy code');

        copyBtn.addEventListener('click', function() {
            navigator.clipboard.writeText(code).then(() => {
                copyBtn.innerHTML = '<i class="fas fa-check"></i>';
                copyBtn.classList.add('copied');
                setTimeout(() => {
                    copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
                    copyBtn.classList.remove('copied');
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy:', err);
                copyBtn.innerHTML = '<i class="fas fa-times"></i>';
                setTimeout(() => {
                    copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
                }, 2000);
            });
        });

        block.appendChild(copyBtn);
    }

    // Observe theme changes and update Monaco editors
    function observeThemeChanges() {
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.attributeName === 'class') {
                    const isDarkMode = document.body.classList.contains('dark-mode') ||
                                      document.documentElement.classList.contains('dark-mode');
                    const theme = isDarkMode ? 'vs-dark' : 'vs';

                    console.log('Theme changed to:', theme);

                    // Update all editors
                    document.querySelectorAll('.monaco-code-block').forEach(block => {
                        if (block.monacoEditor) {
                            monaco.editor.setTheme(theme);
                        }
                    });
                }
            });
        });

        // Observe both body and html elements
        observer.observe(document.body, {
            attributes: true,
            attributeFilter: ['class']
        });

        observer.observe(document.documentElement, {
            attributes: true,
            attributeFilter: ['class']
        });
    }

    // Initialize when DOM and Monaco are ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initMonaco);
    } else {
        initMonaco();
    }
})();
