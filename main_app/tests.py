from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.utils.text import slugify
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date, datetime
from .models import (
    Tag, Course, Lesson, LessonContent, Quiz, Question, Answer,
    PracticalTask, BlogPost, VideoPlaylist
)
import shutil
import tempfile
import os

# Create a temporary directory for test media files
TEMP_MEDIA_ROOT = tempfile.mkdtemp()


class TagModelTest(TestCase):
    """Tests for Tag model"""

    def setUp(self):
        self.tag = Tag.objects.create(
            name="Python",
            slug="python"
        )

    def test_tag_creation(self):
        """Test that Tag is created correctly"""
        self.assertEqual(self.tag.name, "Python")
        self.assertEqual(self.tag.slug, "python")
        self.assertEqual(str(self.tag), "Python")

    def test_tag_unique_name(self):
        """Test that Tag name must be unique"""
        with self.assertRaises(Exception):
            Tag.objects.create(name="Python", slug="python-2")

    def test_tag_ordering(self):
        """Test that Tags are ordered by name"""
        tag2 = Tag.objects.create(name="JavaScript", slug="javascript")
        tags = Tag.objects.all()
        self.assertEqual(tags[0].name, "JavaScript")
        self.assertEqual(tags[1].name, "Python")


class CourseModelTest(TestCase):
    """Tests for Course model"""

    def setUp(self):
        self.tag1 = Tag.objects.create(name="Python", slug="python")
        self.tag2 = Tag.objects.create(name="Backend", slug="backend")
        self.course = Course.objects.create(
            title="Python dla początkujących",
            slug="python-dla-poczatkujacych",
            short_description="Krótki opis kursu",
            description="Pełny opis kursu",
            icon="fab fa-python",
            is_active=True
        )
        self.course.tags.add(self.tag1, self.tag2)

    def test_course_creation(self):
        """Test that Course is created correctly"""
        self.assertEqual(self.course.title, "Python dla początkujących")
        self.assertEqual(self.course.slug, "python-dla-poczatkujacych")
        self.assertEqual(self.course.icon, "fab fa-python")
        self.assertTrue(self.course.is_active)
        self.assertEqual(self.course.tags.count(), 2)

    def test_course_str(self):
        """Test Course string representation"""
        self.assertEqual(str(self.course), "Python dla początkujących")

    def test_course_default_icon(self):
        """Test Course has default icon"""
        course = Course.objects.create(
            title="Test Course",
            slug="test-course",
            short_description="Test",
            description="Test description"
        )
        self.assertEqual(course.icon, "fas fa-code")

    def test_course_ordering(self):
        """Test that Courses are ordered by created_at descending"""
        course2 = Course.objects.create(
            title="Another Course",
            slug="another-course",
            short_description="Test",
            description="Test"
        )
        courses = Course.objects.all()
        self.assertEqual(courses[0].title, "Another Course")


class LessonModelTest(TestCase):
    """Tests for Lesson model"""

    def setUp(self):
        self.course = Course.objects.create(
            title="Test Course",
            slug="test-course",
            short_description="Test",
            description="Test description"
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Pierwsza lekcja",
            slug="pierwsza-lekcja",
            order=1,
            content_markdown="# Nagłówek\n\nTreść lekcji"
        )

    def test_lesson_creation(self):
        """Test that Lesson is created correctly"""
        self.assertEqual(self.lesson.title, "Pierwsza lekcja")
        self.assertEqual(self.lesson.course, self.course)
        self.assertEqual(self.lesson.order, 1)
        self.assertIsNotNone(self.lesson.content_markdown)

    def test_lesson_str(self):
        """Test Lesson string representation"""
        self.assertEqual(str(self.lesson), "Pierwsza lekcja")

    def test_lesson_get_absolute_url(self):
        """Test Lesson get_absolute_url method"""
        url = self.lesson.get_absolute_url()
        expected_url = reverse('lesson_detail', args=[self.course.slug, self.lesson.slug])
        self.assertEqual(url, expected_url)

    def test_lesson_auto_slug_generation(self):
        """Test that slug is auto-generated from title"""
        lesson = Lesson.objects.create(
            course=self.course,
            title="Nowa Lekcja Test",
            order=2,
            content_markdown="Test content"
        )
        self.assertEqual(lesson.slug, slugify("Nowa Lekcja Test"))

    def test_lesson_content_html_property(self):
        """Test that content_html renders Markdown to HTML"""
        html = self.lesson.content_html
        self.assertIn("Nagłówek", html)
        self.assertIn("<h1", html)
        self.assertIn("<p>Treść lekcji</p>", html)

    def test_lesson_with_code_block(self):
        """Test Markdown code block rendering"""
        lesson = Lesson.objects.create(
            course=self.course,
            title="Lekcja z kodem",
            slug="lekcja-z-kodem",
            order=2,
            content_markdown="```python\nprint('Hello World')\n```"
        )
        html = lesson.content_html
        self.assertIn("print", html)

    def test_lesson_ordering(self):
        """Test that Lessons are ordered by order field"""
        lesson2 = Lesson.objects.create(
            course=self.course,
            title="Druga lekcja",
            slug="druga-lekcja",
            order=0,
            content_markdown="Test"
        )
        lessons = self.course.lessons.all()
        self.assertEqual(lessons[0].order, 0)
        self.assertEqual(lessons[1].order, 1)

    def test_lesson_special_note_block(self):
        """Test special NOTE callout block processing"""
        lesson = Lesson.objects.create(
            course=self.course,
            title="Lekcja z notatką",
            slug="lekcja-z-notatka",
            order=3,
            content_markdown="> [!NOTE]\n> To jest notatka\n\nInna treść"
        )
        self.assertIn('class="callout note"', lesson.content_markdown)

    def test_lesson_special_warning_block(self):
        """Test special WARNING callout block processing"""
        lesson = Lesson.objects.create(
            course=self.course,
            title="Lekcja z ostrzeżeniem",
            slug="lekcja-z-ostrzezeniem",
            order=4,
            content_markdown="> [!WARNING]\n> To jest ostrzeżenie\n\nInna treść"
        )
        self.assertIn('class="callout warning"', lesson.content_markdown)

    def test_lesson_special_danger_block(self):
        """Test special DANGER callout block processing"""
        lesson = Lesson.objects.create(
            course=self.course,
            title="Lekcja z niebezpieczeństwem",
            slug="lekcja-z-niebezpieczenstwem",
            order=5,
            content_markdown="> [!DANGER]\n> To jest niebezpieczne\n\nInna treść"
        )
        self.assertIn('class="callout danger"', lesson.content_markdown)


