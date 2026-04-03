import json
import os
import logging

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
from .models import Course, Tag, Lesson, Quiz, Question, Answer, PracticalTask, BlogPost, VideoPlaylist, Project

logger = logging.getLogger(__name__)

def home(request):
    # Optimize with prefetch_related to avoid N+1 queries
    featured_courses = Course.objects.filter(
        is_active=True
    ).prefetch_related('tags').order_by('-created_at')[:3]

    recent_posts = BlogPost.objects.filter(
        is_published=True
    ).only('id', 'title', 'slug', 'short_description', 'published_date').order_by('-published_date')[:6]

    video_playlists = VideoPlaylist.objects.filter(
        is_active=True
    ).only('id', 'title', 'youtube_playlist_url', 'thumbnail', 'description', 'order').order_by('order', '-created_at')[:6]

    projects = Project.objects.filter(
        is_active=True
    ).order_by('order', '-created_at')[:6]

    # Calculate real statistics for hero section (cached for performance)
    from django.core.cache import cache

    total_courses = cache.get('stats_total_courses')
    if total_courses is None:
        total_courses = Course.objects.filter(is_active=True).count()
        cache.set('stats_total_courses', total_courses, 3600)  # Cache for 1 hour

    total_lessons = cache.get('stats_total_lessons')
    if total_lessons is None:
        total_lessons = Lesson.objects.filter(course__is_active=True).count()
        cache.set('stats_total_lessons', total_lessons, 3600)

    total_quizzes = cache.get('stats_total_quizzes')
    if total_quizzes is None:
        total_quizzes = Quiz.objects.filter(lesson__course__is_active=True).count()
        cache.set('stats_total_quizzes', total_quizzes, 3600)

    return render(request, 'main_app/index.html', {
        'featured_courses': featured_courses,
        'recent_posts': recent_posts,
        'video_playlists': video_playlists,
        'projects': projects,
        'total_courses': total_courses,
        'total_lessons': total_lessons,
        'total_quizzes': total_quizzes,
        'is_home_page': True
    })

def courses(request):
    active_courses = Course.objects.filter(is_active=True).prefetch_related('tags')
    all_tags = Tag.objects.all()
    
    return render(request, 'main_app/courses.html', {
        'courses': active_courses,
        'tags': all_tags,
        'is_home_page': False
    })

def course_detail(request, slug):
    # Optimize with prefetch_related for tags and lessons
    course = get_object_or_404(
        Course.objects.prefetch_related('tags', 'lessons'),
        slug=slug,
        is_active=True
    )

    # Optimize suggested courses query
    suggested_courses = Course.objects.filter(
        tags__in=course.tags.all(),
        is_active=True
    ).exclude(
        id=course.id
    ).prefetch_related('tags').distinct()[:3]

    return render(request, 'main_app/course_detail.html', {
        'course': course,
        'suggested_courses': suggested_courses,
        'is_home_page': False
    })

def course_lessons(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug, is_active=True)
    lessons = course.lessons.all().order_by('order')
    return render(request, 'main_app/course_lessons.html', {
        'course': course,
        'lessons': lessons,
        'is_home_page': False
    })

def lesson_detail(request, course_slug, lesson_slug):
    # Optimize with select_related to avoid extra query for course
    lesson = get_object_or_404(
        Lesson.objects.select_related('course'),
        course__slug=course_slug,
        slug=lesson_slug,
        course__is_active=True
    )
    return render(request, 'main_app/lesson_detail.html', {
        'course': lesson.course,
        'lesson': lesson,
        'is_home_page': False
    })

def quiz_detail(request, course_slug, lesson_slug):
    # Optimize with select_related and prefetch_related
    lesson = get_object_or_404(
        Lesson.objects.select_related('course'),
        course__slug=course_slug,
        slug=lesson_slug
    )

    # Check if quiz exists
    if not hasattr(lesson, 'quiz'):
        from django.http import Http404
        raise Http404("Quiz does not exist for this lesson")

    quiz = lesson.quiz
    questions = quiz.questions.prefetch_related('answers').order_by('order')

    return render(request, 'main_app/quiz_detail.html', {
        'course': lesson.course,
        'lesson': lesson,
        'quiz': quiz,
        'questions': questions,
        'is_home_page': False
    })

def quiz_submit(request, course_slug, lesson_slug):
    if request.method != 'POST':
        return redirect('quiz_detail', course_slug=course_slug, lesson_slug=lesson_slug)

    # Optimize with select_related
    lesson = get_object_or_404(
        Lesson.objects.select_related('course'),
        course__slug=course_slug,
        slug=lesson_slug
    )

    # Check if quiz exists
    if not hasattr(lesson, 'quiz'):
        from django.http import Http404
        raise Http404("Quiz does not exist for this lesson")

    quiz = lesson.quiz
    questions = quiz.questions.prefetch_related('answers').order_by('order')

    # Create a dictionary of all answers for O(1) lookup instead of querying in loop
    all_answer_ids = [request.POST.get(f'question_{q.id}') for q in questions if request.POST.get(f'question_{q.id}')]
    answers_dict = {
        str(answer.id): answer
        for answer in Answer.objects.filter(id__in=all_answer_ids).select_related('question')
    }

    total_questions = len(questions)
    correct_answers = 0
    results = []

    for question in questions:
        selected_answer_id = request.POST.get(f'question_{question.id}')
        selected_answer = None
        is_correct = False

        if selected_answer_id and selected_answer_id in answers_dict:
            selected_answer = answers_dict[selected_answer_id]
            is_correct = selected_answer.is_correct
            if is_correct:
                correct_answers += 1

        # Use prefetched answers instead of filter
        correct_answer = next((a for a in question.answers.all() if a.is_correct), None)

        results.append({
            'question': question,
            'selected_answer': selected_answer,
            'is_correct': is_correct,
            'correct_answer': correct_answer
        })

    score = round((correct_answers / total_questions) * 100) if total_questions > 0 else 0
    incorrect_answers = total_questions - correct_answers

    return render(request, 'main_app/quiz_result.html', {
        'course': lesson.course,
        'lesson': lesson,
        'quiz': quiz,
        'results': results,
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
        'score': score,
        'is_home_page': False
    })

