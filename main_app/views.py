from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Tag, Lesson, Quiz, Answer, BlogPost, VideoPlaylist

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
        Lesson.objects.select_related('course', 'quiz'),
        course__slug=course_slug,
        slug=lesson_slug
    )
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
        Lesson.objects.select_related('course', 'quiz'),
        course__slug=course_slug,
        slug=lesson_slug
    )
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
        Lesson.objects.select_related('course', 'practicaltask'),
        course__slug=course_slug,
        slug=lesson_slug,
        course__is_active=True
    )
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

