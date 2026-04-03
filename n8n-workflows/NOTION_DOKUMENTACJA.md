# 🤖 Automatyczne generowanie kursów - Szybkie Kursiki

System automatycznego generowania kompletnych kursów (lekcje + quizy + zadania) za pomocą n8n i Claude AI.

---

## 📊 Jak to działa?

```
1. Wpisujesz prompt → "Stwórz kurs Python dla początkujących"
          ↓
2. n8n przekazuje do Claude AI
          ↓
3. Claude generuje pełną strukturę kursu (JSON)
          ↓
4. System waliduje i formatuje dane
          ↓
5. Wysyła do Django API (/api/import-course/)
          ↓
6. Kurs trafia do bazy jako DRAFT
          ↓
7. Weryfikujesz w Django Admin i publikujesz
```

---

## 🔧 Konfiguracja - WSZYSTKO CO MUSISZ ZROBIĆ

### ✅ Krok 1: Token do API (Django)

**GDZIE:** Plik `.env` w projekcie szybkie-kursiki

**CO DODAĆ:**
```bash
COURSE_IMPORT_TOKEN=wygenerowany-bezpieczny-token
```

**JAK WYGENEROWAĆ TOKEN:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**PRZYKŁAD:**
```bash
COURSE_IMPORT_TOKEN=xK7mP9nQ2rS5tU8vW1yZ4aB6cD9eF2gH3jK6lM9nP2qR5sT8uV1wX4yZ7aB0cD3
```

**PO DODANIU TOKENA:**
```bash
cd /home/deploy/szybkie-kursiki
docker-compose restart web
```

---

### ✅ Krok 2: Anthropic API Key (Claude)

**GDZIE:** n8n → Settings → Credentials

**JAK DODAĆ:**

1. Otwórz: https://n8n.szybkie-kursiki.pl/
2. Zaloguj się:
   - Username: `admin`
   - Password: `/SGMfTh3B44ZG4CR8eSYNMgoKdMSW5t5`
3. Kliknij **Settings** (⚙️) → **Credentials**
4. Kliknij **Add Credential**
5. Wyszukaj i wybierz: **Anthropic API**
6. Wklej swój **API Key** z https://console.anthropic.com/
7. Kliknij **Save**

**GDZIE DOSTAĆ API KEY:**
- Wejdź na: https://console.anthropic.com/
- Zaloguj się
- Settings → API Keys
- Create Key

---

### ✅ Krok 3: Zmienne środowiskowe w n8n

**OPCJA A - Przez Docker (zalecane):**

Edytuj docker-compose dla n8n i dodaj:
```yaml
environment:
  - DJANGO_APP_URL=https://szybkie-kursiki.pl
  - COURSE_IMPORT_TOKEN=<ten-sam-token-co-w-django>
```

Zrestartuj:
```bash
docker-compose restart n8n
```

**OPCJA B - Bezpośrednio w n8n:**

1. Otwórz: https://n8n.szybkie-kursiki.pl/
2. Settings → Variables
3. Dodaj dwie zmienne:

| Name | Value |
|------|-------|
| `DJANGO_APP_URL` | `https://szybkie-kursiki.pl` |
| `COURSE_IMPORT_TOKEN` | `<ten-sam-token-co-w-django>` |

---

### ✅ Krok 4: Skonfiguruj workflow

**WORKFLOW 1 - Manual Trigger (do ręcznego generowania):**

1. Otwórz: https://n8n.szybkie-kursiki.pl/workflow/e01e4a8f-1fc3-4d91-a870-19bb5ba18223
2. Kliknij na node **"Generate Course with Claude"**
3. W polu **Credential to connect with** wybierz dodane wcześniej Anthropic credentials
4. **Zapisz** workflow (Ctrl+S)
5. **Aktywuj** workflow (przełącznik ON w prawym górnym rogu)

**WORKFLOW 2 - Webhook (do integracji z API):**

1. Otwórz: https://n8n.szybkie-kursiki.pl/workflow/4ec0a807-a671-4f65-91b2-7da7db6fd66f
2. Kliknij na node **"Generate Course with Claude"**
3. W polu **Credential to connect with** wybierz Anthropic credentials
4. **Zapisz** workflow
5. **Aktywuj** workflow

---

## 🚀 Jak używać - Generowanie kursu

### Metoda 1: Ręczne generowanie (Manual Trigger)

1. **Otwórz workflow:** https://n8n.szybkie-kursiki.pl/workflow/e01e4a8f-1fc3-4d91-a870-19bb5ba18223

2. **Kliknij "Execute Workflow"** (przycisk po prawej stronie)

3. **Przejdź do node "Manual Trigger"** i kliknij "Execute"

4. **W oknie testowym wpisz JSON:**
```json
{
  "coursePrompt": "Stwórz kurs 'Python dla początkujących' z 5 lekcjami: instalacja, zmienne, pętle, funkcje, klasy. Każda lekcja z quizem i zadaniem."
}
```

