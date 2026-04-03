# 🚀 Konfiguracja automatycznego generowania kursów - KROK PO KROKU

Wykonaj te kroki dokładnie w podanej kolejności.

---

## ✅ KROK 1: Wygeneruj token bezpieczeństwa

**Na serwerze, uruchom:**

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Skopiuj** wynik - to będzie Twój `COURSE_IMPORT_TOKEN`

**Przykład wyniku:**
```
xK7mP9nQ2rS5tU8vW1yZ4aB6cD9eF2gH3jK6lM9nP2qR5sT8uV1wX4yZ7aB0cD3
```

---

## ✅ KROK 2: Dodaj token do Django

**Edytuj plik `.env`:**

```bash
cd /home/deploy/szybkie-kursiki
nano .env
```

**Dodaj na końcu pliku:**
```bash
COURSE_IMPORT_TOKEN=<wklej-tutaj-token-z-kroku-1>
```

**Przykład:**
```bash
COURSE_IMPORT_TOKEN=xK7mP9nQ2rS5tU8vW1yZ4aB6cD9eF2gH3jK6lM9nP2qR5sT8uV1wX4yZ7aB0cD3
```

**Zapisz i wyjdź:**
- Naciśnij `Ctrl + O` (zapisz)
- Naciśnij `Enter` (potwierdź)
- Naciśnij `Ctrl + X` (wyjdź)

---

## ✅ KROK 3: Zrestartuj Django

```bash
cd /home/deploy/szybkie-kursiki
docker-compose restart web
```

**Poczekaj ~10 sekund**, aż aplikacja się zrestartuje.

**Sprawdź czy działa:**
```bash
docker-compose logs web --tail 20
```

Powinno być: `Booting worker` i `Listening at: http://0.0.0.0:8000`

---

## ✅ KROK 4: Zdobądź Anthropic API Key

**Krok 4.1 - Załóż konto (jeśli nie masz):**

1. Wejdź na: https://console.anthropic.com/
2. Kliknij **"Sign Up"**
3. Zarejestruj się emailem lub Google
4. Potwierdź email

**Krok 4.2 - Dodaj metodę płatności:**

1. Po zalogowaniu: **Settings** → **Billing**
2. Kliknij **"Add payment method"**
3. Wpisz dane karty kredytowej
4. Zapisz

**Krok 4.3 - Wygeneruj API Key:**

1. **Settings** → **API Keys**
2. Kliknij **"Create Key"**
3. Nazwij klucz: `n8n-szybkie-kursiki`
4. Kliknij **"Create Key"**
5. **SKOPIUJ KLUCZ** (zaczyna się od `sk-ant-...`)
6. **ZAPISZ GO GDZIEŚ BEZPIECZNIE** - zobaczysz go tylko raz!

**Przykład API key:**
```
sk-ant-api03-AbCdEfGhIjKlMnOpQrStUvWxYz1234567890
```

---

## ✅ KROK 5: Zaloguj się do n8n

**Krok 5.1 - Otwórz n8n:**

1. Otwórz przeglądarkę
2. Wejdź na: https://n8n.szybkie-kursiki.pl/

**Krok 5.2 - Zaloguj się:**

```
Username: admin
Password: /SGMfTh3B44ZG4CR8eSYNMgoKdMSW5t5
```

**Powinno Cię przekierować do głównego interfejsu n8n.**

---

## ✅ KROK 6: Dodaj Anthropic API Key do n8n

**Krok 6.1 - Otwórz Credentials:**

1. W n8n, kliknij **ikonę koła zębatego** (⚙️) w lewym dolnym rogu
2. Wybierz **"Credentials"**

**Krok 6.2 - Dodaj nowe credentials:**

1. Kliknij przycisk **"Add Credential"** (prawy górny róg)
2. W wyszukiwarce wpisz: `anthropic`
3. Kliknij **"Anthropic API"**

