# Przewodnik importu pytań do quizów z XML

## Wprowadzenie

Funkcjonalność importu XML pozwala na szybkie dodawanie wielu pytań do quizu jednocześnie, zamiast dodawania ich pojedynczo przez admin panel.

## Jak używać

### 1. Przejdź do quizu w admin panelu

1. Zaloguj się do admin panelu Django
2. Przejdź do **Quizy** w menu
3. Wybierz quiz, do którego chcesz dodać pytania
4. Kliknij przycisk **"Importuj pytania z XML"** na dole strony edycji quizu

### 2. Wklej kod XML

Na stronie importu zobaczysz:
- Pole tekstowe do wklejenia kodu XML
- Przykładowy format XML
- Instrukcje dotyczące formatu

### 3. Format XML

Poniżej znajdziesz szczegółowy opis formatu XML:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<questions>
  <question order="1">
    <text>Treść pytania</text>
    <explanation>Wyjaśnienie odpowiedzi (opcjonalne)</explanation>
    <answers>
      <answer correct="true" order="1">Poprawna odpowiedź</answer>
      <answer correct="false" order="2">Niepoprawna odpowiedź</answer>
      <answer correct="false" order="3">Inna niepoprawna odpowiedź</answer>
    </answers>
  </question>
  <question order="2">
    <text>Kolejne pytanie</text>
    <answers>
      <answer correct="false" order="1">Odpowiedź A</answer>
      <answer correct="true" order="2">Odpowiedź B</answer>
    </answers>
  </question>
</questions>
```

## Struktura XML

### Element główny: `<questions>`

Wszystkie pytania muszą być zawarte w elemencie `<questions>`.

### Element pytania: `<question>`

Każde pytanie powinno mieć:

- **Atrybut `order`** (wymagany): Określa kolejność pytania w quizie
  ```xml
  <question order="1">
  ```

- **Element `<text>`** (wymagany): Treść pytania
  ```xml
  <text>Jakie jest znaczenie operatora == w Pythonie?</text>
  ```

- **Element `<explanation>`** (opcjonalny): Wyjaśnienie poprawnej odpowiedzi
  ```xml
  <explanation>Operator == porównuje wartości dwóch obiektów.</explanation>
  ```

- **Element `<answers>`** (wymagany): Kontener dla odpowiedzi
  ```xml
  <answers>
    <!-- odpowiedzi tutaj -->
  </answers>
  ```

### Element odpowiedzi: `<answer>`

Każda odpowiedź powinna mieć:

- **Atrybut `correct`** (wymagany): `"true"` dla poprawnej odpowiedzi, `"false"` dla niepoprawnej
  ```xml
  <answer correct="true" order="1">
  ```

- **Atrybut `order`** (wymagany): Określa kolejność wyświetlania odpowiedzi
  ```xml
  <answer correct="false" order="2">
  ```

- **Treść tekstowa**: Tekst odpowiedzi
  ```xml
  <answer correct="true" order="1">To jest poprawna odpowiedź</answer>
  ```

## Zaawansowane funkcje

### Bloki kodu w pytaniach

Pytania mogą zawierać składnię Markdown, w tym bloki kodu:

```xml
<question order="1">
  <text>Co wypisze poniższy kod?
```python
def hello():
    print("Hello, World!")
hello()
```
  </text>
  <answers>
    <answer correct="true" order="1">Hello, World!</answer>
    <answer correct="false" order="2">hello()</answer>
  </answers>
</question>
```

### Znaki specjalne

W XML niektóre znaki muszą być escape'owane:

- `<` → `&lt;`
- `>` → `&gt;`
- `&` → `&amp;`
- `"` → `&quot;`
- `'` → `&apos;`

Przykład:

```xml
<text>Porównaj 5 &lt; 10</text>
```

## Przykłady

### Przykład 1: Podstawowy quiz programistyczny

```xml
<?xml version="1.0" encoding="UTF-8"?>
<questions>
  <question order="1">
    <text>Który typ danych w Pythonie jest niezmienny (immutable)?</text>
    <explanation>Tuple jest typem niemutowalnym - po utworzeniu nie można zmienić jego elementów.</explanation>
    <answers>
      <answer correct="false" order="1">List</answer>
      <answer correct="true" order="2">Tuple</answer>
      <answer correct="false" order="3">Dictionary</answer>
      <answer correct="false" order="4">Set</answer>
    </answers>
  </question>

  <question order="2">
    <text>Co zwróci następujące wyrażenie: len([1, 2, 3])?</text>
    <answers>
      <answer correct="false" order="1">1</answer>
      <answer correct="false" order="2">2</answer>
      <answer correct="true" order="3">3</answer>
      <answer correct="false" order="4">6</answer>
    </answers>
  </question>
</questions>
```

### Przykład 2: Quiz z blokami kodu

