from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.courses, name='courses'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<slug:course_slug>/', views.course_lessons, name='course_lessons'),
    path('course/<slug:course_slug>/<slug:lesson_slug>/', views.lesson_detail, name='lesson_detail'),
    path('course/<slug:course_slug>/<slug:lesson_slug>/quiz/', views.quiz_detail, name='quiz_detail'),
    path('course/<slug:course_slug>/<slug:lesson_slug>/quiz/submit/', views.quiz_submit, name='quiz_submit'),
    path('course/<slug:course_slug>/<slug:lesson_slug>/task/', views.practical_task_detail, name='practical_task_detail'),
    path('blog/<slug:slug>/', views.blog_post_detail, name='blog_post_detail'),
]