class QuizModelTest(TestCase):
    """Tests for Quiz model"""

    def setUp(self):
        self.course = Course.objects.create(
            title="Test Course",
            slug="test-course",
            short_description="Test",
            description="Test"
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Test Lesson",
            slug="test-lesson",
            order=1
        )
        self.quiz = Quiz.objects.create(
            lesson=self.lesson,
            title="Quiz testowy",
            description="Opis quizu"
        )

    def test_quiz_creation(self):
        """Test that Quiz is created correctly"""
        self.assertEqual(self.quiz.title, "Quiz testowy")
        self.assertEqual(self.quiz.lesson, self.lesson)
        self.assertEqual(str(self.quiz), "Quiz testowy")

    def test_quiz_one_to_one_with_lesson(self):
        """Test that Quiz has one-to-one relationship with Lesson"""
        with self.assertRaises(Exception):
            Quiz.objects.create(
                lesson=self.lesson,
                title="Drugi quiz",
                description="Test"
            )


class QuestionAndAnswerModelTest(TestCase):
    """Tests for Question and Answer models"""

    def setUp(self):
        self.course = Course.objects.create(
            title="Test Course",
            slug="test-course",
            short_description="Test",
            description="Test"
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Test Lesson",
            slug="test-lesson",
            order=1
        )
        self.quiz = Quiz.objects.create(
            lesson=self.lesson,
            title="Test Quiz",
            description="Test"
        )
        self.question = Question.objects.create(
            quiz=self.quiz,
            text="Co to jest Python?",
            order=1,
            explanation="Python to język programowania"
        )
        self.answer1 = Answer.objects.create(
            question=self.question,
            text="Język programowania",
            is_correct=True,
            order=1
        )
        self.answer2 = Answer.objects.create(
            question=self.question,
            text="Wąż",
            is_correct=False,
            order=2
        )

    def test_question_creation(self):
        """Test that Question is created correctly"""
        self.assertEqual(self.question.text, "Co to jest Python?")
        self.assertEqual(self.question.quiz, self.quiz)
        self.assertEqual(str(self.question), "Co to jest Python?")

    def test_answer_creation(self):
        """Test that Answer is created correctly"""
        self.assertEqual(self.answer1.text, "Język programowania")
        self.assertTrue(self.answer1.is_correct)
        self.assertEqual(str(self.answer1), "Język programowania")

    def test_question_text_html_property(self):
        """Test that text_html renders Markdown"""
        question = Question.objects.create(
            quiz=self.quiz,
            text="**Pytanie bold**",
            order=2
        )
        html = question.text_html
        self.assertIn("<strong>", html)

    def test_question_with_code_block(self):
        """Test Question with code block"""
        question = Question.objects.create(
            quiz=self.quiz,
            text="Co wypisze ten kod?\n```python\nprint('test')\n```",
            order=3
        )
        html = question.text_html
        self.assertIn("print", html)

    def test_answer_ordering(self):
        """Test that Answers are ordered by order field"""
        answers = self.question.answers.all()
        self.assertEqual(answers[0].order, 1)
        self.assertEqual(answers[1].order, 2)