**Krok 6.3 - Wklej API Key:**

1. W polu **"API Key"** wklej klucz z kroku 4.3
2. Kliknij **"Save"**

**Gotowe!** Credentials zostały dodane.

---

## ✅ KROK 7: Dodaj zmienne środowiskowe w n8n

**Krok 7.1 - Otwórz Variables:**

1. W n8n, kliknij **ikonę koła zębatego** (⚙️)
2. Wybierz **"Variables"**

**Krok 7.2 - Dodaj pierwszą zmienną:**

1. Kliknij **"Add Variable"**
2. **Key:** `DJANGO_APP_URL`
3. **Value:** `https://szybkie-kursiki.pl`
4. Kliknij **"Save"**

**Krok 7.3 - Dodaj drugą zmienną:**

1. Kliknij **"Add Variable"** ponownie
2. **Key:** `COURSE_IMPORT_TOKEN`
3. **Value:** `<wklej token z kroku 1>`
4. Kliknij **"Save"**

**Przykład:**
```
Key: COURSE_IMPORT_TOKEN
Value: xK7mP9nQ2rS5tU8vW1yZ4aB6cD9eF2gH3jK6lM9nP2qR5sT8uV1wX4yZ7aB0cD3
```

---

## ✅ KROK 8: Skonfiguruj pierwszy workflow

**Krok 8.1 - Otwórz workflow:**

1. W n8n, kliknij **"Workflows"** w lewym menu
2. Znajdź workflow: **"Szybkie Kursiki - AI Course Generator"**
3. Kliknij na niego żeby otworzyć

**Krok 8.2 - Przypisz credentials do Claude:**

1. Kliknij na node **"Generate Course with Claude"** (drugi prostokąt od lewej)
2. W prawym panelu, znajdź pole **"Credential to connect with"**
3. Kliknij na dropdown
4. Wybierz credentials **"Anthropic API"** które dodałeś w kroku 6
5. Kliknij **"Save"** w prawym górnym rogu (ikona dyskietki)

**Krok 8.3 - Aktywuj workflow:**

1. W prawym górnym rogu znajdź przełącznik **"Inactive"**
2. Kliknij na niego żeby zmienić na **"Active"**
3. Workflow jest gotowy!

---

## ✅ KROK 9: Skonfiguruj drugi workflow (Webhook)

**Krok 9.1 - Otwórz drugi workflow:**

1. W n8n, kliknij **"Workflows"** w lewym menu
2. Znajdź workflow: **"Szybkie Kursiki - AI Course Generator (Webhook)"**
3. Kliknij na niego

**Krok 9.2 - Przypisz credentials:**

1. Kliknij na node **"Generate Course with Claude"**
2. W polu **"Credential to connect with"** wybierz **"Anthropic API"**
3. Kliknij **"Save"**

**Krok 9.3 - Aktywuj workflow:**

1. Zmień przełącznik na **"Active"**

**Oba workflow są gotowe!** 🎉

---

## ✅ KROK 10: TEST - Wygeneruj pierwszy kurs!

**Krok 10.1 - Otwórz workflow do testowania:**

1. W n8n, otwórz workflow: **"Szybkie Kursiki - AI Course Generator"**

**Krok 10.2 - Uruchom test:**

1. Kliknij przycisk **"Test workflow"** w prawym górnym rogu
2. Kliknij na node **"Manual Trigger"** (pierwszy prostokąt)
3. Kliknij przycisk **"Execute node"**

**Krok 10.3 - Dodaj dane testowe:**

W okienku, które się pojawi, wpisz:

```json
{
  "coursePrompt": "Stwórz prosty kurs testowy 'Podstawy Git' z 3 lekcjami: instalacja Git, pierwsze repozytorium, podstawowe komendy. Każda lekcja z quizem."
}
```

**Krok 10.4 - Uruchom:**

