# CloudPulse Telemetry API

![CI Status](https://github.com/vitaliikohutiak25-dev/cloudpulse-ci/actions/workflows/ci.yml/badge.svg)

Мікросервіс системного моніторингу на базі Python/Flask із налаштованим CI/CD пайплайном у GitHub Actions.

## CI/CD
Автоматичний workflow (`.github/workflows/ci.yml`) запускається при кожному `push` або `pull_request` у гілку `main`.

### Етапи пайплайну:
1. **Checkout та Setup Python** — розгортання середовища одночасно на матриці версій Python **3.10** та **3.11**.
2. **Install dependencies** — встановлення `flask`, `pytest` та `pylint`.
3. **Lint (Pylint)** — перевірка стилю та якості коду (`app/main.py`).
4. **Build** — компіляція байт-коду (`python -m compileall app/`).
5. **Test (Pytest)** — запуск модульних тестів (`tests/test_app.py`).
6. **Package Artifact** — окремий job для збірки та збереження `cloudpulse-release.zip` як артефакту запуску.