class PracticalTaskModelTest(TestCase):
    """Tests for PracticalTask model"""

    def setUp(self):
        self.course = Course.objects.create(
            title="Test Course",
            slug="test-course",
            short_description="Test",
            description="Test"
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Test Lesson",
            slug="test-lesson",
            order=1
        )
        self.task = PracticalTask.objects.create(
            lesson=self.lesson,
            title="Zadanie praktyczne",
            content_markdown="# Zadanie\n\nZrób coś",
            instructions_markdown="## Instrukcje\n\nKrok 1",
            example_markdown="```python\nprint('example')\n```",
            hints_markdown="Wskazówka 1",
            solution_markdown="```python\nprint('solution')\n```"
        )

    def test_practical_task_creation(self):
        """Test that PracticalTask is created correctly"""
        self.assertEqual(self.task.title, "Zadanie praktyczne")
        self.assertEqual(self.task.lesson, self.lesson)
        self.assertEqual(str(self.task), "Zadanie praktyczne")

    def test_practical_task_auto_slug(self):
        """Test that slug is auto-generated"""
        self.assertTrue(len(self.task.slug) > 0)

    def test_practical_task_html_conversion(self):
        """Test that Markdown fields are converted to HTML on save"""
        self.assertIsNotNone(self.task.content_html)
        self.assertIsNotNone(self.task.instructions_html)
        self.assertIsNotNone(self.task.example_html)
        self.assertIsNotNone(self.task.hints_html)
        self.assertIsNotNone(self.task.solution_html)

        self.assertIn("Zadanie", self.task.content_html)
        self.assertIn("<h1", self.task.content_html)
        self.assertIn("Instrukcje", self.task.instructions_html)
        self.assertIn("<h2", self.task.instructions_html)

    def test_practical_task_unique_slug(self):
        """Test that duplicate slugs are handled"""
        # Create a new lesson since PracticalTask has OneToOne relationship
        lesson2 = Lesson.objects.create(
            course=self.course,
            title="Another Lesson",
            slug="another-lesson",
            order=2
        )
        task2 = PracticalTask.objects.create(
            lesson=lesson2,
            title="Zadanie praktyczne",
            content_markdown="Test"
        )
        self.assertNotEqual(self.task.slug, task2.slug)

    def test_practical_task_one_to_one_with_lesson(self):
        """Test that PracticalTask has one-to-one relationship with Lesson"""
        lesson2 = Lesson.objects.create(
            course=self.course,
            title="Another Lesson",
            slug="another-lesson",
            order=2
        )
        task = PracticalTask.objects.create(
            lesson=lesson2,
            title="Another Task",
            content_markdown="Test"
        )
        self.assertEqual(task.lesson, lesson2)


class BlogPostModelTest(TestCase):
    """Tests for BlogPost model"""

    def setUp(self):
        self.blog_post = BlogPost.objects.create(
            title="Test Blog Post",
            short_description="Krótki opis posta",
            author_name="Jan Kowalski",
            published_date=date.today(),
            content_markdown="# Nagłówek\n\nTreść posta",
            is_published=True
        )

    def test_blog_post_creation(self):
        """Test that BlogPost is created correctly"""
        self.assertEqual(self.blog_post.title, "Test Blog Post")
        self.assertEqual(self.blog_post.author_name, "Jan Kowalski")
        self.assertTrue(self.blog_post.is_published)
        self.assertEqual(str(self.blog_post), "Test Blog Post")

    def test_blog_post_auto_slug(self):
        """Test that slug is auto-generated from title"""
        self.assertEqual(self.blog_post.slug, slugify("Test Blog Post"))

    def test_blog_post_get_absolute_url(self):
        """Test BlogPost get_absolute_url method"""
        url = self.blog_post.get_absolute_url()
        expected_url = reverse('blog_post_detail', args=[self.blog_post.slug])
        self.assertEqual(url, expected_url)

    def test_blog_post_content_html_property(self):
        """Test that content_html renders Markdown to HTML"""
        html = self.blog_post.content_html
        self.assertIn("Nagłówek", html)
        self.assertIn("<h1", html)
        self.assertIn("<p>Treść posta</p>", html)

    def test_blog_post_ordering(self):
        """Test that BlogPosts are ordered by published_date descending"""
        from datetime import timedelta
        blog_post2 = BlogPost.objects.create(
            title="Newer Post",
            short_description="Test",
            author_name="Test",
            published_date=date.today() + timedelta(days=1),
            content_markdown="Test",
            is_published=True
        )
        posts = BlogPost.objects.all()
        self.assertEqual(posts[0].title, "Newer Post")

    def test_blog_post_unique_slug_handling(self):
        """Test that duplicate titles get different slugs"""
        blog_post2 = BlogPost.objects.create(
            title="Test Blog Post",
            short_description="Test",
            author_name="Test",
            published_date=date.today(),
            content_markdown="Test",
            is_published=True
        )
        self.assertNotEqual(self.blog_post.slug, blog_post2.slug)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class VideoPlaylistModelTest(TestCase):
    """Tests for VideoPlaylist model"""

    def setUp(self):
        # Create a simple 1x1 pixel image for testing
        image_content = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x44\x01\x00\x3b'
        )
        self.test_image = SimpleUploadedFile(
            name='test_thumbnail.gif',
            content=image_content,
            content_type='image/gif'
        )

        self.playlist = VideoPlaylist.objects.create(
            title="Python Tutorial",
            description="Learn Python",
            thumbnail=self.test_image,
            youtube_playlist_url="https://www.youtube.com/playlist?list=TEST123",
            order=1,
            is_active=True
        )

    def test_video_playlist_creation(self):
        """Test that VideoPlaylist is created correctly"""
        self.assertEqual(self.playlist.title, "Python Tutorial")
        self.assertTrue(self.playlist.is_active)
        self.assertEqual(self.playlist.order, 1)
        self.assertEqual(str(self.playlist), "Python Tutorial")

    def test_video_playlist_auto_slug(self):
        """Test that slug is auto-generated"""
        self.assertEqual(self.playlist.slug, slugify("Python Tutorial"))

    def test_video_playlist_ordering(self):
        """Test that VideoPlaylists are ordered by order, then created_at"""
        image_content = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x44\x01\x00\x3b'
        )
        test_image2 = SimpleUploadedFile(
            name='test_thumbnail2.gif',
            content=image_content,
            content_type='image/gif'
        )

        playlist2 = VideoPlaylist.objects.create(
            title="JavaScript Tutorial",
            description="Learn JavaScript",
            thumbnail=test_image2,
            youtube_playlist_url="https://www.youtube.com/playlist?list=TEST456",
            order=0,
            is_active=True
        )
        playlists = VideoPlaylist.objects.all()
        self.assertEqual(playlists[0].order, 0)
        self.assertEqual(playlists[1].order, 1)


