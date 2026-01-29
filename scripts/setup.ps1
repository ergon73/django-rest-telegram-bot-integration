# Создание виртуального окружения и установка зависимостей
Write-Host "Создание виртуального окружения..." -ForegroundColor Cyan
python -m venv .venv

Write-Host "Активация окружения..." -ForegroundColor Cyan
.\.venv\Scripts\Activate.ps1

Write-Host "Установка зависимостей..." -ForegroundColor Cyan
pip install -r requirements.txt

Write-Host "Применение миграций..." -ForegroundColor Cyan
python manage.py makemigrations bot
python manage.py migrate

Write-Host "Готово!" -ForegroundColor Green