def practical_task_detail(request, course_slug, lesson_slug):
    # Optimize with select_related
    lesson = get_object_or_404(
        Lesson.objects.select_related('course'),
        course__slug=course_slug,
        slug=lesson_slug,
        course__is_active=True
    )

    # Check if practical task exists
    if not hasattr(lesson, 'practicaltask'):
        from django.http import Http404
        raise Http404("Practical task does not exist for this lesson")

    task = lesson.practicaltask

    pygments_css = "monokai"

    return render(request, 'main_app/practical_task_detail.html', {
        'course': lesson.course,
        'lesson': lesson,
        'task': task,
        'pygments_style': pygments_css,
        'is_home_page': False
    })

def blog_post_detail(request, slug):
    blog_post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    return render(request, 'main_app/blog_post_detail.html', {
        'blog_post': blog_post,
        'is_home_page': False
    })


def _unique_slug(base_slug, model_class, exclude_id=None):
    slug = base_slug
    counter = 1
    qs = model_class.objects.filter(slug=slug)
    if exclude_id:
        qs = qs.exclude(id=exclude_id)
    while qs.exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
        qs = model_class.objects.filter(slug=slug)
        if exclude_id:
            qs = qs.exclude(id=exclude_id)
    return slug


@csrf_exempt
def import_course(request):
    # Log incoming request details for debugging
    logger.info(f"Import course endpoint called - Method: {request.method}, Path: {request.path}, Content-Type: {request.content_type}")

    if request.method != 'POST':
        logger.warning(f"Method not allowed: {request.method} (expected POST)")
        return JsonResponse({
            'error': 'Method not allowed',
            'received_method': request.method,
            'expected_method': 'POST'
        }, status=405)

    token = request.headers.get('X-Import-Token', '')
    expected_token = os.environ.get('COURSE_IMPORT_TOKEN', '')
    if not expected_token or token != expected_token:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    try:
        course_data = data.get('course', {})
        lessons_data = data.get('lessons', [])

        if not course_data.get('title') or not lessons_data:
            return JsonResponse({'error': 'Missing course title or lessons'}, status=400)

        # Create or get tags
        tags = []
        for tag_name in course_data.get('tags', []):
            tag_slug = slugify(tag_name)
            tag, _ = Tag.objects.get_or_create(
                slug=tag_slug,
                defaults={'name': tag_name}
            )
            tags.append(tag)

        # Create course as draft (is_active=False)
        course_slug = _unique_slug(
            slugify(course_data['title']),
            Course
        )
        course = Course.objects.create(
            title=course_data['title'],
            slug=course_slug,
            short_description=course_data.get('short_description', ''),
            description=course_data.get('description', ''),
            icon=course_data.get('icon', 'fas fa-code'),
            is_active=False,
        )
        course.tags.set(tags)

        # Create lessons with quizzes and tasks
        for lesson_data in lessons_data:
            lesson_slug = _unique_slug(
                slugify(lesson_data.get('title', 'lekcja')),
                Lesson
            )
            lesson = Lesson.objects.create(
                course=course,
                title=lesson_data['title'],
                slug=lesson_slug,
                order=lesson_data.get('order', 0),
                content_markdown=lesson_data.get('content_markdown', ''),
            )

            # Create quiz if provided
            quiz_data = lesson_data.get('quiz')
            if quiz_data and quiz_data.get('questions'):
                quiz = Quiz.objects.create(
                    lesson=lesson,
                    title=quiz_data.get('title', f'Quiz - {lesson.title}'),
                    description=quiz_data.get('description', ''),
                )
                for q_idx, q_data in enumerate(quiz_data['questions']):
                    question = Question.objects.create(
                        quiz=quiz,
                        text=q_data.get('text', ''),
                        order=q_data.get('order', q_idx),
                        explanation=q_data.get('explanation', ''),
                    )
                    for a_idx, a_data in enumerate(q_data.get('answers', [])):
                        Answer.objects.create(
                            question=question,
                            text=a_data.get('text', ''),
                            is_correct=a_data.get('is_correct', False),
                            order=a_data.get('order', a_idx),
                        )

            # Create practical task if provided
            task_data = lesson_data.get('practical_task')
            if task_data and task_data.get('title'):
                task_slug = _unique_slug(
                    slugify(task_data.get('title', 'zadanie')),
                    PracticalTask
                )
                PracticalTask.objects.create(
                    lesson=lesson,
                    title=task_data['title'],
                    slug=task_slug,
                    content_markdown=task_data.get('content_markdown', ''),
                    instructions_markdown=task_data.get('instructions_markdown', ''),
                    example_markdown=task_data.get('example_markdown', ''),
                    hints_markdown=task_data.get('hints_markdown', ''),
                    solution_markdown=task_data.get('solution_markdown', ''),
                )

        logger.info(f"Imported draft course: {course.title} (slug: {course.slug})")

        return JsonResponse({
            'status': 'ok',
            'course_id': course.id,
            'course_slug': course.slug,
            'course_title': course.title,
            'lessons_count': len(lessons_data),
            'admin_url': f'/admin/main_app/course/{course.id}/change/',
        })

    except Exception as e:
        logger.error(f"Course import error: {e}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)