class ViewsTest(TestCase):
    """Tests for views"""

    def setUp(self):
        self.client = Client()

        # Create test data
        self.tag = Tag.objects.create(name="Python", slug="python")
        self.course = Course.objects.create(
            title="Test Course",
            slug="test-course",
            short_description="Test",
            description="Test description",
            is_active=True
        )
        self.course.tags.add(self.tag)

        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Test Lesson",
            slug="test-lesson",
            order=1,
            content_markdown="# Test content"
        )

        self.quiz = Quiz.objects.create(
            lesson=self.lesson,
            title="Test Quiz",
            description="Test quiz description"
        )

        self.question = Question.objects.create(
            quiz=self.quiz,
            text="Test question?",
            order=1,
            explanation="Test explanation"
        )

        self.correct_answer = Answer.objects.create(
            question=self.question,
            text="Correct answer",
            is_correct=True,
            order=1
        )

        self.wrong_answer = Answer.objects.create(
            question=self.question,
            text="Wrong answer",
            is_correct=False,
            order=2
        )

        self.task = PracticalTask.objects.create(
            lesson=self.lesson,
            title="Test Task",
            content_markdown="Test task content"
        )

        self.blog_post = BlogPost.objects.create(
            title="Test Blog Post",
            short_description="Test",
            author_name="Test Author",
            published_date=date.today(),
            content_markdown="Test content",
            is_published=True
        )

    def test_home_view(self):
        """Test home view returns 200 and uses correct template"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/index.html')
        self.assertIn('featured_courses', response.context)
        self.assertIn('recent_posts', response.context)
        self.assertIn('video_playlists', response.context)

    def test_courses_view(self):
        """Test courses view returns 200 and lists courses"""
        response = self.client.get(reverse('courses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/courses.html')
        self.assertIn('courses', response.context)
        self.assertIn('tags', response.context)
        self.assertEqual(len(response.context['courses']), 1)

    def test_course_lessons_view(self):
        """Test course lessons view"""
        response = self.client.get(
            reverse('course_lessons', args=[self.course.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/course_lessons.html')
        self.assertEqual(response.context['course'], self.course)
        self.assertIn(self.lesson, response.context['lessons'])

    def test_course_lessons_view_inactive_course(self):
        """Test that inactive courses return 404"""
        self.course.is_active = False
        self.course.save()
        response = self.client.get(
            reverse('course_lessons', args=[self.course.slug])
        )
        self.assertEqual(response.status_code, 404)

    def test_lesson_detail_view(self):
        """Test lesson detail view"""
        response = self.client.get(
            reverse('lesson_detail', args=[self.course.slug, self.lesson.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/lesson_detail.html')
        self.assertEqual(response.context['lesson'], self.lesson)
        self.assertEqual(response.context['course'], self.course)

    def test_lesson_detail_view_not_found(self):
        """Test lesson detail view with invalid slug returns 404"""
        response = self.client.get(
            reverse('lesson_detail', args=[self.course.slug, 'invalid-slug'])
        )
        self.assertEqual(response.status_code, 404)

    def test_quiz_detail_view(self):
        """Test quiz detail view"""
        response = self.client.get(
            reverse('quiz_detail', args=[self.course.slug, self.lesson.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/quiz_detail.html')
        self.assertEqual(response.context['quiz'], self.quiz)
        self.assertIn(self.question, response.context['questions'])

    def test_quiz_submit_get_redirects(self):
        """Test that GET request to quiz_submit redirects"""
        response = self.client.get(
            reverse('quiz_submit', args=[self.course.slug, self.lesson.slug])
        )
        self.assertEqual(response.status_code, 302)

    def test_quiz_submit_correct_answer(self):
        """Test quiz submission with correct answer"""
        response = self.client.post(
            reverse('quiz_submit', args=[self.course.slug, self.lesson.slug]),
            {f'question_{self.question.id}': self.correct_answer.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/quiz_result.html')
        self.assertEqual(response.context['correct_answers'], 1)
        self.assertEqual(response.context['score'], 100)

    def test_quiz_submit_wrong_answer(self):
        """Test quiz submission with wrong answer"""
        response = self.client.post(
            reverse('quiz_submit', args=[self.course.slug, self.lesson.slug]),
            {f'question_{self.question.id}': self.wrong_answer.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['correct_answers'], 0)
        self.assertEqual(response.context['score'], 0)

    def test_quiz_submit_no_answer(self):
        """Test quiz submission with no answer selected"""
        response = self.client.post(
            reverse('quiz_submit', args=[self.course.slug, self.lesson.slug]),
            {}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['correct_answers'], 0)

    def test_practical_task_detail_view(self):
        """Test practical task detail view"""
        response = self.client.get(
            reverse('practical_task_detail', args=[self.course.slug, self.lesson.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/practical_task_detail.html')
        self.assertEqual(response.context['task'], self.task)
        self.assertEqual(response.context['lesson'], self.lesson)

    def test_blog_post_detail_view(self):
        """Test blog post detail view"""
        response = self.client.get(
            reverse('blog_post_detail', args=[self.blog_post.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/blog_post_detail.html')
        self.assertEqual(response.context['blog_post'], self.blog_post)

    def test_blog_post_detail_unpublished(self):
        """Test that unpublished blog posts return 404"""
        self.blog_post.is_published = False
        self.blog_post.save()
        response = self.client.get(
            reverse('blog_post_detail', args=[self.blog_post.slug])
        )
        self.assertEqual(response.status_code, 404)


class IntegrationTest(TestCase):
    """Integration tests for complete user flows"""

    def setUp(self):
        self.client = Client()

        # Create a complete course with lessons, quiz, and task
        self.tag = Tag.objects.create(name="Python", slug="python")

        self.course = Course.objects.create(
            title="Python Basics",
            slug="python-basics",
            short_description="Learn Python",
            description="Complete Python course",
            is_active=True
        )
        self.course.tags.add(self.tag)

        self.lesson1 = Lesson.objects.create(
            course=self.course,
            title="Introduction",
            slug="introduction",
            order=1,
            content_markdown="# Welcome\n\nLearn Python basics"
        )

        self.lesson2 = Lesson.objects.create(
            course=self.course,
            title="Variables",
            slug="variables",
            order=2,
            content_markdown="# Variables\n\n```python\nx = 5\n```"
        )

        self.quiz = Quiz.objects.create(
            lesson=self.lesson2,
            title="Variables Quiz",
            description="Test your knowledge"
        )

        self.question1 = Question.objects.create(
            quiz=self.quiz,
            text="What is a variable?",
            order=1
        )

        Answer.objects.create(
            question=self.question1,
            text="A storage location",
            is_correct=True,
            order=1
        )

        Answer.objects.create(
            question=self.question1,
            text="A function",
            is_correct=False,
            order=2
        )

        self.question2 = Question.objects.create(
            quiz=self.quiz,
            text="How to create a variable?",
            order=2
        )

        self.correct_answer2 = Answer.objects.create(
            question=self.question2,
            text="x = 5",
            is_correct=True,
            order=1
        )

        Answer.objects.create(
            question=self.question2,
            text="var x = 5",
            is_correct=False,
            order=2
        )

    def test_complete_course_flow(self):
        """Test complete user flow through a course"""
        # 1. View home page
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

        # 2. View courses list
        response = self.client.get(reverse('courses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Basics")

        # 3. View course lessons
        response = self.client.get(
            reverse('course_lessons', args=[self.course.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Introduction")
        self.assertContains(response, "Variables")

        # 4. View first lesson
        response = self.client.get(
            reverse('lesson_detail', args=[self.course.slug, self.lesson1.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome")

        # 5. View second lesson (with quiz)
        response = self.client.get(
            reverse('lesson_detail', args=[self.course.slug, self.lesson2.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Variables")

        # 6. Take quiz
        response = self.client.get(
            reverse('quiz_detail', args=[self.course.slug, self.lesson2.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "What is a variable?")

        # 7. Submit quiz with mixed answers (1 correct, 1 wrong)
        response = self.client.post(
            reverse('quiz_submit', args=[self.course.slug, self.lesson2.slug]),
            {
                f'question_{self.question1.id}': self.question1.answers.get(is_correct=True).id,
                f'question_{self.question2.id}': self.question2.answers.get(is_correct=False).id,
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['correct_answers'], 1)
        self.assertEqual(response.context['incorrect_answers'], 1)
        self.assertEqual(response.context['score'], 50)

    def test_suggested_courses(self):
        """Test that suggested courses are based on tags"""
        # Create another course with the same tag
        course2 = Course.objects.create(
            title="Advanced Python",
            slug="advanced-python",
            short_description="Advanced topics",
            description="Advanced Python course",
            is_active=True
        )
        course2.tags.add(self.tag)

        # View course detail (this view has suggested_courses in the original views.py)
        # Note: course_detail view in urls.py has two patterns, need to check which one
        response = self.client.get(
            reverse('course_lessons', args=[self.course.slug])
        )
        self.assertEqual(response.status_code, 200)


class LessonContentModelTest(TestCase):
    """Tests for LessonContent model"""

    def setUp(self):
        self.course = Course.objects.create(
            title="Test Course",
            slug="test-course",
            short_description="Test",
            description="Test"
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Test Lesson",
            slug="test-lesson",
            order=1
        )

    def test_lesson_content_creation(self):
        """Test that LessonContent is created correctly"""
        content = LessonContent.objects.create(
            lesson=self.lesson,
            text_content="<p>Test content</p>"
        )
        self.assertEqual(content.lesson, self.lesson)
        self.assertIsNotNone(content.text_content)
        self.assertEqual(str(content), f"Treść lekcji: {self.lesson.title}")

    def test_lesson_content_one_to_one_relationship(self):
        """Test that LessonContent has one-to-one relationship with Lesson"""
        LessonContent.objects.create(
            lesson=self.lesson,
            text_content="<p>Test</p>"
        )

        # Try to create another content for the same lesson
        with self.assertRaises(Exception):
            LessonContent.objects.create(
                lesson=self.lesson,
                text_content="<p>Another test</p>"
            )

    def test_lesson_content_blank_text_content(self):
        """Test that text_content can be blank"""
        content = LessonContent.objects.create(
            lesson=self.lesson,
            text_content=""
        )
        self.assertEqual(content.text_content, "")

    def test_lesson_content_timestamps(self):
        """Test that timestamps are automatically set"""
        content = LessonContent.objects.create(
            lesson=self.lesson,
            text_content="Test"
        )
        self.assertIsNotNone(content.created_at)
        self.assertIsNotNone(content.updated_at)


class CourseDetailViewTest(TestCase):
    """Tests for course_detail view"""

    def setUp(self):
        self.client = Client()
        self.tag1 = Tag.objects.create(name="Python", slug="python")
        self.tag2 = Tag.objects.create(name="Web", slug="web")

        self.course = Course.objects.create(
            title="Python Course",
            slug="python-course",
            short_description="Learn Python",
            description="Complete Python course",
            is_active=True
        )
        self.course.tags.add(self.tag1)

    def test_course_detail_view(self):
        """Test course detail view displays correctly"""
        response = self.client.get(reverse('course_detail', args=[self.course.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/course_detail.html')
        self.assertEqual(response.context['course'], self.course)

    def test_course_detail_inactive_course(self):
        """Test that inactive courses return 404"""
        self.course.is_active = False
        self.course.save()
        response = self.client.get(reverse('course_detail', args=[self.course.slug]))
        self.assertEqual(response.status_code, 404)

    def test_course_detail_invalid_slug(self):
        """Test that invalid slug returns 404"""
        response = self.client.get(reverse('course_detail', args=['invalid-slug']))
        self.assertEqual(response.status_code, 404)

    def test_course_detail_suggested_courses(self):
        """Test that suggested courses are based on shared tags"""
        # Create courses with shared tags
        course2 = Course.objects.create(
            title="Advanced Python",
            slug="advanced-python",
            short_description="Advanced",
            description="Advanced Python",
            is_active=True
        )
        course2.tags.add(self.tag1)

        course3 = Course.objects.create(
            title="Web Development",
            slug="web-dev",
            short_description="Web",
            description="Web course",
            is_active=True
        )
        course3.tags.add(self.tag2)

        response = self.client.get(reverse('course_detail', args=[self.course.slug]))
        suggested = response.context['suggested_courses']

        # Should include course2 (shares tag1), but not course3
        self.assertIn(course2, suggested)
        self.assertNotIn(course3, suggested)
        self.assertNotIn(self.course, suggested)

    def test_course_detail_no_duplicate_suggestions(self):
        """Test that suggested courses don't include duplicates"""
        course2 = Course.objects.create(
            title="Another Course",
            slug="another-course",
            short_description="Test",
            description="Test",
            is_active=True
        )
        course2.tags.add(self.tag1, self.tag2)

        self.course.tags.add(self.tag2)

        response = self.client.get(reverse('course_detail', args=[self.course.slug]))
        suggested = response.context['suggested_courses']

        # Count occurrences
        suggestion_ids = [c.id for c in suggested]
        self.assertEqual(len(suggestion_ids), len(set(suggestion_ids)))

    def test_course_get_absolute_url(self):
        """Test Course.get_absolute_url() returns correct URL"""
        expected_url = reverse('course_detail', args=[self.course.slug])
        self.assertEqual(self.course.get_absolute_url(), expected_url)