1. Kliknij **"Execute"**
2. **Poczekaj 2-5 minut** - workflow się wykonuje
3. Zobaczysz jak dane przechodzą przez wszystkie node

**Krok 10.5 - Sprawdź wynik:**

1. Kliknij na ostatni node **"Success Output"**
2. W dolnym panelu zobaczysz:
   - `status: success`
   - `course_title: Podstawy Git`
   - `course_slug: podstawy-git`
   - `admin_url: ...`
   - `preview_url: ...`

**Jeśli widzisz sukces - DZIAŁA!** 🎉

---

## ✅ KROK 11: Sprawdź kurs w Django Admin

**Krok 11.1 - Otwórz Django Admin:**

1. Wejdź na: https://szybkie-kursiki.pl/admin/
2. Zaloguj się swoimi danymi

**Krok 11.2 - Znajdź kurs:**

1. Kliknij **"Kursy"** w menu
2. Znajdź kurs **"Podstawy Git"**
3. Kliknij na niego

**Krok 11.3 - Sprawdź zawartość:**

1. Zobacz czy kurs ma:
   - ✅ Tytuł
   - ✅ Opis
   - ✅ Tagi
2. Przewiń w dół do **"Lekcje"**
3. Kliknij na pierwszą lekcję
4. Sprawdź czy ma:
   - ✅ Treść w Markdown
   - ✅ Quiz z pytaniami
   - ✅ Zadanie praktyczne

**Krok 11.4 - Opublikuj kurs:**

1. Wróć do edycji kursu
2. Znajdź pole **"Aktywny" (is_active)**
3. Zaznacz checkbox
4. Kliknij **"Save"**

**Krok 11.5 - Zobacz kurs na stronie:**

1. Otwórz: https://szybkie-kursiki.pl/course/podstawy-git/
2. **Kurs jest live!** 🚀

---

## 🎉 GRATULACJE! System działa!

Teraz możesz:

### Generować kursy ręcznie:

1. n8n → Workflow: "Szybkie Kursiki - AI Course Generator"
2. Test workflow → Execute
3. Wpisz swój prompt
4. Poczekaj 2-5 minut
5. Sprawdź w Django Admin
6. Opublikuj

### Generować kursy przez API:

```bash
curl -X POST https://n8n.szybkie-kursiki.pl/webhook/generate-course \
  -H "Content-Type: application/json" \
  -d '{
    "coursePrompt": "Stwórz kurs Docker dla developerów z 4 lekcjami"
  }'
```

---

## 📝 Przykładowe prompty do użycia

### Kurs Python:
```
Stwórz kurs "Python od podstaw" dla początkujących z 5 lekcjami:
1. Instalacja Python
2. Zmienne i typy danych
3. Instrukcje warunkowe
4. Pętle
5. Funkcje

Każda lekcja z przykładami kodu, quizem i zadaniem.
```

### Kurs JavaScript:
```
Kurs "JavaScript Modern ES6+" dla programistów:
- Arrow functions
- Promises i async/await
- Destructuring
- Spread operator
- Modules

Poziom: średniozaawansowany
```

### Kurs Docker:
```
Praktyczny kurs Docker dla developerów:
1. Czym jest Docker?
2. Podstawowe komendy
3. Dockerfile
4. Docker Compose
5. Best practices

Z przykładami z prawdziwych projektów.
```

---

## ⚠️ Co zrobić gdy coś nie działa?

### Problem: Workflow kończy się błędem "Unauthorized"

**Sprawdź:**
1. Czy `COURSE_IMPORT_TOKEN` w n8n jest taki sam jak w Django `.env`
2. Zrestartuj Django: `docker-compose restart web`

### Problem: Workflow nie generuje kursu

**Sprawdź:**
1. Czy Anthropic credentials są dodane
2. Czy credentials są przypisane do node "Generate Course with Claude"
3. Czy API key jest poprawny (nie wygasł)

