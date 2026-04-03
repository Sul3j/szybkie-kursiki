# Automatyzacja generowania kursów za pomocą n8n i Claude Code

Ten katalog zawiera konfigurację workflow n8n, która automatyzuje proces tworzenia kursów, lekcji i quizów za pomocą Claude Code (Anthropic API).

## Spis treści

- [Przegląd](#przegląd)
- [Wymagania](#wymagania)
- [Instalacja i konfiguracja](#instalacja-i-konfiguracja)
- [Dostępne workflow](#dostępne-workflow)
- [Jak używać](#jak-używać)
- [Format danych](#format-danych)
- [Rozwiązywanie problemów](#rozwiązywanie-problemów)

## Przegląd

System automatyzacji składa się z:

1. **Django API endpoint** (`/api/import-course/`) - przyjmuje strukturę kursu w formacie JSON
2. **n8n workflow** - wykorzystuje Claude Code do generowania treści kursu i wysyła do API
3. **Claude Code (Anthropic API)** - generuje pełną strukturę kursu z lekcjami, quizami i zadaniami

### Schemat działania

```
Prompt użytkownika
      ↓
n8n Trigger (Manual/Webhook)
      ↓
Claude Code API (generuje strukturę kursu)
      ↓
Parser JSON (walidacja)
      ↓
Django API (/api/import-course/)
      ↓
Kurs zapisany w bazie (jako draft)
      ↓
Admin może zweryfikować i opublikować
```

## Wymagania

### Oprogramowanie

- **n8n** (wersja >= 1.0.0) - zainstalowany i uruchomiony
- **Django aplikacja** - szybkie-kursiki.pl
- **Konto Anthropic** - z dostępem do Claude API

### Klucze API

1. **Anthropic API Key** - do generowania treści
2. **COURSE_IMPORT_TOKEN** - token bezpieczeństwa dla Django API

## Instalacja i konfiguracja

### Krok 1: Konfiguracja Django

1. Dodaj token importu do pliku `.env`:

```bash
COURSE_IMPORT_TOKEN='twoj-bezpieczny-losowy-token-tutaj'
```

2. Wygeneruj bezpieczny token (opcjonalnie):

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

3. Zrestartuj aplikację Django:

```bash
docker-compose restart web
```

### Krok 2: Instalacja n8n

Jeśli jeszcze nie masz n8n, zainstaluj go:

```bash
# Docker (zalecane)
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# Lub npm
npm install n8n -g
n8n
```

### Krok 3: Konfiguracja n8n

1. Otwórz n8n w przeglądarce: `http://localhost:5678`

2. Przejdź do **Settings > Credentials**

3. Dodaj nowe credentials:

#### Anthropic API Credentials

- Typ: `Anthropic API`
- API Key: `twój-klucz-anthropic-api`

#### Zmienne środowiskowe n8n

Dodaj do pliku `.env` n8n (lub ustaw jako zmienne środowiskowe):

```bash
# URL twojej aplikacji Django
DJANGO_APP_URL=https://szybkie-kursiki.pl

# Token do importu kursów (ten sam co w Django)
COURSE_IMPORT_TOKEN=twoj-bezpieczny-losowy-token-tutaj
```

### Krok 4: Import workflow do n8n

1. W n8n kliknij **"+"** > **Import from File**

2. Wybierz jeden z workflow:
   - `course-generator-workflow.json` - wersja z ręcznym triggerem
   - `course-generator-webhook-workflow.json` - wersja z webhookiem

3. Aktywuj workflow (przełącznik w prawym górnym rogu)

## Dostępne workflow

### 1. Course Generator (Manual Trigger)

**Plik**: `course-generator-workflow.json`

**Opis**: Workflow z ręcznym triggerem - uruchamiany manualnie z interfejsu n8n.

**Użycie**: Idealne do testowania i jednorazowego generowania kursów.

**Jak uruchomić**:
1. Otwórz workflow w n8n
2. Kliknij "Execute Workflow"
3. Podaj prompt w polu `coursePrompt`
4. Workflow automatycznie wygeneruje i zaimportuje kurs

### 2. Course Generator (Webhook)

**Plik**: `course-generator-webhook-workflow.json`

**Opis**: Workflow z webhookiem - może być wywoływany przez zewnętrzne systemy.

**Użycie**: Integracja z innymi systemami, automatyzacja, API.

**Endpoint**: `http://localhost:5678/webhook/generate-course`

**Przykład wywołania**:

```bash
curl -X POST http://localhost:5678/webhook/generate-course \
  -H "Content-Type: application/json" \
  -d '{
    "coursePrompt": "Stwórz kurs Python dla początkujących obejmujący podstawy programowania, zmienne, pętle i funkcje"
  }'
```

## Jak używać

### Przykładowe prompty

#### Kurs dla początkujących:

```
Stwórz kurs "Python od podstaw" dla początkujących programistów.
Kurs powinien zawierać 5 lekcji:
1. Wprowadzenie do Pythona i instalacja
2. Zmienne i typy danych
3. Instrukcje warunkowe
4. Pętle
5. Funkcje

Każda lekcja powinna mieć szczegółową treść z przykładami kodu,
quiz z 5 pytaniami i zadanie praktyczne.
```

#### Kurs zaawansowany:

```
Stwórz kurs "FastAPI - Tworzenie REST API" dla programistów Python
znających podstawy. Kurs powinien obejmować:
1. Wprowadzenie do FastAPI
2. Routing i request handling
3. Modele Pydantic
4. Bazy danych z SQLAlchemy
5. Autoryzacja i JWT

Treść powinna być szczegółowa z praktycznymi przykładami.
```

#### Kurs tematyczny:

```
Stwórz kurs o Docker dla developerów. Zawrzyj tematy:
- Podstawy konteneryzacji
- Dockerfile
- Docker Compose
- Volumes i networking
- Best practices

Z quizami i zadaniami praktycznymi.
```

### Krok po kroku - generowanie kursu

1. **Przygotuj prompt**
   - Określ temat kursu
   - Wskaż poziom zaawansowania (początkujący/średniozaawansowany/zaawansowany)
   - Wymień tematy lekcji
   - Podaj dodatkowe wymagania

2. **Uruchom workflow**
   - Manual: Execute Workflow w n8n
   - Webhook: Wyślij POST request

3. **Poczekaj na generowanie**
   - Claude Code generuje treść (2-5 minut)
   - System automatycznie formatuje i waliduje JSON
   - Kurs jest importowany do Django

4. **Sprawdź w panelu admin**
   - Przejdź do Django Admin
   - Znajdź nowo utworzony kurs (status: draft)
   - Zweryfikuj treść
   - Ustaw `is_active=True` aby opublikować

## Format danych

### Struktura JSON kursu

```json
{
  "course": {
    "title": "Nazwa kursu",
    "short_description": "Krótki opis (max 200 znaków)",
    "description": "Pełny opis kursu",
    "icon": "fas fa-code",
    "tags": ["Python", "Backend"]
  },
  "lessons": [
    {
      "title": "Tytuł lekcji",
      "order": 0,
      "content_markdown": "# Treść lekcji\n\n...",
      "quiz": {
        "title": "Quiz - Tytuł",
        "description": "Opis quizu",
        "questions": [
          {
            "text": "Pytanie?",
            "order": 0,
            "explanation": "Wyjaśnienie",
            "answers": [
              {
                "text": "Odpowiedź",
                "is_correct": true,
                "order": 0
              }
            ]
          }
        ]
      },
      "practical_task": {
        "title": "Zadanie",
        "content_markdown": "Treść zadania",
        "instructions_markdown": "Instrukcje",
        "example_markdown": "Przykład",
        "hints_markdown": "Wskazówki",
        "solution_markdown": "Rozwiązanie"
      }
    }
  ]
}
```

### Ikony Font Awesome

Dostępne ikony dla kursów (parametr `icon`):

- `fas fa-code` - Programowanie
- `fab fa-python` - Python
- `fab fa-js` - JavaScript
- `fab fa-react` - React
- `fab fa-docker` - Docker
- `fas fa-database` - Bazy danych
- `fas fa-server` - Backend
- `fas fa-laptop-code` - Fullstack
- `fas fa-mobile-alt` - Mobile
- `fas fa-robot` - AI/ML

Pełna lista: https://fontawesome.com/icons

## Odpowiedź API

### Sukces

```json
{
  "status": "success",
  "message": "Kurs został pomyślnie utworzony!",
  "course_title": "Python od podstaw",
  "course_slug": "python-od-podstaw",
  "lessons_count": 5,
  "admin_url": "https://szybkie-kursiki.pl/admin/main_app/course/123/change/",
  "preview_url": "https://szybkie-kursiki.pl/course/python-od-podstaw/"
}
```

### Błąd

```json
{
  "status": "error",
  "message": "Nie udało się zaimportować kursu",
  "error": "Missing course title"
}
```

## Rozwiązywanie problemów

### Błąd: "Unauthorized" (403)

**Przyczyna**: Nieprawidłowy lub brakujący `COURSE_IMPORT_TOKEN`

**Rozwiązanie**:
1. Sprawdź czy token w `.env` Django jest taki sam jak w n8n
2. Zrestartuj Django i n8n

### Błąd: "Failed to parse Claude response"

**Przyczyna**: Claude zwrócił nieprawidłowy JSON

**Rozwiązanie**:
1. Sprawdź prompt - upewnij się, że jest jasny i konkretny
2. Sprawdź logi Claude w n8n
3. Spróbuj z prostszym promptem

### Błąd: "Missing course title or lessons"

**Przyczyna**: Struktura JSON nie zawiera wymaganych pól

**Rozwiązanie**:
1. Zmodyfikuj system prompt w Claude node
2. Dodaj więcej szczegółów w prompcie użytkownika

### Kurs nie pojawia się na stronie

**Przyczyna**: Kurs został utworzony jako draft (`is_active=False`)

**Rozwiązanie**:
1. Przejdź do Django Admin
2. Znajdź kurs
3. Ustaw `is_active = True`
4. Zapisz

### Timeout podczas generowania

**Przyczyna**: Zbyt długi kurs lub wolne API

**Rozwiązanie**:
1. Zmniejsz liczbę lekcji w prompcie
2. Zwiększ timeout w n8n settings
3. Spróbuj ponownie

## Bezpieczeństwo

### Zalecenia

1. **COURSE_IMPORT_TOKEN**:
   - Użyj długiego, losowego tokena (min. 32 znaki)
   - Przechowuj w zmiennych środowiskowych
   - Nigdy nie commituj do repozytorium

2. **Anthropic API Key**:
   - Przechowuj w n8n credentials
   - Nie udostępniaj publicznie

3. **Webhook endpoint**:
   - Zabezpiecz tokenem lub basic auth
   - Użyj HTTPS w produkcji
   - Rate limiting

4. **Kurs draft**:
   - Wszystkie kursy są tworzone jako draft
   - Zawsze weryfikuj przed publikacją
   - Sprawdź treść pod kątem błędów

## Przykładowy flow produkcyjny

1. Marketing wysyła request do webhooka z tematem kursu
2. n8n generuje kurs za pomocą Claude
3. Kurs trafia do bazy jako draft
4. Notyfikacja email do zespołu edukacyjnego
5. Weryfikacja i edycja w Django Admin
6. Publikacja kursu

## Wsparcie

Jeśli masz problemy:

1. Sprawdź logi n8n
2. Sprawdź logi Django (`docker-compose logs web`)
3. Sprawdź dokumentację Anthropic API
4. Otwórz issue w repozytorium projektu

## Licencja

Ten projekt jest częścią szybkie-kursiki.pl