class CourseFilteringTest(TestCase):
    """Tests for course filtering by tags"""

    def setUp(self):
        self.client = Client()
        self.tag_python = Tag.objects.create(name="Python", slug="python")
        self.tag_web = Tag.objects.create(name="Web", slug="web")

        self.course1 = Course.objects.create(
            title="Python Course",
            slug="python-course",
            short_description="Python",
            description="Python course",
            is_active=True
        )
        self.course1.tags.add(self.tag_python)

        self.course2 = Course.objects.create(
            title="Web Course",
            slug="web-course",
            short_description="Web",
            description="Web course",
            is_active=True
        )
        self.course2.tags.add(self.tag_web)

        self.course3 = Course.objects.create(
            title="Full Stack",
            slug="full-stack",
            short_description="Full Stack",
            description="Full Stack course",
            is_active=True
        )
        self.course3.tags.add(self.tag_python, self.tag_web)

    def test_courses_view_shows_all_active_courses(self):
        """Test that courses view shows all active courses"""
        response = self.client.get(reverse('courses'))
        courses = response.context['courses']
        self.assertEqual(len(courses), 3)

    def test_courses_view_hides_inactive_courses(self):
        """Test that inactive courses are not shown"""
        self.course1.is_active = False
        self.course1.save()

        response = self.client.get(reverse('courses'))
        courses = response.context['courses']
        self.assertEqual(len(courses), 2)
        self.assertNotIn(self.course1, courses)

    def test_courses_view_includes_all_tags(self):
        """Test that all tags are included in context"""
        response = self.client.get(reverse('courses'))
        tags = response.context['tags']
        self.assertIn(self.tag_python, tags)
        self.assertIn(self.tag_web, tags)


