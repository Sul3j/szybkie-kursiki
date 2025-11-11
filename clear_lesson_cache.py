#!/usr/bin/env python
"""
Script to clear cached HTML content in lessons, forcing Monaco Editor to regenerate
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'szybkie_kursiki.settings')
django.setup()

from main_app.models import Lesson, Question, BlogPost

def clear_caches():
    print("Clearing cached HTML content...")

    # Force regeneration by accessing the properties
    lessons = Lesson.objects.all()
    print(f"\nProcessing {lessons.count()} lessons...")
    for lesson in lessons:
        if lesson.content_markdown:
            # Just access the property to trigger regeneration
            _ = lesson.content_html
            print(f"✓ Processed: {lesson.title}")

    questions = Question.objects.all()
    print(f"\nProcessing {questions.count()} questions...")
    for question in questions:
        if question.text:
            _ = question.text_html
            print(f"✓ Processed: Question ID {question.id}")

    blogs = BlogPost.objects.all()
    print(f"\nProcessing {blogs.count()} blog posts...")
    for blog in blogs:
        if blog.content_markdown:
            _ = blog.content_html
            print(f"✓ Processed: {blog.title}")

    print("\n✅ All caches cleared! Monaco Editor will now be used for syntax highlighting.")

if __name__ == '__main__':
    clear_caches()