### Problem: Kurs nie pojawia się na stronie

**Sprawdź:**
1. Django Admin → Kursy → Znajdź kurs
2. Czy `is_active = True`?
3. Jeśli nie - zaznacz i zapisz

### Problem: Timeout

**Rozwiązanie:**
1. Zmniejsz liczbę lekcji w prompcie (3-4 zamiast 5-7)
2. Spróbuj ponownie

---

## 📊 Logi i monitoring

### Sprawdź logi n8n:
```bash
docker logs n8n --tail 50 -f
```

### Sprawdź logi Django:
```bash
docker-compose logs web --tail 50 -f
```

### Sprawdź executions w n8n:
1. n8n → **Executions** (w lewym menu)
2. Zobacz historię wszystkich uruchomień
3. Kliknij na wykonanie żeby zobaczyć szczegóły

---

## 💰 Koszty

### Anthropic API:
- **Model:** Claude Sonnet 4.5
- **Koszt:** ~$3 za 1M tokenów (wejście/wyjście)
- **Średni koszt kursu:** $0.10 - $0.30
- **Kurs 3 lekcje:** ~$0.10
- **Kurs 5 lekcji:** ~$0.20
- **Kurs 7 lekcji:** ~$0.30

### Pierwsze $5 FREE od Anthropic! 🎁

To znaczy możesz wygenerować ~20-50 kursów za darmo!

---

## 🔐 Bezpieczeństwo - Zapamiętaj!

❌ **NIE commituj** `COURSE_IMPORT_TOKEN` do Git
❌ **NIE udostępniaj** publicznie API key
✅ **ZAWSZE** weryfikuj kursy przed publikacją
✅ **ZMIENIAJ** tokeny co 3-6 miesięcy

---

## 📁 Pliki do zapamiętania

### Workflow w n8n:
- **Manual:** "Szybkie Kursiki - AI Course Generator"
- **Webhook:** "Szybkie Kursiki - AI Course Generator (Webhook)"

### Linki:
- **n8n:** https://n8n.szybkie-kursiki.pl/
- **Django Admin:** https://szybkie-kursiki.pl/admin/
- **Anthropic Console:** https://console.anthropic.com/

### Dokumentacja:
- **Pełna:** `/home/deploy/szybkie-kursiki/n8n-workflows/README.md`
- **Ta instrukcja:** `/home/deploy/szybkie-kursiki/n8n-workflows/KROK_PO_KROKU.md`
- **Prompty:** `/home/deploy/szybkie-kursiki/n8n-workflows/examples/sample-prompts.md`

---

## ✅ Checklist końcowy

Sprawdź czy wszystko zrobiłeś:

- [ ] Wygenerowałeś `COURSE_IMPORT_TOKEN`
- [ ] Dodałeś token do `.env` w Django
- [ ] Zrestartowałeś Django
- [ ] Założyłeś konto Anthropic
- [ ] Dodałeś metodę płatności w Anthropic
- [ ] Wygenerowałeś Anthropic API Key
- [ ] Zalogowałeś się do n8n
- [ ] Dodałeś Anthropic credentials w n8n
- [ ] Dodałeś zmienne `DJANGO_APP_URL` i `COURSE_IMPORT_TOKEN` w n8n
- [ ] Skonfigurowałeś oba workflow (przypisałeś credentials)
- [ ] Aktywowałeś oba workflow
- [ ] Wygenerowałeś testowy kurs
- [ ] Sprawdziłeś kurs w Django Admin
- [ ] Opublikowałeś kurs

**Jeśli wszystko zaznaczone - GRATULACJE!** System działa! 🎉

---

## 🚀 Następne kroki

1. **Wygeneruj prawdziwy kurs** z dobrym promptem
2. **Zweryfikuj treść** w Django Admin
3. **Opublikuj** dla użytkowników
4. **Generuj więcej kursów!**

**Powodzenia!** 🎓
