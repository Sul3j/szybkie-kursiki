# Quick Start - Generowanie kursów z n8n i Claude Code

Szybki przewodnik uruchomienia systemu automatycznego generowania kursów.

## 🚀 Szybki start (5 minut)

### 1. Przygotuj tokeny

```bash
# Wygeneruj bezpieczny token
python3 -c "import secrets; print('COURSE_IMPORT_TOKEN=' + secrets.token_urlsafe(32))"

# Dodaj do .env w projekcie Django
echo "COURSE_IMPORT_TOKEN=<wygenerowany-token>" >> .env
```

### 2. Zrestartuj Django

```bash
cd /home/deploy/szybkie-kursiki
docker-compose restart web
```

### 3. Uruchom n8n

```bash
# Docker (zalecane)
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -e DJANGO_APP_URL=https://szybkie-kursiki.pl \
  -e COURSE_IMPORT_TOKEN=<twoj-token> \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### 4. Skonfiguruj n8n

1. Otwórz: `http://localhost:5678`
2. Utwórz konto
3. Dodaj Anthropic credentials:
   - Settings → Credentials → Add Credential
   - Wybierz "Anthropic API"
   - Wklej API Key

### 5. Importuj workflow

1. W n8n: **Workflows** → **Add workflow** → **Import from File**
2. Wybierz: `n8n-workflows/course-generator-workflow.json`
3. Aktywuj workflow (przełącznik ON)

### 6. Wygeneruj pierwszy kurs!

1. Otwórz workflow w n8n
2. Kliknij **"Execute Workflow"**
3. W polu `coursePrompt` wpisz:

```
Stwórz kurs "Git i GitHub dla początkujących" z 4 lekcjami:
1. Wprowadzenie do kontroli wersji
2. Podstawowe komendy Git
3. Praca z GitHub
4. Branching i merge

Każda lekcja z quizem i zadaniem praktycznym.
```

4. Kliknij **"Execute"**
5. Poczekaj 2-5 minut
6. Sprawdź wynik!

## ✅ Weryfikacja

### Sprawdź czy działa:

```bash
# Test API endpoint
curl -X POST https://szybkie-kursiki.pl/api/import-course/ \
  -H "X-Import-Token: <twoj-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "course": {
      "title": "Test",
      "short_description": "Test kurs",
      "description": "Testowy opis",
      "icon": "fas fa-code",
      "tags": ["Test"]
    },
    "lessons": [{
      "title": "Test lesson",
      "order": 0,
      "content_markdown": "# Test\n\nTreść testowa"
    }]
  }'
```

Oczekiwana odpowiedź:
```json
{
  "status": "ok",
  "course_id": 123,
  "course_slug": "test",
  ...
}
```

## 🎯 Co dalej?

1. **Opublikuj kurs**:
   - Django Admin → Kursy → Znajdź nowy kurs
   - Zaznacz `is_active = True`
   - Zapisz

2. **Zobacz kurs na stronie**:
   - `https://szybkie-kursiki.pl/course/<slug-kursu>/`

3. **Wygeneruj więcej kursów**:
   - Użyj różnych promptów
   - Eksperymentuj z tematami

## 📝 Przykładowe prompty

### Kurs Python:
```
Stwórz kompletny kurs Python dla początkujących zawierający:
- Instalacja i konfiguracja
- Podstawy składni
- Typy danych
- Funkcje
- Klasy i obiekty

Z szczegółowymi lekcjami, quizami i zadaniami.
```

### Kurs JavaScript:
```
Kurs JavaScript Modern - ES6+ dla programistów znających podstawy:
1. Arrow functions i destructuring
2. Promises i async/await
3. Modules
4. Classes
5. Array methods

Każda lekcja z praktycznymi przykładami.
```

### Kurs Docker:
```
Docker dla developerów - od podstaw do zaawansowanych:
- Czym jest konteneryzacja
- Tworzenie obrazów Docker
- Docker Compose
- Volumes i networking
- CI/CD z Docker

Z quizami sprawdzającymi wiedzę.
```

## 🔧 Troubleshooting

### Workflow nie działa:
1. Sprawdź czy Anthropic credentials są poprawne
2. Sprawdź zmienne środowiskowe n8n
3. Zobacz logi: `docker logs n8n`

### Kurs nie importuje się:
1. Sprawdź token w Django i n8n
2. Zobacz logi Django: `docker-compose logs web`
3. Zweryfikuj format JSON w workflow

### Timeout:
1. Zmniejsz liczbę lekcji w prompcie
2. Poczekaj dłużej (Claude może potrzebować czasu)

## 💡 Tips & Tricks

1. **Lepsze prompty = lepsze kursy**
   - Bądź konkretny
   - Określ poziom zaawansowania
   - Podaj strukturę lekcji

2. **Iteruj i poprawiaj**
   - Generuj kurs jako draft
   - Edytuj w Django Admin
   - Publikuj po weryfikacji

3. **Używaj tagów**
   - Ułatwia kategoryzację
   - Pomaga w wyszukiwaniu
   - Lepsze SEO

4. **Testuj lokalnie**
   - Najpierw przetestuj na localhost
   - Zweryfikuj treść
   - Potem wdróż na produkcję

## 🎉 Gotowe!

Masz działający system automatycznego generowania kursów!

Więcej informacji w głównym README.md
