# Instrukcja Deployment - Szybkie Kursiki

Kompleksowy przewodnik wdrożenia aplikacji Django na serwer VPS z automatycznym CI/CD przez GitHub Actions.

## Spis treści

1. [Wymagania](#wymagania)
2. [Konfiguracja VPS](#konfiguracja-vps)
3. [Konfiguracja GitHub](#konfiguracja-github)
4. [Pierwsze wdrożenie](#pierwsze-wdrożenie)
5. [SSL/HTTPS z Let's Encrypt](#ssl-https-z-lets-encrypt)
6. [Automatyczne wdrożenia](#automatyczne-wdrożenia)
7. [Rozwiązywanie problemów](#rozwiązywanie-problemów)

---

## Wymagania

### Na lokalnej maszynie:
- Git
- Dostęp do repozytorium GitHub

### Na serwerze VPS:
- Ubuntu 20.04 LTS lub nowszy
- Minimum 2GB RAM (zalecane 4GB)
- 20GB przestrzeni dyskowej
- Dostęp root lub sudo
- Domena wskazująca na adres IP serwera

---

## Konfiguracja VPS

### Krok 1: Połącz się z VPS

```bash
ssh root@twoj-serwer-ip
```

### Krok 2: Aktualizacja systemu

```bash
apt update && apt upgrade -y
```

### Krok 3: Instalacja wymaganych pakietów

```bash
# Instalacja Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Instalacja Docker Compose
apt install docker-compose-plugin -y

# Instalacja Git
apt install git -y

# Weryfikacja instalacji
docker --version
docker compose version
```

### Krok 4: Utworzenie użytkownika deployment

**Dla Ubuntu/Debian:**

```bash
# Utwórz użytkownika deploy
sudo adduser deploy

# Dodaj użytkownika do grupy docker
sudo usermod -aG docker deploy

# Dodaj użytkownika do grupy sudo
sudo usermod -aG sudo deploy

# Przełącz się na użytkownika deploy
su - deploy
```

**Dla CentOS/RHEL/AlmaLinux:**

```bash
# Utwórz użytkownika deploy
sudo useradd -m -s /bin/bash deploy
sudo passwd deploy

# Dodaj użytkownika do grupy docker
sudo usermod -aG docker deploy

# Dodaj użytkownika do grupy wheel (sudo dla RHEL)
sudo usermod -aG wheel deploy

# Przełącz się na użytkownika deploy
su - deploy
```

### Krok 5: Konfiguracja SSH dla GitHub Actions

```bash
# Jako użytkownik deploy
cd ~
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Wygeneruj klucz SSH (bez hasła dla automatyzacji)
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/github_actions

# Dodaj klucz publiczny do authorized_keys
cat ~/.ssh/github_actions.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# Wyświetl klucz prywatny (skopiuj go dla GitHub Secrets)
cat ~/.ssh/github_actions
```

**WAŻNE:** Skopiuj cały klucz prywatny (wraz z nagłówkami `-----BEGIN` i `-----END`).

### Krok 6: Klonowanie repozytorium

```bash
# Jako użytkownik deploy
cd /home/deploy

# Sklonuj repozytorium (zamień na swój URL)
git clone https://github.com/twoj-username/szybkie-kursiki.git

# Przejdź do katalogu projektu
cd szybkie-kursiki
```

### Krok 7: Utworzenie pliku .env

```bash
# Skopiuj przykładowy plik
cp .env.example .env

# Edytuj plik .env
nano .env
```

Wypełnij plik `.env` następującymi danymi:

```env
# Django Settings
DJANGO_SECRET_KEY='wygeneruj-silny-klucz-tutaj'
DJANGO_DEBUG='0'
DJANGO_ALLOWED_HOSTS='twoja-domena.com,www.twoja-domena.com'
DJANGO_SETTINGS_MODULE='app.settings'

# MySQL Database Configuration
MYSQL_DATABASE='szybkie_kursiki_db'
MYSQL_USER='szybkie_kursiki_user'
MYSQL_PASSWORD='silne-haslo-bazy-danych'
MYSQL_ROOT_PASSWORD='silne-haslo-root'
MYSQL_HOST='db'
MYSQL_PORT='3306'
```

**Generowanie DJANGO_SECRET_KEY:**

```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Krok 8: Konfiguracja Nginx

```bash
# Edytuj konfigurację nginx
nano nginx/conf.d/app.conf
```

Zamień `yourdomain.com` na swoją domenę w pliku konfiguracyjnym.

### Krok 9: Utworzenie katalogów dla certyfikatów

```bash
mkdir -p certbot/conf certbot/www
```

---

## Konfiguracja GitHub

### Krok 1: Dodanie GitHub Secrets

Przejdź do swojego repozytorium GitHub:
1. Kliknij **Settings** → **Secrets and variables** → **Actions**
2. Kliknij **New repository secret**

Dodaj następujące sekrety:

| Nazwa | Wartość | Opis |
|-------|---------|------|
| `VPS_HOST` | `twoj-serwer-ip` | Adres IP serwera VPS |
| `VPS_USERNAME` | `deploy` | Nazwa użytkownika na VPS |
| `VPS_SSH_KEY` | `[klucz prywatny]` | Klucz prywatny SSH z kroku 5 |
| `VPS_PORT` | `22` | Port SSH (domyślnie 22) |
| `DJANGO_SECRET_KEY` | `[wygenerowany klucz]` | Django secret key |
| `DJANGO_ALLOWED_HOSTS` | `twoja-domena.com,www.twoja-domena.com` | Dozwolone hosty |
| `MYSQL_DATABASE` | `szybkie_kursiki_db` | Nazwa bazy danych |
| `MYSQL_USER` | `szybkie_kursiki_user` | Użytkownik MySQL |
| `MYSQL_PASSWORD` | `[hasło]` | Hasło użytkownika MySQL |
| `MYSQL_ROOT_PASSWORD` | `[hasło root]` | Hasło root MySQL |

### Krok 2: Weryfikacja workflow

Sprawdź czy plik `.github/workflows/deploy.yml` istnieje w repozytorium.

---

## Pierwsze wdrożenie

### Krok 1: Manualne wdrożenie (pierwsze uruchomienie)

```bash
# Na serwerze VPS jako użytkownik deploy
cd /home/deploy/szybkie-kursiki

# Uruchom kontenery (bez SSL na razie)
docker compose -f docker-compose.production.yml up -d

# Sprawdź status kontenerów
docker compose -f docker-compose.production.yml ps

# Sprawdź logi
docker compose -f docker-compose.production.yml logs -f
```

### Krok 2: Utworzenie superusera Django

```bash
docker compose -f docker-compose.production.yml exec web python manage.py createsuperuser
```

### Krok 3: Testowanie aplikacji

Otwórz przeglądarkę i przejdź do `http://twoja-domena.com` lub `http://twoj-serwer-ip`.

---

## SSL/HTTPS z Let's Encrypt

### Krok 1: Zatrzymaj nginx tymczasowo

```bash
docker compose -f docker-compose.production.yml stop nginx
```

### Krok 2: Uzyskaj certyfikat SSL

```bash
# Zamień twoja-domena.com i email@example.com na swoje dane
docker compose -f docker-compose.production.yml run --rm certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  -d twoja-domena.com \
  -d www.twoja-domena.com \
  --email email@example.com \
  --agree-tos \
  --no-eff-email
```

### Krok 3: Aktualizacja konfiguracji nginx

```bash
nano nginx/conf.d/app.conf
```

1. Odkomentuj linie z certyfikatami SSL (linie zaczynające się od `# ssl_`)
2. Zamień `yourdomain.com` na swoją domenę
3. Zakomentuj lub usuń sekcję "Temporary HTTP-only server"

### Krok 4: Restart nginx

```bash
docker compose -f docker-compose.production.yml up -d nginx
```

### Krok 5: Weryfikacja SSL

Otwórz `https://twoja-domena.com` w przeglądarce i sprawdź czy certyfikat działa.

### Automatyczne odnawianie certyfikatów

Certyfikaty będą automatycznie odnawiane przez kontener certbot co 12 godzin.

---

## Automatyczne wdrożenia

Po skonfigurowaniu GitHub Secrets, każdy push do gałęzi `main` automatycznie:

1. Połączy się z serwerem VPS przez SSH
2. Pobierze najnowszy kod z GitHub
3. Utworzy plik `.env` z sekretów GitHub
4. Zbuduje i uruchomi kontenery Docker
5. Wykona migracje bazy danych
6. Zbierze pliki statyczne
7. Wyczyści nieużywane zasoby Docker

### Ręczne uruchomienie deployment

Możesz również uruchomić deployment ręcznie:
1. Przejdź do **Actions** w GitHub
2. Wybierz **Deploy to VPS**
3. Kliknij **Run workflow**

---

## Rozwiązywanie problemów

### Problem: Kontenery nie startują

```bash
# Sprawdź logi
docker compose -f docker-compose.production.yml logs

# Sprawdź status kontenerów
docker compose -f docker-compose.production.yml ps

# Restart wszystkich kontenerów
docker compose -f docker-compose.production.yml restart
```

### Problem: Błędy bazy danych

```bash
# Sprawdź logi bazy danych
docker compose -f docker-compose.production.yml logs db

# Restart kontenera bazy danych
docker compose -f docker-compose.production.yml restart db

# Wykonaj migracje ponownie
docker compose -f docker-compose.production.yml exec web python manage.py migrate
```

### Problem: Statyczne pliki nie ładują się

```bash
# Zbierz pliki statyczne ponownie
docker compose -f docker-compose.production.yml exec web python manage.py collectstatic --noinput

# Restart nginx
docker compose -f docker-compose.production.yml restart nginx
```

### Problem: GitHub Actions nie może się połączyć

1. Sprawdź czy klucz SSH jest poprawnie dodany do GitHub Secrets
2. Sprawdź czy użytkownik `deploy` ma dostęp SSH
3. Sprawdź czy port SSH jest otwarty w firewall

```bash
# Na serwerze VPS
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Problem: Nginx pokazuje 502 Bad Gateway

```bash
# Sprawdź czy kontener web działa
docker compose -f docker-compose.production.yml ps web

# Sprawdź logi web
docker compose -f docker-compose.production.yml logs web

# Restart web
docker compose -f docker-compose.production.yml restart web
```

### Przydatne komendy

```bash
# Zobacz wszystkie działające kontenery
docker ps

# Zobacz logi konkretnego kontenera
docker compose -f docker-compose.production.yml logs -f [nazwa-serwisu]

# Wykonaj komendę w kontenerze
docker compose -f docker-compose.production.yml exec web [komenda]

# Restart wszystkich kontenerów
docker compose -f docker-compose.production.yml restart

# Zatrzymaj wszystkie kontenery
docker compose -f docker-compose.production.yml down

# Usuń wszystkie kontenery i wolumeny (UWAGA: usuwa dane!)
docker compose -f docker-compose.production.yml down -v

# Sprawdź użycie miejsca przez Docker
docker system df

# Wyczyść nieużywane zasoby
docker system prune -a
```

---

## Aktualizacje i konserwacja

### Aktualizacja aplikacji

Wystarczy wykonać `git push` do gałęzi `main` - GitHub Actions automatycznie wdroży zmiany.

### Backup bazy danych

```bash
# Utwórz backup
docker compose -f docker-compose.production.yml exec db mysqldump -u root -p$MYSQL_ROOT_PASSWORD $MYSQL_DATABASE > backup_$(date +%Y%m%d_%H%M%S).sql

# Przywróć backup
docker compose -f docker-compose.production.yml exec -T db mysql -u root -p$MYSQL_ROOT_PASSWORD $MYSQL_DATABASE < backup_file.sql
```

### Monitoring

Zalecane narzędzia do monitorowania:
- **Docker stats**: `docker stats`
- **htop**: Monitoring zasobów serwera
- **Logwatch**: Analiza logów systemowych
- **Uptime Robot**: Monitoring dostępności strony

---

## Bezpieczeństwo

### Zalecenia:

1. **Firewall**:
   ```bash
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

2. **Fail2Ban** (ochrona przed atakami brute-force):
   ```bash
   sudo apt install fail2ban -y
   sudo systemctl enable fail2ban
   sudo systemctl start fail2ban
   ```

3. **Regularne aktualizacje**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

4. **Silne hasła**: Używaj generatora haseł dla wszystkich sekretów

5. **Backup**: Regularnie twórz kopie zapasowe bazy danych

---

## Kontakt i wsparcie

W przypadku problemów:
1. Sprawdź sekcję [Rozwiązywanie problemów](#rozwiązywanie-problemów)
2. Sprawdź logi aplikacji i serwera
3. Utwórz issue w repozytorium GitHub

---

**Powodzenia z deploymentem!** 🚀