5. **Workflow się uruchomi** - poczekaj 2-5 minut

6. **Sprawdź wynik** - zobaczysz status i linki do kursu

---

### Metoda 2: Przez Webhook (API)

**Endpoint:**
```
POST https://n8n.szybkie-kursiki.pl/webhook/generate-course
```

**Przykład cURL:**
```bash
curl -X POST https://n8n.szybkie-kursiki.pl/webhook/generate-course \
  -H "Content-Type: application/json" \
  -d '{
    "coursePrompt": "Stwórz kurs Git i GitHub dla programistów z 4 lekcjami"
  }'
```

**Odpowiedź (sukces):**
```json
{
  "status": "success",
  "course_title": "Git i GitHub dla programistów",
  "course_slug": "git-i-github-dla-programistow",
  "lessons_count": 4,
  "admin_url": "https://szybkie-kursiki.pl/admin/main_app/course/123/change/",
  "preview_url": "https://szybkie-kursiki.pl/course/git-i-github-dla-programistow/"
}
```

---

## 📝 Przykładowe prompty

### Kurs dla początkujących:
```
Stwórz kurs "Python od podstaw" dla początkujących programistów.
Kurs powinien zawierać 5 lekcji:
1. Wprowadzenie do Python - instalacja, pierwszy program
2. Zmienne i typy danych
3. Instrukcje warunkowe
4. Pętle
5. Funkcje

Każda lekcja z szczegółową treścią, przykładami kodu, quizem i zadaniem praktycznym.
```

### Kurs zaawansowany:
```
Stwórz kurs "Docker dla developerów" z praktycznymi przykładami:
- Podstawy konteneryzacji
- Dockerfile
- Docker Compose
- Volumes i networking
- CI/CD z Docker

Poziom: średniozaawansowany
```

### Kurs z konkretną technologią:
```
Kurs "FastAPI - REST API w Python" dla programistów Python:
1. Wprowadzenie do FastAPI
2. Routing i request handling
3. Modele Pydantic
4. Bazy danych (SQLAlchemy)
5. Autoryzacja JWT

Z prawdziwymi przykładami projektów.
```

**WIĘCEJ PRZYKŁADÓW:** `/home/deploy/szybkie-kursiki/n8n-workflows/examples/sample-prompts.md`

---

## ✅ Weryfikacja i publikacja kursu

### Po wygenerowaniu:

1. **Przejdź do Django Admin:**
   - https://szybkie-kursiki.pl/admin/

2. **Znajdź nowy kurs:**
   - Main app → Kursy
   - Kurs będzie miał status: `is_active = False` (draft)

3. **Zweryfikuj treść:**
   - Sprawdź czy wszystkie lekcje są poprawne
   - Przejrzyj quizy
   - Sprawdź zadania praktyczne

4. **Edytuj jeśli trzeba:**
   - Możesz poprawić treść
   - Dodać/usunąć elementy
   - Zmienić kolejność

5. **Opublikuj:**
   - Zaznacz `is_active = True`
   - Kliknij **Save**

6. **Kurs jest live!**
   - https://szybkie-kursiki.pl/course/[slug-kursu]/

---

## 🎯 Struktura wygenerowanego kursu

Każdy kurs zawiera:

### 📚 Kurs:
- Tytuł
- Krótki opis (max 200 znaków)
- Pełny opis
- Ikona (Font Awesome)
- Tagi

### 📖 Lekcje (minimum 3-5):
- Tytuł
- Kolejność
- **Treść** (Markdown, min 500 słów)
  - Szczegółowe wyjaśnienia
  - Przykłady kodu
  - Sekcje i podsekcje

### ❓ Quizy (dla każdej lekcji):
- 3-5 pytań wielokrotnego wyboru
- 4 odpowiedzi na pytanie
- Tylko 1 poprawna odpowiedź
- Wyjaśnienie poprawnej odpowiedzi

### 💻 Zadania praktyczne (dla każdej lekcji):
- Opis zadania
- Instrukcje krok po kroku
- Przykład
- Wskazówki
- Pełne rozwiązanie z wyjaśnieniem

---

## 🔍 Monitorowanie i logi

### Sprawdzenie statusu n8n:
```bash
docker logs n8n --tail 50
```

### Sprawdzenie statusu Django:
```bash
docker-compose logs web --tail 50
```

### Sprawdzenie wykonań workflow:
1. n8n → Executions
2. Zobacz historię wszystkich uruchomień
3. Sprawdź błędy jeśli są

---

## ⚠️ Troubleshooting - Najczęstsze problemy

### Problem 1: "Unauthorized" (403)

**Przyczyna:** Nieprawidłowy token

**Rozwiązanie:**
1. Sprawdź czy `COURSE_IMPORT_TOKEN` w Django `.env` jest taki sam jak w n8n
2. Zrestartuj Django: `docker-compose restart web`
3. Zrestartuj n8n: `docker-compose restart n8n`

---

### Problem 2: Workflow nie generuje kursu

