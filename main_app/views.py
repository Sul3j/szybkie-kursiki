from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Tag, Lesson, Quiz, Answer, PracticalTask, BlogPost, VideoPlaylist

def home(request):
    featured_courses = Course.objects.filter(is_active=True).order_by('-created_at')[:3]
    recent_posts = BlogPost.objects.filter(is_published=True).order_by('-published_date')[:6]
    video_playlists = VideoPlaylist.objects.filter(is_active=True).order_by('order', '-created_at')[:6]
    return render(request, 'main_app/index.html', {
        'featured_courses': featured_courses,
        'recent_posts': recent_posts,
        'video_playlists': video_playlists,
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
    course = get_object_or_404(Course, slug=slug, is_active=True)
    
    suggested_courses = Course.objects.filter(
        tags__in=course.tags.all(),
        is_active=True
    ).exclude(
        id=course.id
    ).distinct()[:3]
    
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
    lesson = get_object_or_404(
        Lesson,
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
    lesson = get_object_or_404(Lesson, course__slug=course_slug, slug=lesson_slug)
    quiz = get_object_or_404(Quiz, lesson=lesson)
    questions = quiz.questions.all().prefetch_related('answers').order_by('order')
    
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
    
    lesson = get_object_or_404(Lesson, course__slug=course_slug, slug=lesson_slug)
    quiz = get_object_or_404(Quiz, lesson=lesson)
    questions = quiz.questions.all().prefetch_related('answers')
    
    total_questions = questions.count()
    correct_answers = 0
    results = []
    
    for question in questions:
        selected_answer_id = request.POST.get(f'question_{question.id}')
        selected_answer = None
        is_correct = False
        
        if selected_answer_id:
            try:
                selected_answer = Answer.objects.get(id=selected_answer_id)
                is_correct = selected_answer.is_correct
                if is_correct:
                    correct_answers += 1
            except Answer.DoesNotExist:
                pass
        
        correct_answer = question.answers.filter(is_correct=True).first()
        
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
    lesson = get_object_or_404(
        Lesson,
        course__slug=course_slug,
        slug=lesson_slug,
        course__is_active=True
    )
    task = get_object_or_404(PracticalTask, lesson=lesson)

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

