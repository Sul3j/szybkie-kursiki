from django.contrib import admin
from .models import Tag, Course, Lesson, LessonContent, Quiz, PracticalTask, Question, Answer, BlogPost, VideoPlaylist
from .forms import CourseForm
from django.utils.html import format_html
from django import forms
from django.db import models
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import messages
import xml.etree.ElementTree as ET

admin.site.site_header = "Panel Administracyjny Szybkie Kurski"
admin.site.site_title = "Szybkie Kurski Admin"
admin.site.index_title = "Zarządzanie platformą Szybkie Kurski"

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    verbose_name = "Tag"
    verbose_name_plural = "Tagi"
    list_per_page = 20

class CourseAdmin(admin.ModelAdmin):
    form = CourseForm
    list_display = ('title', 'short_description', 'icon_preview', 'status_badge', 'created_at')
    list_filter = ('tags', 'is_active', 'created_at')
    search_fields = ('title', 'short_description', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    list_per_page = 20
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('title', 'slug', 'short_description', 'description', 'is_active')
        }),
        ('Wygląd', {
            'fields': ('icon',),
        }),
        ('Kategoryzacja', {
            'fields': ('tags',),
        }),
    )

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<i class="{}" style="font-size: 24px; color: #4361ee;"></i>', obj.icon)
        return '-'
    icon_preview.short_description = 'Ikona'

    def status_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 3px;">Aktywny</span>')
        return format_html('<span style="background-color: #dc3545; color: white; padding: 3px 10px; border-radius: 3px;">Nieaktywny</span>')
    status_badge.short_description = 'Status'

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        help_text = format_html(
            '<p style="margin-left: 200px; margin-top: -20px; color: #666;">'
            'Przykłady ikon: <code>fas fa-code</code>, <code>fab fa-python</code>, '
            '<code>fas fa-database</code><br>'
            'Pełna lista: <a href="https://fontawesome.com/icons" target="_blank">'
            'fontawesome.com/icons</a></p>'
        )
        
        for fieldset in fieldsets:
            if fieldset[0] == 'Wygląd':
                fieldset[1]['description'] = help_text
                
        return fieldsets
    
class LessonContentInline(admin.StackedInline):
    model = LessonContent
    extra = 1

class QuizInline(admin.StackedInline):
    model = Quiz
    extra = 0
    max_num = 1

class PracticalTaskInline(admin.StackedInline):
    model = PracticalTask
    extra = 0
    max_num = 1

class LessonAdminForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'
        widgets = {
            'content_markdown': forms.Textarea(attrs={'rows': 30, 'cols': 120}),
        }

class PracticalTaskInline(admin.StackedInline):
    model = PracticalTask
    extra = 0
    max_num = 1
    fieldsets = (
        (None, {
            'fields': ('title', 'slug')
        }),
        ('Treść zadania', {
            'fields': ('content_markdown',)
        }),
        ('Instrukcje', {
            'fields': ('instructions_markdown',),
            'classes': ('collapse',)
        }),
        ('Przykład', {
            'fields': ('example_markdown',),
            'classes': ('collapse',)
        }),
        ('Wskazówki', {
            'fields': ('hints_markdown',),
            'classes': ('collapse',)
        }),
        ('Rozwiązanie', {
            'fields': ('solution_markdown',),
            'classes': ('collapse',)
        }),
    )
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 20, 'cols': 120})},
    }

