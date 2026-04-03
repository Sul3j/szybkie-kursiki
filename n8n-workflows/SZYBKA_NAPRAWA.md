# 🔧 Szybka naprawa - Workflow bez błędu credentials

## Problem
Workflow pokazuje błąd "Credentials not found"

## ✅ Rozwiązanie - 2 minuty

### Krok 1: Dodaj ANTHROPIC_API_KEY do zmiennych n8n

1. **Zaloguj się do n8n:** https://n8n.szybkie-kursiki.pl/
2. **Kliknij Settings** (⚙️) → **Variables**
3. **Kliknij "Add Variable"**
4. Dodaj:
   - **Key:** `ANTHROPIC_API_KEY`
   - **Value:** Twój API key (zaczyna się od `sk-ant-...`)
5. **Kliknij "Save"**

### Krok 2: Otwórz workflow

**Link:** https://n8n.szybkie-kursiki.pl/workflow/3aef026d-25ba-48cb-a2e1-379b48071a37

### Krok 3: Edytuj node "Call Claude API"

1. **Kliknij** na node **"Call Claude API"**
2. W prawym panelu znajdź sekcję **"Authentication"**
3. Zmień na: **"None"** (zamiast "Predefined Credential Type")
4. Przewiń w dół do sekcji **"Headers"**
5. **Włącz** "Send Headers" jeśli nie jest włączone
6. **Dodaj header:**
   - Kliknij **"Add Header"**
   - **Name:** `x-api-key`
   - **Value:** `={{ $env.ANTHROPIC_API_KEY }}`
7. **Kliknij "Save"**

### Krok 4: Test

1. **"Test workflow"**
2. Kliknij node **"Manual Trigger"**
3. **"Execute node"**
4. Wpisz:
```json
{
  "coursePrompt": "Stwórz prosty kurs testowy 'Git Basics' z 2 lekcjami"
}
```
5. **"Execute"**
6. **Poczekaj 2-3 minuty**

**Powinno działać!** 🎉

---

## 🆘 Jeśli nadal nie działa

### Sprawdź czy masz API key:

1. Wejdź na: https://console.anthropic.com/settings/keys
2. Jeśli nie masz - kliknij **"Create Key"**
3. Skopiuj klucz (zaczyna się od `sk-ant-...`)
4. Dodaj jako zmienną w n8n (Krok 1 powyżej)

### Sprawdź format headera:

Node "Call Claude API" powinien mieć **3 headery**:
1. `anthropic-version` = `2023-06-01`
2. `x-api-key` = `={{ $env.ANTHROPIC_API_KEY }}`
3. `Content-Type` = `application/json` (dodany automatycznie)

---

## 📋 Podsumowanie - co zrobiłeś:

✅ Dodałeś `ANTHROPIC_API_KEY` do zmiennych n8n
✅ Zmieniłeś authentication na "None"
✅ Dodałeś header `x-api-key` z wartością `={{ $env.ANTHROPIC_API_KEY }}`
✅ Zapisałeś workflow
✅ Przetestowałeś

**Teraz workflow używa standardowego HTTP Request node z prostym headerem!** 🚀
