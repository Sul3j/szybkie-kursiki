#!/usr/bin/env python3
"""
Test script for course import API

Usage:
    python test_import_api.py --file example-course.json --token YOUR_TOKEN
    python test_import_api.py --url https://szybkie-kursiki.pl --token YOUR_TOKEN
"""

import argparse
import json
import os
import sys
from pathlib import Path
import requests


def load_course_data(file_path):
    """Load course data from JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File not found: {file_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in file: {e}")
        sys.exit(1)


def import_course(api_url, token, course_data):
    """Send course data to import API"""
    headers = {
        'X-Import-Token': token,
        'Content-Type': 'application/json'
    }

    endpoint = f"{api_url}/api/import-course/"

    print(f"📤 Sending request to: {endpoint}")
    print(f"📦 Course title: {course_data.get('course', {}).get('title', 'N/A')}")
    print(f"📚 Lessons count: {len(course_data.get('lessons', []))}")
    print()

    try:
        response = requests.post(
            endpoint,
            headers=headers,
            json=course_data,
            timeout=30
        )

        print(f"📡 Response status: {response.status_code}")
        print()

        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(f"   Course ID: {result.get('course_id')}")
            print(f"   Course Slug: {result.get('course_slug')}")
            print(f"   Course Title: {result.get('course_title')}")
            print(f"   Lessons Count: {result.get('lessons_count')}")
            print()
            print(f"🔗 Admin URL: {api_url}{result.get('admin_url', '')}")
            print(f"🔗 Preview URL: {api_url}/course/{result.get('course_slug', '')}/")
            return True
        else:
            print("❌ Error!")
            try:
                error = response.json()
                print(f"   Message: {error.get('error', 'Unknown error')}")
            except:
                print(f"   Response: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API")
        print(f"   Check if the server is running at: {api_url}")
        return False
    except requests.exceptions.Timeout:
        print("❌ Error: Request timeout")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Test course import API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Import from example file
  python test_import_api.py --file ../examples/example-course.json --token YOUR_TOKEN

  # Use custom API URL
  python test_import_api.py --url https://szybkie-kursiki.pl --token YOUR_TOKEN --file course.json

  # Use environment variable for token
  export COURSE_IMPORT_TOKEN=your_token
  python test_import_api.py --file course.json
        """
    )

    parser.add_argument(
        '--file',
        default='../examples/example-course.json',
        help='Path to course JSON file (default: ../examples/example-course.json)'
    )
    parser.add_argument(
        '--url',
        default='http://localhost:8000',
        help='API base URL (default: http://localhost:8000)'
    )
    parser.add_argument(
        '--token',
        default=os.getenv('COURSE_IMPORT_TOKEN'),
        help='Import token (or set COURSE_IMPORT_TOKEN env var)'
    )

    args = parser.parse_args()

    # Validate token
    if not args.token:
        print("❌ Error: Import token is required")
        print("   Use --token or set COURSE_IMPORT_TOKEN environment variable")
        sys.exit(1)

    # Load course data
    print(f"📂 Loading course data from: {args.file}")
    course_data = load_course_data(args.file)
    print("✅ Course data loaded successfully")
    print()

    # Import course
    success = import_course(args.url, args.token, course_data)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
