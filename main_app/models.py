from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
import markdown
import re
from django.utils.text import slugify

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nazwa")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Slug")

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tagi"
        ordering = ['name']

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="Tytuł")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")
    short_description = models.TextField(max_length=200, verbose_name="Krótki opis")
    description = models.TextField(verbose_name="Opis")
    icon = models.CharField(
        max_length=50,
        verbose_name="Ikona",
        help_text='Wpisz klasę ikony z Font Awesome (np. fas fa-code, fab fa-python)',
        default='fas fa-code'
    )
    tags = models.ManyToManyField(Tag, verbose_name="Tagi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data aktualizacji")
    is_active = models.BooleanField(default=True, verbose_name="Aktywny")

    class Meta:
        verbose_name = "Kurs"
        verbose_name_plural = "Kursy"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course_detail', args=[self.slug])
    
class Lesson(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='lessons', verbose_name="Kurs")
    title = models.CharField(max_length=200, verbose_name="Tytuł")
    slug = models.SlugField(max_length=200, verbose_name="Slug")
    order = models.PositiveIntegerField(default=0, verbose_name="Kolejność")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data aktualizacji")
    content_markdown = models.TextField(blank=True, null=True, verbose_name="Treść (Markdown)")

    class Meta:
        ordering = ['order']
        unique_together = ('course', 'slug')
        verbose_name = "Lekcja"
        verbose_name_plural = "Lekcje"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lesson_detail', args=[self.course.slug, self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            
        self.content_markdown = self._process_special_blocks(self.content_markdown)
        super().save(*args, **kwargs)
    
    def _process_special_blocks(self, markdown_text):
        if not markdown_text:
            return markdown_text
        markdown_text = re.sub(
            r'^>\s*\[!(NOTE|WARNING|DANGER)\](.*?)(?=\n{2,}|\Z)',
            self._replace_callout,
            markdown_text,
            flags=re.MULTILINE|re.DOTALL
        )
        return markdown_text
    
    def _replace_callout(self, match):
        callout_type = match.group(1).lower()
        content = match.group(2).strip()
        return f'<div class="callout {callout_type}">{content}</div>'
    
    @property
    def content_html(self):
        if not self.content_markdown:
            return ""
        
        extensions = [
            'markdown.extensions.extra',
            'markdown.extensions.fenced_code',  # Zamienione codehilite na fenced_code
            'markdown.extensions.toc'
        ]

        html = markdown.markdown(self.content_markdown, extensions=extensions)
        
        pattern = re.compile(r'<pre><code class="language-(.*?)">(.*?)</code></pre>', re.DOTALL)
        html = pattern.sub(self._highlight_code, html)
        
        return html
    
    def _highlight_code(self, match):
        language = match.group(1)
        code = match.group(2)

        # Unescape HTML entities in code
        import html
        code = html.unescape(code)

        # Map language aliases to Monaco language IDs
        language_map = {
            'py': 'python',
            'js': 'javascript',
            'ts': 'typescript',
            'html': 'html',
            'css': 'css',
            'bash': 'shell',
            'sh': 'shell',
            'shell': 'shell',
            'sql': 'sql',
            'yaml': 'yaml',
            'yml': 'yaml',
            'json': 'json',
            'xml': 'xml',
            'dockerfile': 'dockerfile',
            'docker': 'dockerfile',
            'csharp': 'csharp',
            'cs': 'csharp',
            'cpp': 'cpp',
            'c++': 'cpp',
            'php': 'php',
        }

        monaco_language = language_map.get(language.lower(), language.lower())

        # Escape code for HTML attribute
        escaped_code = html.escape(code)

        # Return Monaco editor container
        return f'<div class="monaco-code-block" data-language="{monaco_language}" data-code="{escaped_code}"></div>'

class LessonContent(models.Model):
    lesson = models.OneToOneField('Lesson', on_delete=models.CASCADE, related_name='content', verbose_name="Lekcja")
    text_content = RichTextField(blank=True, null=True, verbose_name="Treść tekstowa")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data aktualizacji")

    class Meta:
        verbose_name = "Treść lekcji"
        verbose_name_plural = "Treści lekcji"

    def __str__(self):
        return f"Treść lekcji: {self.lesson.title}"

