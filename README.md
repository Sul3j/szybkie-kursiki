# Szybkie Kursiki

An educational platform for learning programming with interactive courses, quizzes, and practical tasks.

## Project Description

Szybkie Kursiki is a comprehensive e-learning platform built with Django, enabling the creation and sharing of programming courses with rich support for technical content. The project offers an intuitive learning interface with support for code, quizzes, and practical exercises.

## Features

### Courses and Lessons
- Create courses with multiple lessons
- Lesson content in Markdown format with code syntax highlighting (Pygments)
- Automatic rendering of code blocks in various programming languages
- Tag system for course categorization
- Lesson ordering by sequence
- Suggested courses based on tags

### Quiz System
- Quizzes linked to lessons
- Questions with Markdown and code block support
- Multiple answers per question
- Automatic answer validation
- Question explanations
- Quiz results with summary

### Practical Tasks
- Practical tasks linked to lessons
- Detailed instructions in Markdown format
- Solution examples
- Hint system
- Complete solutions

### Blog
- Blog post system
- Content in Markdown format
- Code syntax highlighting in articles
- Publication date and author

### Video Courses
- YouTube playlist integration
- Video course thumbnails
- Display order management

### Admin Panel
- Elegant Django Jazzmin interface
- WYSIWYG editor (CKEditor) for content
- Management of all platform elements

## Technologies

### Backend
- **Django 5.1.5** - web application framework
- **MySQL 8.0** - database
- **Python 3.x** - programming language

### Python Libraries
- **mysqlclient** - MySQL connector for Django
- **django-jazzmin** - modern admin panel interface
- **django-ckeditor** - WYSIWYG editor
- **markdown** - Markdown syntax processing
- **Pygments** - code syntax highlighting
- **Pillow** - image handling
- **python-dotenv** - environment variable management

### Deployment
- **Docker** - application containerization
- **Docker Compose** - container orchestration

## Project Structure

```
szybkie-kursiki/
├── app/                      # Django main project configuration
│   ├── settings.py          # Project settings
│   ├── urls.py              # Main URL routing
│   └── wsgi.py              # WSGI application
├── main_app/                # Main application
│   ├── models.py            # Data models (Course, Lesson, Quiz, etc.)
│   ├── views.py             # Application views
│   ├── urls.py              # Application URL routing
│   ├── forms.py             # Forms
│   ├── admin.py             # Admin panel configuration
│   ├── static/              # Static files
│   │   └── main_app/
│   │       ├── css/         # Styling (courses, lessons, quiz, etc.)
│   │       └── js/          # JavaScript logic (quiz, lessons, etc.)
│   └── templates/           # HTML templates
│       └── main_app/
│           ├── base.html
│           ├── index.html
│           ├── courses.html
│           ├── lesson_detail.html
│           ├── quiz_detail.html
│           └── ...
├── media/                   # User-uploaded files
├── static/                  # Global static files
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile               # Docker image definition
├── requirements.txt         # Python dependencies
└── manage.py               # Django management tool
```

## Data Models

### Course
- Title, slug, description
- Icon (Font Awesome)
- Tags (many-to-many relationship)
- Active status

### Lesson
- Linked to course
- Content in Markdown
- Display order
- Automatic HTML rendering with syntax highlighting

### Quiz
- Linked to lesson (one-to-one)
- Title and description

### Question
- Linked to quiz
- Content with Markdown support
- Answer explanation
- Order

### Answer
- Linked to question
- Correctness flag (is_correct)

### PracticalTask
- Linked to lesson (one-to-one)
- Content, instructions, examples, hints, solution
- All fields with Markdown support

### BlogPost
- Title, slug, author
- Content in Markdown
- Publication date

### VideoPlaylist
- YouTube playlist link
- Thumbnail
- Display order

## Installation

### Requirements
- Docker and Docker Compose
- `.env` file with configuration (see Configuration section)

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/szybkie-kursiki.git
cd szybkie-kursiki
```

2. Create a `.env` file in the project root directory:
```env
# Django
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# MySQL
MYSQL_DATABASE=szybkie_kursiki
MYSQL_USER=django_user
MYSQL_PASSWORD=your-password
MYSQL_ROOT_PASSWORD=your-root-password
MYSQL_HOST=db
MYSQL_PORT=3306
```

3. Start Docker containers:
```bash
docker-compose up -d
```

4. Run database migrations:
```bash
docker-compose exec web python manage.py migrate
```

5. Create a superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

6. Open your browser and navigate to:
- Application: http://localhost:8000
- Admin panel: http://localhost:8000/admin

## Running Without Docker

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure MySQL database locally

3. Create a `.env` file with configuration

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Start the development server:
```bash
python manage.py runserver
```

## Usage

### Admin Panel
1. Log in to the admin panel: http://localhost:8000/admin
2. Add tags, courses, lessons
3. Create quizzes and practical tasks
4. Publish blog posts
5. Add video courses

### Creating Content in Markdown
Lessons, practical tasks, and blog posts support Markdown syntax:

```markdown
# Heading

## Code Block

```python
def hello():
    print("Hello World!")
```

### List
- Item 1
- Item 2
```

### Special Blocks (Callouts)
In lesson content, you can use special blocks:

```markdown
> [!NOTE]
> This is a note

> [!WARNING]
> This is a warning

> [!DANGER]
> This is danger
```

## Configuration

### Environment Variables
All environment variables should be defined in the `.env` file:

- `DJANGO_SECRET_KEY` - Django secret key
- `DJANGO_DEBUG` - debug mode (True/False)
- `DJANGO_ALLOWED_HOSTS` - allowed hosts (comma-separated)
- `MYSQL_*` - MySQL database configuration

### Font Awesome Icons
Courses can use Font Awesome icons. Examples:
- `fas fa-code` - code icon
- `fab fa-python` - Python icon
- `fab fa-js` - JavaScript icon

## Project Development

### Code Structure
- Views in `main_app/views.py`
- Models in `main_app/models.py`
- Routing in `main_app/urls.py`
- Templates in `main_app/templates/main_app/`
- Static files in `main_app/static/main_app/`

### Adding New Features
1. Add model in `models.py` (if needed)
2. Create migration: `python manage.py makemigrations`
3. Apply migration: `python manage.py migrate`
4. Add view in `views.py`
5. Add routing in `urls.py`
6. Create HTML template
7. Add CSS styles and JavaScript if needed

## Author

- Szymon Sulejczak

## Support

For questions or issues, create an issue in the GitHub repository.