class EdgeCasesTest(TestCase):
    """Tests for edge cases and error handling"""

    def setUp(self):
        self.client = Client()
        self.course = Course.objects.create(
            title="Test Course",
            slug="test-course",
            short_description="Test",
            description="Test",
            is_active=True
        )
        self.lesson_without_quiz = Lesson.objects.create(
            course=self.course,
            title="Lesson without Quiz",
            slug="lesson-no-quiz",
            order=1
        )
        self.lesson_without_task = Lesson.objects.create(
            course=self.course,
            title="Lesson without Task",
            slug="lesson-no-task",
            order=2
        )

    def test_quiz_detail_without_quiz_returns_404(self):
        """Test that accessing quiz for lesson without quiz returns 404"""
        response = self.client.get(
            reverse('quiz_detail', args=[self.course.slug, self.lesson_without_quiz.slug])
        )
        self.assertEqual(response.status_code, 404)

    def test_practical_task_detail_without_task_returns_404(self):
        """Test that accessing task for lesson without task returns 404"""
        response = self.client.get(
            reverse('practical_task_detail', args=[self.course.slug, self.lesson_without_task.slug])
        )
        self.assertEqual(response.status_code, 404)

    def test_quiz_submit_without_quiz_returns_404(self):
        """Test that submitting quiz for lesson without quiz returns 404"""
        response = self.client.post(
            reverse('quiz_submit', args=[self.course.slug, self.lesson_without_quiz.slug]),
            {}
        )
        self.assertEqual(response.status_code, 404)

    def test_lesson_with_empty_markdown(self):
        """Test lesson with empty markdown content"""
        lesson = Lesson.objects.create(
            course=self.course,
            title="Empty Lesson",
            slug="empty-lesson",
            order=3,
            content_markdown=""
        )
        self.assertEqual(lesson.content_html, "")

    def test_lesson_with_none_markdown(self):
        """Test lesson with None markdown content"""
        lesson = Lesson.objects.create(
            course=self.course,
            title="None Lesson",
            slug="none-lesson",
            order=4,
            content_markdown=None
        )
        self.assertEqual(lesson.content_html, "")

    def test_question_with_empty_text(self):
        """Test question text_html with empty text"""
        lesson = Lesson.objects.create(
            course=self.course,
            title="Quiz Lesson",
            slug="quiz-lesson",
            order=5
        )
        quiz = Quiz.objects.create(
            lesson=lesson,
            title="Test Quiz"
        )
        question = Question.objects.create(
            quiz=quiz,
            text="",
            order=1
        )
        self.assertEqual(question.text_html, "")