class Quiz(models.Model):
    lesson = models.OneToOneField('Lesson', on_delete=models.CASCADE, related_name='quiz', verbose_name="Lekcja")
    title = models.CharField(max_length=200, verbose_name="Tytuł")
    description = models.TextField(blank=True, verbose_name="Opis")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data aktualizacji")

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizy"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions', verbose_name="Quiz")
    text = models.TextField(
        verbose_name="Treść pytania",
        help_text="Możesz używać Markdown, w tym bloków kodu. Przykład kodu: ```python\nprint('Hello')\n```"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Kolejność")
    explanation = models.TextField(blank=True, verbose_name="Wyjaśnienie", help_text="Wyjaśnienie poprawnych odpowiedzi")

    class Meta:
        ordering = ['order']
        verbose_name = "Pytanie"
        verbose_name_plural = "Pytania"

    def __str__(self):
        return self.text

    @property
    def text_html(self):
        """Renders text as HTML with markdown support, especially for code blocks"""
        if not self.text:
            return ""

        extensions = [
            'markdown.extensions.extra',
            'markdown.extensions.fenced_code',  # Removed codehilite for Monaco
        ]

        html = markdown.markdown(self.text, extensions=extensions)

        # Apply Pygments syntax highlighting with VS Code style
        pattern = re.compile(r'<pre><code class="language-(.*?)">(.*?)</code></pre>', re.DOTALL)
        html = pattern.sub(self._highlight_code, html)

        # Sanitize HTML to prevent XSS attacks while allowing safe markdown tags
        import bleach
        allowed_tags = [
            'p', 'br', 'strong', 'em', 'u', 'code', 'pre', 'blockquote',
            'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'a', 'div', 'span', 'table', 'thead', 'tbody', 'tr', 'th', 'td',
        ]
        allowed_attrs = {
            'a': ['href', 'title'],
            'div': ['class'],
            'span': ['class'],
            'code': ['class'],
            'pre': ['class'],
        }
        # Add monaco-code-block to allowed tags since we generate it
        allowed_tags.append('div')
        allowed_attrs['div'] = ['class', 'data-language', 'data-code']

        html = bleach.clean(html, tags=allowed_tags, attributes=allowed_attrs, strip=False)

        return html

    def _highlight_code(self, match):
        language = match.group(1)
        code = match.group(2)

        # Unescape HTML entities in code
        import html
        code = html.unescape(code)

        # Map language aliases to Monaco language IDs
        language_map = {
            'py': 'python', 'js': 'javascript', 'ts': 'typescript',
            'html': 'html', 'css': 'css', 'bash': 'shell', 'sh': 'shell',
            'shell': 'shell', 'sql': 'sql', 'yaml': 'yaml', 'yml': 'yaml',
            'json': 'json', 'xml': 'xml', 'dockerfile': 'dockerfile',
            'docker': 'dockerfile', 'csharp': 'csharp', 'cs': 'csharp',
            'cpp': 'cpp', 'c++': 'cpp', 'php': 'php',
        }

        monaco_language = language_map.get(language.lower(), language.lower())
        escaped_code = html.escape(code)

        return f'<div class="monaco-code-block" data-language="{monaco_language}" data-code="{escaped_code}"></div>'

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name="Pytanie")
    text = models.CharField(max_length=255, verbose_name="Tekst odpowiedzi")
    is_correct = models.BooleanField(default=False, verbose_name="Poprawna odpowiedź")
    order = models.PositiveIntegerField(default=0, verbose_name="Kolejność")

    class Meta:
        ordering = ['order']
        verbose_name = "Odpowiedź"
        verbose_name_plural = "Odpowiedzi"

    def __str__(self):
        return self.text
    
