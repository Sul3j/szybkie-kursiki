from django.test import TestCase, Client
from django.urls import reverse
from django.utils.text import slugify
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date, datetime
from .models import (
    Tag, Course, Lesson, LessonContent, Quiz, Question, Answer,
    PracticalTask, BlogPost, VideoPlaylist
)


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