```xml
<?xml version="1.0" encoding="UTF-8"?>
<questions>
  <question order="1">
    <text>Co wypisze poniższy kod?
```python
x = [1, 2, 3]
x.append(4)
print(x[-1])
```
    </text>
    <explanation>Metoda append() dodaje element na koniec listy, a x[-1] pobiera ostatni element.</explanation>
    <answers>
      <answer correct="false" order="1">1</answer>
      <answer correct="false" order="2">3</answer>
      <answer correct="true" order="3">4</answer>
      <answer correct="false" order="4">Błąd</answer>
    </answers>
  </question>
</questions>
```

### Przykład 3: Quiz matematyczny

```xml
<?xml version="1.0" encoding="UTF-8"?>
<questions>
  <question order="1">
    <text>Ile wynosi 2 + 2 * 2?</text>
    <explanation>Zgodnie z kolejnością działań, mnożenie wykonuje się przed dodawaniem: 2 + (2 * 2) = 2 + 4 = 6</explanation>
    <answers>
      <answer correct="false" order="1">8</answer>
      <answer correct="true" order="2">6</answer>
      <answer correct="false" order="3">4</answer>
      <answer correct="false" order="4">10</answer>
    </answers>
  </question>

  <question order="2">
    <text>Który operator oznacza resztę z dzielenia w Pythonie?</text>
    <answers>
      <answer correct="false" order="1">/</answer>
      <answer correct="false" order="2">//</answer>
      <answer correct="true" order="3">%</answer>
      <answer correct="false" order="4">**</answer>
    </answers>
  </question>
</questions>
```

## Walidacja i komunikaty błędów

System automatycznie sprawdza:

### ✅ Co jest sprawdzane:
- Poprawność składni XML
- Obecność elementu głównego `<questions>`
- Obecność wymaganego pola `<text>` w każdym pytaniu
- Obecność odpowiedzi dla każdego pytania
- Poprawność atrybutów `correct` i `order`

### ❌ Możliwe błędy:

1. **"Błąd parsowania XML"** - Niepoprawna składnia XML
2. **"Nieprawidłowy format XML. Element główny musi być <questions>"** - Zły element główny
3. **"Pominięto pytanie bez tekstu"** - Pytanie nie ma elementu `<text>`
4. **"Pytanie nie ma odpowiedzi"** - Brak elementu `<answers>` lub brak odpowiedzi w środku

## Po imporcie

Po udanym imporcie:
1. Zobaczysz komunikat: **"Pomyślnie zaimportowano X pytań do quizu"**
2. Zostaniesz przekierowany do strony edycji quizu
3. Wszystkie zaimportowane pytania będą widoczne na liście
4. Możesz edytować pytania indywidualnie, jeśli zajdzie taka potrzeba

## Dobre praktyki

1. **Testuj małe partie** - Zacznij od zaimportowania 1-2 pytań, aby upewnić się, że format jest poprawny
2. **Używaj kolejności** - Ustaw sensowne wartości `order` dla pytań i odpowiedzi
3. **Dodawaj wyjaśnienia** - Element `<explanation>` pomaga użytkownikom zrozumieć, dlaczego odpowiedź jest poprawna
4. **Waliduj XML** - Użyj walidatora XML online przed importem, aby wykryć błędy składni
5. **Zachowaj backup** - Przed importem dużej liczby pytań, zapisz XML w pliku na wypadek konieczności poprawek

## Narzędzia pomocnicze

### Walidatory XML online:
- https://www.xmlvalidation.com/
- https://codebeautify.org/xmlvalidator

### Edytory z podświetlaniem składni:
- VS Code z rozszerzeniem "XML Tools"
- Sublime Text
- Notepad++ z pluginem XML Tools

## Rozwiązywanie problemów

### Problem: "Błąd parsowania XML"

**Rozwiązanie:**
- Sprawdź, czy wszystkie tagi są poprawnie zamknięte
- Upewnij się, że używasz znaków escape dla `<`, `>`, `&`
- Użyj walidatora XML online

### Problem: "Nie zaimportowano żadnych pytań"

**Rozwiązanie:**
- Sprawdź, czy każde pytanie ma element `<text>`
- Upewnij się, że każde pytanie ma element `<answers>` z przynajmniej jedną odpowiedzią
- Sprawdź logi błędów - mogą być komunikaty o pominiętych pytaniach

### Problem: Znaki specjalne wyświetlają się niepoprawnie

**Rozwiązanie:**
- Użyj odpowiednich encji XML (`&lt;`, `&gt;`, `&amp;`, etc.)
- Upewnij się, że plik jest zapisany w kodowaniu UTF-8
- Dodaj deklarację kodowania w pierwszej linii: `<?xml version="1.0" encoding="UTF-8"?>`

## Wsparcie

Jeśli napotkasz problemy z importem XML:
1. Sprawdź, czy format XML jest zgodny z przykładami w tym przewodniku
2. Użyj walidatora XML, aby sprawdzić składnię
3. Skontaktuj się z administratorem systemu

---

**Powodzenia w tworzeniu quizów!** 🎓
