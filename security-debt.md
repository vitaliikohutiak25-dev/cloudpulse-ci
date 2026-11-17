# Security Audit & Technical Debt: CloudPulse API

## 1. онтекст системи
- **роєкт:** CloudPulse Telemetry API (Python/Flask + Redis у Docker).
- **ористувачі:** DevOps-інженери, внутрішні системи моніторингу.
- **ані:** мінні оточення (`NODE_NAME`, `APP_ENV`, `PORT`), мережеві порти, логи, кеш Redis.
- **Must-історії:**
  1. Як інженер, я хочу отримувати JSON-статус вузла через HTTP GET `/`.
  2. Як DevOps, я хочу змінювати конфігурацію середовища через ENV-змінні без перезбірки образу.

## 2. иявлені ризики безпеки (OWASP Top 10)
| ID | атегорія OWASP | изик | Severity |
|---|---|---|---|
| R-01 | A01 Broken Access Control | овнішній порт Redis (6379) відкритий без пароля (`requirepass`) | Critical |
| R-02 | A05 Security Misconfiguration | апуск Flask dev-сервера в контейнері замість Gunicorn + робота під `root` | High |
| R-03 | A07 Auth Failures | HTTP-ендпоінт `/` не має аутентифікації та Rate Limiting (ризик DoS) | High |
| R-04 | A05 Security Misconfiguration | рив'язка сокета до `0.0.0.0` (Bandit B104, CWE-605) + відсутність HTTPS | Medium |
| R-05 | A06 Vulnerable Components | разлива версія `flask 3.0.0` (PYSEC-2026-2151) — **СТ (оновлено до 3.1.3)** | Resolved |
| R-06 | A09 Logging Failures | оги не містять IP-адрес клієнтів та безпекових подій (4xx/5xx) | Low |

## 3. Технічний борг
1. **нфраструктура (High):** ідсутній non-root користувач у `Dockerfile` та файл `.dockerignore`.
2. **Серверна частина (High):** икористано `app.run()` замість `gunicorn` + відсутня валідація `PORT`.
3. **Тестування (Medium):** отребує додавання інтеграційних тестів взаємодії з Redis.
4. **окументація (Low):** е описано матрицю безпечних конфігурацій ENV у `README.md`.

## 4. лан погашення техборгу (1 спринт) та DoD
### иправляємо в поточному спринті:
- акрити порт `6379` Redis від зовнішнього хоста в `docker-compose.yml` та встановити пароль. *(DoD: порт 6379 недоступний зовні, підключення лише через `pulse_net` із паролем).*
- одати non-root користувача в `Dockerfile` та перейти на `gunicorn`. *(DoD: `whoami` у контейнері повертає `appuser`).*
- одати валідацію `APP_PORT` при старті. *(DoD: некоректний порт не викликає падіння з `ValueError`).*

### Свідомо відкладаємо на наступну ітерацію:
- провадження OAuth2/JWT та налаштування централізованого SIEM-логування.