class PracticalTask(models.Model):
    lesson = models.OneToOneField(
        'Lesson',
        on_delete=models.CASCADE,
        related_name='practicaltask',
        verbose_name="Lekcja"
    )
    title = models.CharField(max_length=200, verbose_name="Tytuł")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="Slug")

    content_markdown = models.TextField(verbose_name="Treść zadania (Markdown)")
    content_html = models.TextField(editable=False, blank=True, verbose_name="Treść zadania (HTML)")

    instructions_markdown = models.TextField(blank=True, verbose_name="Instrukcje (Markdown)")
    instructions_html = models.TextField(editable=False, blank=True, verbose_name="Instrukcje (HTML)")

    example_markdown = models.TextField(blank=True, verbose_name="Przykład (Markdown)")
    example_html = models.TextField(editable=False, blank=True, verbose_name="Przykład (HTML)")

    hints_markdown = models.TextField(blank=True, verbose_name="Wskazówki (Markdown)")
    hints_html = models.TextField(editable=False, blank=True, verbose_name="Wskazówki (HTML)")

    solution_markdown = models.TextField(blank=True, verbose_name="Rozwiązanie (Markdown)")
    solution_html = models.TextField(editable=False, blank=True, verbose_name="Rozwiązanie (HTML)")

    class Meta:
        verbose_name = "Zadanie praktyczne"
        verbose_name_plural = "Zadania praktyczne"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = base_slug
            counter = 1
            while PracticalTask.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        
        extensions = [
            'markdown.extensions.extra',
            'markdown.extensions.fenced_code',  # Removed codehilite for Monaco
            'markdown.extensions.tables',
            'markdown.extensions.toc'
        ]

        self.content_html = markdown.markdown(self.content_markdown, extensions=extensions)
        self.instructions_html = markdown.markdown(self.instructions_markdown, extensions=extensions)
        self.example_html = markdown.markdown(self.example_markdown, extensions=extensions)
        self.hints_html = markdown.markdown(self.hints_markdown, extensions=extensions)
        self.solution_html = markdown.markdown(self.solution_markdown, extensions=extensions)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tytuł")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="Slug")
    short_description = models.TextField(max_length=300, verbose_name="Krótki opis")
    author_name = models.CharField(max_length=100, verbose_name="Autor")
    published_date = models.DateField(verbose_name="Data publikacji")
    content_markdown = models.TextField(verbose_name="Treść (Markdown)")
    is_published = models.BooleanField(default=True, verbose_name="Opublikowany")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data aktualizacji")

    class Meta:
        ordering = ['-published_date']
        verbose_name = "Post na blogu"
        verbose_name_plural = "Posty na blogu"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            counter = 1
            while BlogPost.objects.filter(slug=self.slug).exists():
                self.slug = f"{slugify(self.title)}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_post_detail', args=[self.slug])

    @property
    def content_html(self):
        if not self.content_markdown:
            return ""

        extensions = [
            'markdown.extensions.extra',
            'markdown.extensions.fenced_code',  # Removed codehilite for Monaco
            'markdown.extensions.tables',
            'markdown.extensions.toc'
        ]

        html = markdown.markdown(self.content_markdown, extensions=extensions)

        # Apply syntax highlighting
        pattern = re.compile(r'<pre><code class="language-(.*?)">(.*?)</code></pre>', re.DOTALL)
        html = pattern.sub(self._highlight_code, html)

        return html

    def _highlight_code(self, match):
        language = match.group(1)
        code = match.group(2)

        # Unescape HTML entities in code
        import html
        code = html.unescape(code)

        # Map language aliases to Monaco language IDs
        language_map = {
            'py': 'python', 'js': 'javascript', 'ts': 'typescript',
            'html': 'html', 'css': 'css', 'bash': 'shell', 'sh': 'shell',
            'shell': 'shell', 'sql': 'sql', 'yaml': 'yaml', 'yml': 'yaml',
            'json': 'json', 'xml': 'xml', 'dockerfile': 'dockerfile',
            'docker': 'dockerfile', 'csharp': 'csharp', 'cs': 'csharp',
            'cpp': 'cpp', 'c++': 'cpp', 'php': 'php',
        }

        monaco_language = language_map.get(language.lower(), language.lower())
        escaped_code = html.escape(code)

        return f'<div class="monaco-code-block" data-language="{monaco_language}" data-code="{escaped_code}"></div>'

class VideoPlaylist(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tytuł kursu wideo")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(max_length=300, verbose_name="Krótki opis")
    thumbnail = models.ImageField(
        upload_to='video_thumbnails/',
        verbose_name="Miniaturka",
        help_text="Zalecany rozmiar: 1280x720px"
    )
    youtube_playlist_url = models.URLField(
        verbose_name="Link do playlisty YouTube",
        help_text="Wklej pełny URL do playlisty YouTube"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Kolejność")
    is_active = models.BooleanField(default=True, verbose_name="Aktywny")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data aktualizacji")

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Kurs wideo"
        verbose_name_plural = "Kursy wideo"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            counter = 1
            while VideoPlaylist.objects.filter(slug=self.slug).exists():
                self.slug = f"{slugify(self.title)}-{counter}"
                counter += 1
        super().save(*args, **kwargs)