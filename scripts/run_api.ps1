# Запуск Django API на порту 8010
.\.venv\Scripts\Activate.ps1
Write-Host "Запуск Django API на http://127.0.0.1:8010/" -ForegroundColor Cyan
python manage.py runserver 127.0.0.1:8010