**Przyczyna:** Brak Anthropic credentials

**Rozwiązanie:**
1. Sprawdź czy dodałeś Anthropic API credentials w n8n
2. Sprawdź czy credentials są przypisane do node "Generate Course with Claude"
3. Sprawdź czy API key jest ważny

---

### Problem 3: "Failed to parse Claude response"

**Przyczyna:** Claude zwrócił nieprawidłowy JSON

**Rozwiązanie:**
1. Spróbuj z prostszym promptem
2. Zmniejsz liczbę lekcji (3-4 zamiast 5-7)
3. Sprawdź logi w n8n → Executions

---

### Problem 4: Kurs nie pojawia się na stronie

**Przyczyna:** Kurs jest jako draft

**Rozwiązanie:**
1. Django Admin → Main app → Kursy
2. Znajdź kurs
3. Zaznacz `is_active = True`
4. Zapisz

---

### Problem 5: Timeout podczas generowania

**Przyczyna:** Zbyt długi kurs lub wolne API

**Rozwiązanie:**
1. Zmniejsz liczbę lekcji w prompcie
2. Spróbuj ponownie (czasem API jest wolniejsze)
3. Podziel kurs na 2 mniejsze

---

## 📊 Statystyki i limity

### Anthropic API (Claude):
- **Model:** claude-sonnet-4-5-20250929
- **Cost:** ~$3 na wejście/wyjście za 1M tokenów
- **Średni koszt kursu:** $0.10-0.30 (w zależności od długości)

### Czas generowania:
- Kurs 3 lekcje: ~2-3 minuty
- Kurs 5 lekcji: ~3-5 minut
- Kurs 7 lekcji: ~5-7 minut

### Limity:
- Max lekcji: brak (zalecane 5-7)
- Max długość promptu: 4096 znaków
- Timeout: 300 sekund (5 minut)

---

## 🔐 Bezpieczeństwo - WAŻNE!

### Tokeny i hasła:

❌ **NIE COMMITUJ** tokenów do Git
❌ **NIE UDOSTĘPNIAJ** publicznie
✅ **PRZECHOWUJ** w zmiennych środowiskowych
✅ **UŻYWAJ** długich, losowych tokenów (min 32 znaki)

### API endpoint:

✅ Zabezpieczony tokenem (`X-Import-Token`)
✅ Tylko HTTPS
✅ Kursy tworzone jako draft (wymagają weryfikacji)

### Zalecenia:

1. Zmień token co 3-6 miesięcy
2. Używaj różnych tokenów dla dev/prod
3. Monitoruj logi pod kątem nieautoryzowanych prób
4. Zawsze weryfikuj wygenerowane kursy przed publikacją

---

## 📂 Lokalizacja plików

### Workflow JSON:
```
/home/deploy/szybkie-kursiki/n8n-workflows/course-generator-workflow.json
/home/deploy/szybkie-kursiki/n8n-workflows/course-generator-webhook-workflow.json
```

### Dokumentacja:
```
/home/deploy/szybkie-kursiki/n8n-workflows/README.md
/home/deploy/szybkie-kursiki/n8n-workflows/QUICK_START.md
```

### Przykłady:
```
/home/deploy/szybkie-kursiki/n8n-workflows/examples/example-course.json
/home/deploy/szybkie-kursiki/n8n-workflows/examples/sample-prompts.md
```

### Skrypty testowe:
```
/home/deploy/szybkie-kursiki/n8n-workflows/scripts/test_import_api.py
/home/deploy/szybkie-kursiki/n8n-workflows/scripts/test_api.sh
```

---

## 🎓 Szybki checklist - Co musisz zrobić

### Konfiguracja jednorazowa:

- [ ] Dodać `COURSE_IMPORT_TOKEN` do `.env` w Django
- [ ] Zrestartować Django (`docker-compose restart web`)
- [ ] Dodać Anthropic API credentials w n8n
- [ ] Dodać zmienne środowiskowe w n8n (`DJANGO_APP_URL`, `COURSE_IMPORT_TOKEN`)
- [ ] Przypisać credentials do node w workflow
- [ ] Aktywować workflow w n8n

### Każde generowanie kursu:

- [ ] Przygotować dobry prompt (jasny, konkretny)
- [ ] Uruchomić workflow (manual lub webhook)
- [ ] Poczekać 2-5 minut
- [ ] Sprawdzić kurs w Django Admin
- [ ] Zweryfikować treść
- [ ] Opublikować (`is_active = True`)

---

## 📞 Kontakt i wsparcie

W razie problemów:

1. Sprawdź logi Docker: `docker-compose logs`
2. Sprawdź Executions w n8n
3. Przejrzyj ten dokument
4. Sprawdź `/home/deploy/szybkie-kursiki/n8n-workflows/README.md`

---

## 🎉 To wszystko!

System jest gotowy do generowania kursów. Wypróbuj najpierw z prostym kursem testowym, a potem generuj prawdziwe kursy dla użytkowników!

**Powodzenia!** 🚀
