from main_app.models import Lesson

lesson = Lesson.objects.filter(content_markdown__contains='```').first()
if lesson:
    print(f'Lesson: {lesson.title}')
    print(f'Course: {lesson.course.slug}')
    print(f'Slug: {lesson.slug}')

    html = lesson.content_html
    has_monaco = 'monaco-code-block' in html
    has_pygments = 'codehilite' in html and 'monaco' not in html

    print(f'\nHas Monaco: {has_monaco}')
    print(f'Has Pygments: {has_pygments}')

    if has_monaco:
        count = html.count('monaco-code-block')
        print(f'Monaco blocks: {count}')

        # Extract first monaco block
        import re
        match = re.search(r'<div class="monaco-code-block"[^>]*>', html)
        if match:
            print(f'\nExample:\n{match.group()}')
    else:
        print('\n❌ NO MONACO FOUND!')
        print(f'First 500 chars of HTML:\n{html[:500]}')
else:
    print('No lesson with code blocks found')
