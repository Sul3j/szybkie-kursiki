from django.db import models
from django.urls import reverse
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter 
from ckeditor.fields import RichTextField
import re
from django.utils.text import slugify
import markdown

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
        return reverse('lesson_detail', args=[self.course.slug, self.slug])
    
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
            'markdown.extensions.codehilite',
            'markdown.extensions.toc'
        ]

        html = markdown.markdown(self.content_markdown, extensions=extensions)
        
        pattern = re.compile(r'<pre><code class="language-(.*?)">(.*?)</code></pre>', re.DOTALL)
        html = pattern.sub(self._highlight_code, html)
        
        return html
    
    def _highlight_code(self, match):
        language = match.group(1)
        code = match.group(2)
        
        try:
            lexer = get_lexer_by_name(language, stripall=True)
        except:
            lexer = get_lexer_by_name('text', stripall=True)
            
        formatter = HtmlFormatter(style='default', cssclass='codehilite')
        return highlight(code, lexer, formatter)
    
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
            'markdown.extensions.codehilite',
            'markdown.extensions.fenced_code',
        ]

        html = markdown.markdown(self.text, extensions=extensions)

        # Apply Pygments syntax highlighting with VS Code style
        pattern = re.compile(r'<pre><code class="language-(.*?)">(.*?)</code></pre>', re.DOTALL)
        html = pattern.sub(self._highlight_code, html)

        return html

    def _highlight_code(self, match):
        language = match.group(1)
        code = match.group(2)

        try:
            lexer = get_lexer_by_name(language, stripall=True)
        except:
            lexer = get_lexer_by_name('text', stripall=True)

        formatter = HtmlFormatter(style='monokai', cssclass='codehilite')
        return highlight(code, lexer, formatter)