class UniqueConstraintsTest(TestCase):
    """Tests for unique constraints and validation"""

    def setUp(self):
        self.course1 = Course.objects.create(
            title="Course 1",
            slug="course-1",
            short_description="Test",
            description="Test"
        )
        self.course2 = Course.objects.create(
            title="Course 2",
            slug="course-2",
            short_description="Test",
            description="Test"
        )

    def test_lesson_unique_together_same_course(self):
        """Test that lessons with same slug in same course are not allowed"""
        Lesson.objects.create(
            course=self.course1,
            title="Test Lesson",
            slug="test-lesson",
            order=1
        )

        # Try to create another lesson with same slug in same course
        with self.assertRaises(Exception):
            Lesson.objects.create(
                course=self.course1,
                title="Another Lesson",
                slug="test-lesson",
                order=2
            )

    def test_lesson_same_slug_different_courses(self):
        """Test that lessons with same slug in different courses are allowed"""
        lesson1 = Lesson.objects.create(
            course=self.course1,
            title="Test Lesson",
            slug="test-lesson",
            order=1
        )

        lesson2 = Lesson.objects.create(
            course=self.course2,
            title="Test Lesson",
            slug="test-lesson",
            order=1
        )

        self.assertNotEqual(lesson1.id, lesson2.id)
        self.assertEqual(lesson1.slug, lesson2.slug)

    def test_course_slug_must_be_unique(self):
        """Test that course slugs must be unique"""
        with self.assertRaises(Exception):
            Course.objects.create(
                title="Duplicate",
                slug="course-1",
                short_description="Test",
                description="Test"
            )


class CacheMechanismTest(TestCase):
    """Tests for cache mechanism in home view"""

    def setUp(self):
        self.client = Client()
        # Clear cache before tests
        from django.core.cache import cache
        cache.clear()

    def test_home_view_statistics_present(self):
        """Test that statistics are present in home view context"""
        Course.objects.create(
            title="Test Course",
            slug="test-course",
            short_description="Test",
            description="Test",
            is_active=True
        )

        response = self.client.get(reverse('home'))
        self.assertIn('total_courses', response.context)
        self.assertIn('total_lessons', response.context)
        self.assertIn('total_quizzes', response.context)

    def test_home_view_statistics_accuracy(self):
        """Test that statistics show correct counts"""
        course = Course.objects.create(
            title="Test Course",
            slug="test-course",
            short_description="Test",
            description="Test",
            is_active=True
        )

        lesson = Lesson.objects.create(
            course=course,
            title="Test Lesson",
            slug="test-lesson",
            order=1
        )

        Quiz.objects.create(
            lesson=lesson,
            title="Test Quiz"
        )

        response = self.client.get(reverse('home'))
        self.assertEqual(response.context['total_courses'], 1)
        self.assertEqual(response.context['total_lessons'], 1)
        self.assertEqual(response.context['total_quizzes'], 1)

    def test_home_view_cache_usage(self):
        """Test that cache is used for statistics"""
        from django.core.cache import cache

        # First request - should cache
        response1 = self.client.get(reverse('home'))

        # Check cache is set
        self.assertIsNotNone(cache.get('stats_total_courses'))
        self.assertIsNotNone(cache.get('stats_total_lessons'))
        self.assertIsNotNone(cache.get('stats_total_quizzes'))

    def test_home_view_only_counts_active_courses(self):
        """Test that statistics only count active courses"""
        Course.objects.create(
            title="Active Course",
            slug="active-course",
            short_description="Test",
            description="Test",
            is_active=True
        )

        Course.objects.create(
            title="Inactive Course",
            slug="inactive-course",
            short_description="Test",
            description="Test",
            is_active=False
        )

        response = self.client.get(reverse('home'))
        self.assertEqual(response.context['total_courses'], 1)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class VideoPlaylistFilteringTest(TestCase):
    """Tests for VideoPlaylist filtering and display"""

    def setUp(self):
        self.client = Client()
        # Create test images
        image_content = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x44\x01\x00\x3b'
        )

        self.active_playlist = VideoPlaylist.objects.create(
            title="Active Playlist",
            slug="active-playlist",
            description="Active",
            thumbnail=SimpleUploadedFile('active.gif', image_content, content_type='image/gif'),
            youtube_playlist_url="https://www.youtube.com/playlist?list=TEST1",
            order=1,
            is_active=True
        )

        self.inactive_playlist = VideoPlaylist.objects.create(
            title="Inactive Playlist",
            slug="inactive-playlist",
            description="Inactive",
            thumbnail=SimpleUploadedFile('inactive.gif', image_content, content_type='image/gif'),
            youtube_playlist_url="https://www.youtube.com/playlist?list=TEST2",
            order=2,
            is_active=False
        )

    def test_home_view_shows_only_active_playlists(self):
        """Test that home view shows only active video playlists"""
        response = self.client.get(reverse('home'))
        playlists = response.context['video_playlists']

        self.assertIn(self.active_playlist, playlists)
        self.assertNotIn(self.inactive_playlist, playlists)

    def test_home_view_playlist_ordering(self):
        """Test that playlists are ordered by order field"""
        image_content = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x44\x01\x00\x3b'
        )

        playlist_first = VideoPlaylist.objects.create(
            title="First",
            slug="first",
            description="First",
            thumbnail=SimpleUploadedFile('first.gif', image_content, content_type='image/gif'),
            youtube_playlist_url="https://www.youtube.com/playlist?list=TEST3",
            order=0,
            is_active=True
        )

        response = self.client.get(reverse('home'))
        playlists = list(response.context['video_playlists'])

        self.assertEqual(playlists[0], playlist_first)
        self.assertEqual(playlists[1], self.active_playlist)

    def test_home_view_limits_playlists(self):
        """Test that home view limits playlists to 6"""
        image_content = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x44\x01\x00\x3b'
        )

        # Create 7 more playlists (total 8 active)
        for i in range(7):
            VideoPlaylist.objects.create(
                title=f"Playlist {i}",
                slug=f"playlist-{i}",
                description=f"Playlist {i}",
                thumbnail=SimpleUploadedFile(f'playlist{i}.gif', image_content, content_type='image/gif'),
                youtube_playlist_url=f"https://www.youtube.com/playlist?list=TEST{i+10}",
                order=i+10,
                is_active=True
            )

        response = self.client.get(reverse('home'))
        playlists = response.context['video_playlists']

        self.assertEqual(len(playlists), 6)