class LessonAdmin(admin.ModelAdmin):
    inlines = [LessonContentInline, QuizInline, PracticalTaskInline]
    form = LessonAdminForm
    list_display = ('title', 'course', 'order', 'has_quiz', 'has_task', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('title', 'course__title')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('course', 'order')
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('course', 'title', 'slug', 'order')
        }),
        ('Treść lekcji (Markdown)', {
            'fields': ('content_markdown',),
            'description': format_html(
                '<div style="background: #f0f8ff; padding: 15px; border-left: 4px solid #4361ee; margin-bottom: 20px;">'
                '<strong>Wskazówki dotyczące Markdown:</strong><br>'
                '• Bloki kodu: <code>```python\nprint("Hello")\n```</code><br>'
                '• Nagłówki: <code>## Nagłówek</code><br>'
                '• Listy: <code>- Element listy</code><br>'
                '• Pogrubienie: <code>**tekst**</code><br>'
                '• Kursywa: <code>*tekst*</code>'
                '</div>'
            )
        }),
    )

    def has_quiz(self, obj):
        try:
            if obj.quiz:
                return format_html('<span style="color: #28a745;">✓</span>')
        except:
            pass
        return format_html('<span style="color: #dc3545;">✗</span>')
    has_quiz.short_description = 'Quiz'

    def has_task(self, obj):
        try:
            if obj.practicaltask:
                return format_html('<span style="color: #28a745;">✓</span>')
        except:
            pass
        return format_html('<span style="color: #dc3545;">✗</span>')
    has_task.short_description = 'Zadanie'

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    min_num = 2
    max_num = 5
    verbose_name = "Odpowiedź"
    verbose_name_plural = "Odpowiedzi"
    fields = ('text', 'is_correct', 'order')

    class Media:
        css = {
            'all': ('admin/css/forms.css',)
        }

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('short_text', 'quiz', 'order', 'answer_count')
    list_filter = ('quiz',)
    ordering = ('quiz', 'order')
    list_per_page = 20
    search_fields = ('text', 'quiz__title')

    def short_text(self, obj):
        if len(obj.text) > 60:
            return obj.text[:60] + '...'
        return obj.text
    short_text.short_description = 'Pytanie'

    def answer_count(self, obj):
        count = obj.answers.count()
        correct = obj.answers.filter(is_correct=True).count()
        return format_html(
            '<span style="background: #e9ecef; padding: 2px 8px; border-radius: 3px;">'
            '{} odpowiedzi ({} poprawnych)'
            '</span>',
            count, correct
        )
    answer_count.short_description = 'Odpowiedzi'

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('title', 'lesson', 'question_count', 'created_at')
    search_fields = ('title', 'lesson__title', 'lesson__course__title')
    list_filter = ('lesson__course', 'created_at')
    list_per_page = 20
    date_hierarchy = 'created_at'

    def question_count(self, obj):
        count = obj.questions.count()
        color = '#28a745' if count > 0 else '#dc3545'
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 3px;">'
            '{} pytań'
            '</span>',
            color, count
        )
    question_count.short_description = 'Liczba pytań'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:quiz_id>/import-xml/', self.admin_site.admin_view(self.import_questions_xml), name='quiz_import_xml'),
        ]
        return custom_urls + urls

    def import_questions_xml(self, request, quiz_id):
        """View for importing questions from XML"""
        quiz = Quiz.objects.get(pk=quiz_id)

        if request.method == 'POST':
            xml_content = request.POST.get('xml_content', '')

            if not xml_content.strip():
                messages.error(request, 'Proszę wkleić kod XML.')
                return render(request, 'admin/quiz_import_xml.html', {'quiz': quiz})

            try:
                # Parse XML
                root = ET.fromstring(xml_content)

                if root.tag != 'questions':
                    messages.error(request, 'Nieprawidłowy format XML. Element główny musi być <questions>.')
                    return render(request, 'admin/quiz_import_xml.html', {'quiz': quiz, 'xml_content': xml_content})

                # Count questions to be imported
                question_count = 0

                # Process each question
                for question_elem in root.findall('question'):
                    # Get question attributes
                    order = int(question_elem.get('order', 0))

                    # Get question text
                    text_elem = question_elem.find('text')
                    if text_elem is None or not text_elem.text:
                        messages.warning(request, f'Pominięto pytanie bez tekstu (order={order}).')
                        continue

                    text = text_elem.text.strip()

                    # Get explanation (optional)
                    explanation_elem = question_elem.find('explanation')
                    explanation = explanation_elem.text.strip() if explanation_elem is not None and explanation_elem.text else ''

                    # Create question
                    question = Question.objects.create(
                        quiz=quiz,
                        text=text,
                        order=order,
                        explanation=explanation
                    )

                    # Process answers
                    answers_elem = question_elem.find('answers')
                    if answers_elem is None:
                        messages.warning(request, f'Pytanie "{text[:50]}..." nie ma odpowiedzi.')
                        question.delete()
                        continue

                    answer_count = 0
                    for answer_elem in answers_elem.findall('answer'):
                        if answer_elem.text:
                            answer_text = answer_elem.text.strip()
                            is_correct = answer_elem.get('correct', 'false').lower() == 'true'
                            answer_order = int(answer_elem.get('order', 0))

                            Answer.objects.create(
                                question=question,
                                text=answer_text,
                                is_correct=is_correct,
                                order=answer_order
                            )
                            answer_count += 1

                    if answer_count == 0:
                        messages.warning(request, f'Pytanie "{text[:50]}..." nie ma odpowiedzi. Pytanie zostało usunięte.')
                        question.delete()
                    else:
                        question_count += 1

                if question_count > 0:
                    messages.success(request, f'Pomyślnie zaimportowano {question_count} pytań do quizu "{quiz.title}".')
                else:
                    messages.warning(request, 'Nie zaimportowano żadnych pytań.')

                return redirect('admin:main_app_quiz_change', quiz_id)

            except ET.ParseError as e:
                messages.error(request, f'Błąd parsowania XML: {str(e)}')
                return render(request, 'admin/quiz_import_xml.html', {'quiz': quiz, 'xml_content': xml_content})
            except Exception as e:
                messages.error(request, f'Wystąpił błąd podczas importu: {str(e)}')
                return render(request, 'admin/quiz_import_xml.html', {'quiz': quiz, 'xml_content': xml_content})

        # GET request - show form
        xml_example = '''<?xml version="1.0" encoding="UTF-8"?>
<questions>
  <question order="1">
    <text>Jakie jest znaczenie operatora == w Pythonie?</text>
    <explanation>Operator == porównuje wartości dwóch obiektów, a nie ich tożsamość.</explanation>
    <answers>
      <answer correct="true" order="1">Porównuje wartości dwóch obiektów</answer>
      <answer correct="false" order="2">Przypisuje wartość do zmiennej</answer>
      <answer correct="false" order="3">Sprawdza typ obiektu</answer>
      <answer correct="false" order="4">Tworzy nowy obiekt</answer>
    </answers>
  </question>
  <question order="2">
    <text>Który z poniższych typów danych jest niezmienny (immutable) w Pythonie?</text>
    <explanation>Tuple jest typem niemutowalnym, co oznacza, że po utworzeniu nie można zmienić jego elementów.</explanation>
    <answers>
      <answer correct="false" order="1">List</answer>
      <answer correct="true" order="2">Tuple</answer>
      <answer correct="false" order="3">Dictionary</answer>
      <answer correct="false" order="4">Set</answer>
    </answers>
  </question>
</questions>'''

        return render(request, 'admin/quiz_import_xml.html', {
            'quiz': quiz,
            'xml_example': xml_example,
        })

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Override change view to add import XML button"""
        extra_context = extra_context or {}
        extra_context['show_import_xml'] = True
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

class PracticalTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'has_sections')
    search_fields = ('title', 'lesson__title', 'lesson__course__title')
    list_filter = ('lesson__course',)
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20
    readonly_fields = (
        'content_html',
        'instructions_html',
        'example_html',
        'hints_html',
        'solution_html'
    )

    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('lesson', 'title', 'slug')
        }),
        ('Treść zadania (Markdown)', {
            'fields': ('content_markdown', 'content_html'),
            'description': 'Główna treść zadania praktycznego'
        }),
        ('Instrukcje (Markdown)', {
            'fields': ('instructions_markdown', 'instructions_html'),
            'classes': ('collapse',),
            'description': 'Szczegółowe instrukcje wykonania zadania'
        }),
        ('Przykład (Markdown)', {
            'fields': ('example_markdown', 'example_html'),
            'classes': ('collapse',),
            'description': 'Przykładowe rozwiązanie lub dane testowe'
        }),
        ('Wskazówki (Markdown)', {
            'fields': ('hints_markdown', 'hints_html'),
            'classes': ('collapse',),
            'description': 'Wskazówki pomagające w rozwiązaniu zadania'
        }),
        ('Rozwiązanie (Markdown)', {
            'fields': ('solution_markdown', 'solution_html'),
            'classes': ('collapse',),
            'description': 'Pełne rozwiązanie zadania'
        }),
    )

    def has_sections(self, obj):
        sections = []
        if obj.instructions_markdown: sections.append('Instrukcje')
        if obj.example_markdown: sections.append('Przykład')
        if obj.hints_markdown: sections.append('Wskazówki')
        if obj.solution_markdown: sections.append('Rozwiązanie')

        if sections:
            return format_html('<span style="color: #28a745;">{}</span>', ', '.join(sections))
        return format_html('<span style="color: #dc3545;">Brak dodatkowych sekcji</span>')
    has_sections.short_description = 'Sekcje'
    
class BlogPostAdminForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = '__all__'
        widgets = {
            'content_markdown': forms.Textarea(attrs={'rows': 30, 'cols': 120}),
            'short_description': forms.Textarea(attrs={'rows': 3, 'cols': 80}),
        }

class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    list_display = ('title', 'author_name', 'published_date', 'status_badge', 'created_at')
    list_filter = ('is_published', 'published_date', 'author_name', 'created_at')
    search_fields = ('title', 'short_description', 'author_name')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    list_per_page = 20

    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('title', 'slug', 'author_name', 'published_date', 'is_published')
        }),
        ('Krótki opis', {
            'fields': ('short_description',),
            'description': 'Krótki opis widoczny na liście postów (max 300 znaków)'
        }),
        ('Treść posta (Markdown)', {
            'fields': ('content_markdown',),
            'description': format_html(
                '<div style="background: #f0f8ff; padding: 15px; border-left: 4px solid #4361ee; margin-bottom: 20px;">'
                '<strong>Wskazówki dotyczące Markdown:</strong><br>'
                '• Bloki kodu: <code>```python\nprint("Hello")\n```</code><br>'
                '• Nagłówki: <code>## Nagłówek</code>, <code>### Podtytuł</code><br>'
                '• Obrazki: <code>![alt text](url)</code><br>'
                '• Linki: <code>[tekst](url)</code><br>'
                '• Listy: <code>- Element listy</code>'
                '</div>'
            )
        }),
    )

    def status_badge(self, obj):
        if obj.is_published:
            return format_html('<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 3px;">Opublikowany</span>')
        return format_html('<span style="background-color: #6c757d; color: white; padding: 3px 10px; border-radius: 3px;">Szkic</span>')
    status_badge.short_description = 'Status'

class VideoPlaylistAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'status_badge', 'thumbnail_preview', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order',)
    list_per_page = 20
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('title', 'slug', 'description', 'order', 'is_active')
        }),
        ('Zawartość multimiedialna', {
            'fields': ('thumbnail', 'youtube_playlist_url'),
            'description': format_html(
                '<div style="background: #fff3cd; padding: 15px; border-left: 4px solid #ffb703; margin-bottom: 20px;">'
                '<strong>Wymagania:</strong><br>'
                '• Miniaturka: Zalecany rozmiar 1280x720px (16:9)<br>'
                '• Link YouTube: Pełny URL do playlisty YouTube<br>'
                '• Format: https://www.youtube.com/playlist?list=...'
                '</div>'
            )
        }),
    )

    def status_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 3px;">Aktywny</span>')
        return format_html('<span style="background-color: #dc3545; color: white; padding: 3px 10px; border-radius: 3px;">Nieaktywny</span>')
    status_badge.short_description = 'Status'

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="max-height: 50px; border-radius: 5px;" />', obj.thumbnail.url)
        return '-'
    thumbnail_preview.short_description = 'Miniaturka'

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(PracticalTask, PracticalTaskAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(VideoPlaylist, VideoPlaylistAdmin)








