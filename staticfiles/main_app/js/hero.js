class VSCodeTypewriter {
    constructor() {
        this.codeSnippets = [];
        this.currentSnippet = 0;
        this.currentLine = 0;
        this.currentChar = 0;
        this.typingSpeed = 100;
        this.lastTypeTime = 0;
        this.isDeleting = false;
        this.pauseTime = 0;
        this.pauseDuration = 2000; 

        this.init();
    }

    init() {
        this.codeElement = document.getElementById('vscode-code');
        this.lineNumbersElement = document.getElementById('vscode-line-numbers');
        this.editorElement = document.querySelector('.vscode-editor');
        this.filenameElement = document.getElementById('vscode-filename');
        this.tabNameElement = document.getElementById('vscode-tab-name');
        this.tabIconElement = document.getElementById('vscode-tab-icon');
        this.explorerFileElement = document.getElementById('vscode-explorer-file');
        this.languageElement = document.getElementById('vscode-language');

        if (!this.codeElement) {
            console.error('VSCode elements not found');
            return;
        }

        this.createCodeSnippets();
        this.startTyping();
        this.setupScrollSync();

        console.log('VSCodeTypewriter: Initialized!');
    }

    setupScrollSync() {
        if (this.editorElement && this.lineNumbersElement) {
            this.editorElement.addEventListener('scroll', () => {
                this.lineNumbersElement.style.transform = `translateY(-${this.editorElement.scrollTop}px)`;
            });
        }
    }

    createCodeSnippets() {
        this.codeSnippets.push({
            language: 'Python',
            filename: 'scraper.py',
            icon: 'fab fa-python',
            iconColor: '#3776ab',
            lines: [
                { text: 'import', type: 'keyword' },
                { text: ' requests', type: 'text' },
                { text: '\n', type: 'text' },
                { text: 'from', type: 'keyword' },
                { text: ' bs4 ', type: 'text' },
                { text: 'import', type: 'keyword' },
                { text: ' BeautifulSoup', type: 'class' },
                { text: '\n\n', type: 'text' },
                { text: 'def', type: 'keyword' },
                { text: ' scrape_website', type: 'function' },
                { text: '(', type: 'text' },
                { text: 'url', type: 'param' },
                { text: '):\n    ', type: 'text' },
                { text: 'response', type: 'text' },
                { text: ' = ', type: 'operator' },
                { text: 'requests', type: 'text' },
                { text: '.', type: 'operator' },
                { text: 'get', type: 'function' },
                { text: '(', type: 'text' },
                { text: 'url', type: 'param' },
                { text: ')\n    ', type: 'text' },
                { text: 'soup', type: 'text' },
                { text: ' = ', type: 'operator' },
                { text: 'BeautifulSoup', type: 'class' },
                { text: '(', type: 'text' },
                { text: 'response', type: 'text' },
                { text: '.', type: 'operator' },
                { text: 'text', type: 'text' },
                { text: ')\n    ', type: 'text' },
                { text: 'return', type: 'keyword' },
                { text: ' soup', type: 'text' },
                { text: '.', type: 'operator' },
                { text: 'find_all', type: 'function' },
                { text: '(', type: 'text' },
                { text: '"article"', type: 'string' },
                { text: ')', type: 'text' }
            ]
        });

        this.codeSnippets.push({
            language: 'JavaScript',
            filename: 'api.js',
            icon: 'fab fa-js',
            iconColor: '#f7df1e',
            lines: [
                { text: 'async', type: 'keyword' },
                { text: ' ', type: 'text' },
                { text: 'function', type: 'keyword' },
                { text: ' fetchUsers', type: 'function' },
                { text: '() {\n  ', type: 'text' },
                { text: 'try', type: 'keyword' },
                { text: ' {\n    ', type: 'text' },
                { text: 'const', type: 'keyword' },
                { text: ' response = ', type: 'text' },
                { text: 'await', type: 'keyword' },
                { text: ' ', type: 'text' },
                { text: 'fetch', type: 'function' },
                { text: '(', type: 'text' },
                { text: "'/api/users'", type: 'string' },
                { text: ');\n    ', type: 'text' },
                { text: 'const', type: 'keyword' },
                { text: ' data = ', type: 'text' },
                { text: 'await', type: 'keyword' },
                { text: ' response', type: 'text' },
                { text: '.', type: 'operator' },
                { text: 'json', type: 'function' },
                { text: '();\n    ', type: 'text' },
                { text: 'return', type: 'keyword' },
                { text: ' data', type: 'text' },
                { text: '.', type: 'operator' },
                { text: 'map', type: 'function' },
                { text: '(', type: 'text' },
                { text: 'user', type: 'param' },
                { text: ' ', type: 'text' },
                { text: '=>', type: 'operator' },
                { text: ' ({\n      id: user', type: 'text' },
                { text: '.', type: 'operator' },
                { text: 'id,\n      name: user', type: 'text' },
                { text: '.', type: 'operator' },
                { text: 'name\n    }));\n  } ', type: 'text' },
                { text: 'catch', type: 'keyword' },
                { text: ' (error) {\n    ', type: 'text' },
                { text: 'console', type: 'text' },
                { text: '.', type: 'operator' },
                { text: 'error', type: 'function' },
                { text: '(', type: 'text' },
                { text: "'Failed to fetch'", type: 'string' },
                { text: ', error);\n  }\n}', type: 'text' }
            ]
        });

        this.codeSnippets.push({
            language: 'Angular',
            filename: 'app.component.ts',
            icon: 'fab fa-angular',
            iconColor: '#dd0031',
            lines: [
                { text: 'import', type: 'keyword' },
                { text: ' { Component, ', type: 'text' },
                { text: 'OnInit', type: 'class' },
                { text: ' } ', type: 'text' },
                { text: 'from', type: 'keyword' },
                { text: ' ', type: 'text' },
                { text: "'@angular/core'", type: 'string' },
                { text: ';\n\n@', type: 'text' },
                { text: 'Component', type: 'class' },
                { text: '({\n  ', type: 'text' },
                { text: 'selector', type: 'param' },
                { text: ': ', type: 'operator' },
                { text: "'app-root'", type: 'string' },
                { text: ',\n  ', type: 'text' },
                { text: 'templateUrl', type: 'param' },
                { text: ': ', type: 'operator' },
                { text: "'./app.component.html'", type: 'string' },
                { text: '\n})\n', type: 'text' },
                { text: 'export', type: 'keyword' },
                { text: ' ', type: 'text' },
                { text: 'class', type: 'keyword' },
                { text: ' AppComponent ', type: 'class' },
                { text: 'implements', type: 'keyword' },
                { text: ' OnInit {\n  ', type: 'text' },
                { text: 'title', type: 'param' },
                { text: ': ', type: 'operator' },
                { text: 'string', type: 'class' },
                { text: ' = ', type: 'operator' },
                { text: "'Szybkie Kursiki'", type: 'string' },
                { text: ';\n  ', type: 'text' },
                { text: 'users', type: 'param' },
                { text: ': ', type: 'operator' },
                { text: 'any', type: 'class' },
                { text: '[] = [];\n\n  ', type: 'text' },
                { text: 'ngOnInit', type: 'function' },
                { text: '(): ', type: 'text' },
                { text: 'void', type: 'class' },
                { text: ' {\n    ', type: 'text' },
                { text: 'this', type: 'keyword' },
                { text: '.', type: 'operator' },
                { text: 'loadUsers', type: 'function' },
                { text: '();\n  }\n}', type: 'text' }
            ]
        });

        this.codeSnippets.push({
            language: 'TypeScript',
            filename: 'types.ts',
            icon: 'fab fa-js-square',
            iconColor: '#3178c6',
            lines: [
                { text: 'interface', type: 'keyword' },
                { text: ' User {\n  ', type: 'text' },
                { text: 'id', type: 'param' },
                { text: ': ', type: 'operator' },
                { text: 'number', type: 'class' },
                { text: ';\n  ', type: 'text' },
                { text: 'name', type: 'param' },
                { text: ': ', type: 'operator' },
                { text: 'string', type: 'class' },
                { text: ';\n  ', type: 'text' },
                { text: 'email', type: 'param' },
                { text: ': ', type: 'operator' },
                { text: 'string', type: 'class' },
                { text: ';\n  ', type: 'text' },
                { text: 'role', type: 'param' },
                { text: ': ', type: 'operator' },
                { text: '"admin"', type: 'string' },
                { text: ' | ', type: 'operator' },
                { text: '"user"', type: 'string' },
                { text: ';\n}\n\n', type: 'text' },
                { text: 'const', type: 'keyword' },
                { text: ' fetchUser ', type: 'function' },
                { text: '= ', type: 'operator' },
                { text: 'async', type: 'keyword' },
                { text: ' (', type: 'text' },
                { text: 'id', type: 'param' },
                { text: ': ', type: 'operator' },
                { text: 'number', type: 'class' },
                { text: '): ', type: 'operator' },
                { text: 'Promise', type: 'class' },
                { text: '<', type: 'operator' },
                { text: 'User', type: 'class' },
                { text: '> ', type: 'operator' },
                { text: '=> ', type: 'operator' },
                { text: '{\n  ', type: 'text' },
                { text: 'const', type: 'keyword' },
                { text: ' response = ', type: 'text' },
                { text: 'await', type: 'keyword' },
                { text: ' ', type: 'text' },
                { text: 'fetch', type: 'function' },
                { text: '(`/users/${', type: 'string' },
                { text: 'id', type: 'param' },
                { text: '}`);\n  ', type: 'string' },
                { text: 'return', type: 'keyword' },
                { text: ' response', type: 'text' },
                { text: '.', type: 'operator' },
                { text: 'json', type: 'function' },
                { text: '();\n};', type: 'text' }
            ]
        });

        this.codeSnippets.push({
            language: 'C#',
            filename: 'UserController.cs',
            icon: 'fas fa-code',
            iconColor: '#68217a',
            lines: [
                { text: 'using', type: 'keyword' },
                { text: ' Microsoft.AspNetCore.Mvc;\n\n', type: 'text' },
                { text: 'namespace', type: 'keyword' },
                { text: ' Api.Controllers\n{\n  [', type: 'text' },
                { text: 'ApiController', type: 'class' },
                { text: ']\n  [', type: 'text' },
                { text: 'Route', type: 'class' },
                { text: '(', type: 'text' },
                { text: '"api/[controller]"', type: 'string' },
                { text: ')]\n  ', type: 'text' },
                { text: 'public', type: 'keyword' },
                { text: ' ', type: 'text' },
                { text: 'class', type: 'keyword' },
                { text: ' UserController ', type: 'class' },
                { text: ': ', type: 'operator' },
                { text: 'ControllerBase', type: 'class' },
                { text: '\n  {\n    [', type: 'text' },
                { text: 'HttpGet', type: 'class' },
                { text: ']\n    ', type: 'text' },
                { text: 'public', type: 'keyword' },
                { text: ' ', type: 'text' },
                { text: 'async', type: 'keyword' },
                { text: ' Task<', type: 'text' },
                { text: 'IActionResult', type: 'class' },
                { text: '> GetUsers()\n    {\n      ', type: 'text' },
                { text: 'var', type: 'keyword' },
                { text: ' users = ', type: 'text' },
                { text: 'await', type: 'keyword' },
                { text: ' _context', type: 'text' },
                { text: '.', type: 'operator' },
                { text: 'Users\n        ', type: 'text' },
                { text: '.', type: 'operator' },
                { text: 'Where', type: 'function' },
                { text: '(u ', type: 'text' },
                { text: '=>', type: 'operator' },
                { text: ' u', type: 'text' },
                { text: '.', type: 'operator' },
                { text: 'IsActive)\n        ', type: 'text' },
                { text: '.', type: 'operator' },
                { text: 'ToListAsync', type: 'function' },
                { text: '();\n\n      ', type: 'text' },
                { text: 'return', type: 'keyword' },
                { text: ' ', type: 'text' },
                { text: 'Ok', type: 'function' },
                { text: '(users);\n    }\n  }\n}', type: 'text' }
            ]
        });

        this.codeSnippets.push({
            language: 'C++',
            filename: 'vector.cpp',
            icon: 'fas fa-code',
            iconColor: '#00599c',
            lines: [
                { text: '#include', type: 'keyword' },
                { text: ' <iostream>\n', type: 'text' },
                { text: '#include', type: 'keyword' },
                { text: ' <vector>\n', type: 'text' },
                { text: '#include', type: 'keyword' },
                { text: ' <algorithm>\n\n', type: 'text' },
                { text: 'int', type: 'class' },
                { text: ' main', type: 'function' },
                { text: '() {\n  std::', type: 'text' },
                { text: 'vector', type: 'class' },
                { text: '<', type: 'operator' },
                { text: 'int', type: 'class' },
                { text: '> numbers = {', type: 'text' },
                { text: '5', type: 'number' },
                { text: ', ', type: 'text' },
                { text: '2', type: 'number' },
                { text: ', ', type: 'text' },
                { text: '8', type: 'number' },
                { text: ', ', type: 'text' },
                { text: '1', type: 'number' },
                { text: ', ', type: 'text' },
                { text: '9', type: 'number' },
                { text: '};\n\n  std::', type: 'text' },
                { text: 'sort', type: 'function' },
                { text: '(numbers', type: 'text' },
                { text: '.', type: 'operator' },
                { text: 'begin(), numbers', type: 'text' },
                { text: '.', type: 'operator' },
                { text: 'end());\n\n  ', type: 'text' },
                { text: 'for', type: 'keyword' },
                { text: ' (', type: 'text' },
                { text: 'const', type: 'keyword' },
                { text: ' ', type: 'text' },
                { text: 'auto', type: 'keyword' },
                { text: '& num : numbers) {\n    std::cout ', type: 'text' },
                { text: '<<', type: 'operator' },
                { text: ' num ', type: 'text' },
                { text: '<<', type: 'operator' },
                { text: ' ', type: 'text' },
                { text: '" "', type: 'string' },
                { text: ';\n  }\n\n  ', type: 'text' },
                { text: 'return', type: 'keyword' },
                { text: ' ', type: 'text' },
                { text: '0', type: 'number' },
                { text: ';\n}', type: 'text' }
            ]
        });
    }

    switchToSnippet(index) {
        const snippet = this.codeSnippets[index];

        this.filenameElement.textContent = snippet.filename;
        this.tabNameElement.textContent = snippet.filename;
        this.languageElement.textContent = snippet.language;

        this.tabIconElement.className = snippet.icon;
        this.tabIconElement.style.color = snippet.iconColor;

        const explorerIcon = this.explorerFileElement.querySelector('.vscode-file-icon');
        if (explorerIcon) {
            explorerIcon.className = 'vscode-file-icon ' + snippet.icon;
            explorerIcon.style.color = snippet.iconColor;
        }
        const explorerName = this.explorerFileElement.querySelector('span');
        if (explorerName) {
            explorerName.textContent = snippet.filename;
        }
    }

    getColorForType(type) {
        const colors = {
            'keyword': 'vscode-keyword',
            'function': 'vscode-function',
            'class': 'vscode-class',
            'string': 'vscode-string',
            'number': 'vscode-number',
            'comment': 'vscode-comment',
            'operator': 'vscode-operator',
            'param': 'vscode-param',
            'text': ''
        };
        return colors[type] || '';
    }

    updateLineNumbers(count) {
        this.lineNumbersElement.innerHTML = '';
        for (let i = 1; i <= Math.max(count, 10); i++) {
            const lineNum = document.createElement('div');
            lineNum.className = 'vscode-line-number';
            lineNum.textContent = i;
            this.lineNumbersElement.appendChild(lineNum);
        }
    }

    startTyping() {
        this.switchToSnippet(this.currentSnippet);
        requestAnimationFrame((timestamp) => this.animate(timestamp));
    }

    animate(timestamp) {
        const snippet = this.codeSnippets[this.currentSnippet];

        if (this.pauseTime > 0) {
            if (timestamp - this.pauseTime >= this.pauseDuration) {
                this.isDeleting = true;
                this.pauseTime = 0;
            }
        } else if (timestamp - this.lastTypeTime >= this.typingSpeed) {
            this.lastTypeTime = timestamp;

            if (this.isDeleting) {
                if (this.currentChar > 0) {
                    this.currentChar--;
                } else {
                    this.isDeleting = false;
                    this.currentSnippet = (this.currentSnippet + 1) % this.codeSnippets.length;
                    this.switchToSnippet(this.currentSnippet);
                }
            } else {
                if (this.currentChar < snippet.lines.length) {
                    this.currentChar++;
                } else {
                    this.pauseTime = timestamp;
                }
            }

            this.render();
        }

        requestAnimationFrame((timestamp) => this.animate(timestamp));
    }

    render() {
        const snippet = this.codeSnippets[this.currentSnippet];
        const codeLines = [];
        let currentLine = '';
        let lineCount = 1;

        for (let i = 0; i < this.currentChar && i < snippet.lines.length; i++) {
            const segment = snippet.lines[i];
            const text = segment.text;
            const colorClass = this.getColorForType(segment.type);

            const parts = text.split('\n');

            parts.forEach((part, index) => {
                if (index > 0) {
                    codeLines.push(currentLine);
                    currentLine = '';
                    lineCount++;
                }

                if (part) {
                    if (colorClass) {
                        currentLine += `<span class="${colorClass}">${this.escapeHtml(part)}</span>`;
                    } else {
                        currentLine += this.escapeHtml(part);
                    }
                }
            });
        }

        if (currentLine) {
            codeLines.push(currentLine);
        }

        if (!this.isDeleting && this.currentChar < snippet.lines.length) {
            const lastIndex = codeLines.length - 1;
            if (lastIndex >= 0) {
                codeLines[lastIndex] += '<span class="vscode-cursor"></span>';
            }
        }

        this.codeElement.innerHTML = codeLines.map(line =>
            `<div class="vscode-code-line">${line || ' '}</div>`
        ).join('');

        this.updateLineNumbers(Math.max(codeLines.length, 1));
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const codeElement = document.getElementById('vscode-code');

    if (codeElement) {
        new VSCodeTypewriter();
        console.log('VSCodeTypewriter: Ready!');
    } else {
        console.log('VSCodeTypewriter: Code element not found, skipping initialization');
    }
});
