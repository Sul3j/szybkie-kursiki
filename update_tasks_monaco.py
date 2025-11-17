"""
Simple script to update all PracticalTask objects to use Monaco Editor.
Run with: docker-compose exec web python update_tasks_monaco.py
Or without Docker: python update_tasks_monaco.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from main_app.models import PracticalTask

def main():
    tasks = PracticalTask.objects.all()
    count = tasks.count()

    print(f"Znaleziono {count} zadań praktycznych do aktualizacji...")

    for i, task in enumerate(tasks, 1):
        print(f"Aktualizacja {i}/{count}: {task.title}")
        task.save()  # Re-save to apply Monaco formatting

    print(f"\n✓ Zaktualizowano {count} zadań!")

if __name__ == '__main__':
    main()