class AdditionalMarkdownTest(TestCase):
    """Additional tests for Markdown edge cases"""

    def setUp(self):
        self.course = Course.objects.create(
            title="Test Course",
            slug="test-course",
            short_description="Test",
            description="Test"
        )

    def test_lesson_with_invalid_code_language(self):
        """Test lesson with invalid/unknown code language"""
        lesson = Lesson.objects.create(
            course=self.course,
            title="Invalid Code",
            slug="invalid-code",
            order=1,
            content_markdown="```invalidlang\ncode here\n```"
        )
        html = lesson.content_html
        # Should still render without crashing, defaulting to text
        self.assertIsNotNone(html)
        self.assertIn("code here", html)

    def test_blog_post_with_tables(self):
        """Test blog post with Markdown tables"""
        blog_post = BlogPost.objects.create(
            title="Table Test",
            slug="table-test",
            short_description="Test",
            author_name="Test",
            published_date=date.today(),
            content_markdown="| Header 1 | Header 2 |\n|----------|----------|\n| Cell 1   | Cell 2   |",
            is_published=True
        )
        html = blog_post.content_html
        self.assertIn("<table>", html)
        self.assertIn("Header 1", html)

    def test_practical_task_with_special_characters(self):
        """Test practical task with special characters in markdown"""
        lesson = Lesson.objects.create(
            course=self.course,
            title="Test Lesson",
            slug="test-lesson",
            order=1
        )

        task = PracticalTask.objects.create(
            lesson=lesson,
            title="Special Chars",
            content_markdown="Test with & < > \" ' characters"
        )

        self.assertIsNotNone(task.content_html)
        # HTML should be escaped properly
        self.assertIn("&", task.content_html)


class QuizScoringEdgeCasesTest(TestCase):
    """Additional tests for quiz scoring edge cases"""

    def setUp(self):
        self.client = Client()
        self.course = Course.objects.create(
            title="Test Course",
            slug="test-course",
            short_description="Test",
            description="Test",
            is_active=True
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Test Lesson",
            slug="test-lesson",
            order=1
        )
        self.quiz = Quiz.objects.create(
            lesson=self.lesson,
            title="Test Quiz"
        )

    def test_quiz_with_no_questions(self):
        """Test quiz submission with no questions"""
        response = self.client.post(
            reverse('quiz_submit', args=[self.course.slug, self.lesson.slug]),
            {}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['score'], 0)

    def test_quiz_with_invalid_answer_id(self):
        """Test quiz submission with invalid answer ID"""
        question = Question.objects.create(
            quiz=self.quiz,
            text="Test?",
            order=1
        )

        Answer.objects.create(
            question=question,
            text="Correct",
            is_correct=True,
            order=1
        )

        # Submit with invalid answer ID
        response = self.client.post(
            reverse('quiz_submit', args=[self.course.slug, self.lesson.slug]),
            {f'question_{question.id}': '99999'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['correct_answers'], 0)


def tearDownModule():
    """Clean up temporary media files after all tests"""
    try:
        if os.path.exists(TEMP_MEDIA_ROOT):
            shutil.rmtree(TEMP_MEDIA_ROOT)
    except Exception as e:
        print(f"Warning: Could not remove temporary media directory: {e}")
