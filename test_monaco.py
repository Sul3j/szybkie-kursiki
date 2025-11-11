#!/usr/bin/env python
import os
import django
import re
import html

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'szybkie_kursiki.settings')
django.setup()

from main_app.models import Lesson

# Test the highlighting function directly
def test_highlight():
    print("Testing Monaco Editor integration...\n")

    # Create a mock match object for testing
    class MockMatch:
        def group(self, n):
            if n == 1:
                return "python"
            elif n == 2:
                return 'print("Hello World")'

    lesson = Lesson.objects.first()
    if not lesson:
        print("No lesson found in database")
        return

    match = MockMatch()
    result = lesson._highlight_code(match)

    print("Result from _highlight_code:")
    print(result)
    print()

    if 'monaco-code-block' in result:
        print("✅ SUCCESS: Method returns Monaco HTML!")
    else:
        print("❌ FAIL: Method doesn't return Monaco HTML")

    # Now check actual lesson content
    print("\n" + "="*60)
    print("Checking actual lesson content...")
    print("="*60 + "\n")

    lessons_with_code = Lesson.objects.filter(content_markdown__contains='```')[:3]
    for lesson in lessons_with_code:
        print(f"\nLesson: {lesson.title}")
        html_content = lesson.content_html

        if 'monaco-code-block' in html_content:
            print("  ✅ Contains monaco-code-block")
            # Count how many
            count = html_content.count('monaco-code-block')
            print(f"  Found {count} Monaco code blocks")
        elif 'codehilite' in html_content:
            print("  ❌ Still using codehilite")
        else:
            print("  ⚠️ No code blocks")

if __name__ == '__main__':
    test_highlight()
