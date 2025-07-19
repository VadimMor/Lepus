import os
import subprocess
import sys
from pathlib import Path

def create_venv():
    if not Path("venv").exists():
        print("📦 Создание виртуального окружения...")
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
    else:
        print("✅ Виртуальное окружение уже существует.")

def install_requirements(path):
    print(f"📥 Установка зависимостей из {path}...")
    pip = Path("venv") / "Scripts" / "pip.exe" if os.name == "nt" else Path("venv/bin/pip")
    subprocess.check_call([str(pip), "install", "-r", path])

def setup_server_env():
    print("\n🛠️ Настройка сервера PostgreSQL:")
    db_url = input("Введите DATABASE_URL (например, postgresql://user:pass@localhost/dbname): ").strip()
    env_path = Path("server") / ".env"
    env_path.write_text(f'DATABASE_URL="{db_url}"\n')
    print(f"✅ .env файл создан: {env_path}")

def setup_client_env():
    print("\n🌐 Настройка клиента:")
    server_url = input("Введите адрес сервера (например, http://localhost:8000/alerts): ").strip()
    env_path = Path("client") / ".env"
    env_path.write_text(f'SERVER_URL="{server_url}"\n')
    print(f"✅ .env файл создан: {env_path}")

def print_server_instructions():
    print("""
🚀 Установка сервера завершена!

👉 Запуск API:
    uvicorn server.main:app --reload
""")

def print_client_instructions():
    print("""
🚀 Установка клиента завершена!

👉 1. Обучение базовой модели:
    python client/create_data.py

👉 2. Запуск мониторинга:
    python client/main.py
""")

def main():
    print("🧠 Lepus Installer")
    print("1. Установить сервер")
    print("2. Установить клиент")
    choice = input("Выберите опцию (1 или 2): ").strip()

    create_venv()

    if choice == "1":
        install_requirements("server/requirements.txt")
        setup_server_env()
        print_server_instructions()
    elif choice == "2":
        install_requirements("client/requirements.txt")
        setup_client_env()
        print_client_instructions()
    else:
        print("❌ Неверный выбор. Перезапустите установщик.")

if __name__ == "__main__":
    main()
