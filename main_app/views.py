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