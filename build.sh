#!/bin/bash

# Очищаем предыдущие сборки
rm -rf build dist
rm -rf __pycache__
rm -rf *.pyc

# Создаем виртуальное окружение
python3 -m venv venv

# Активируем виртуальное окружение
source venv/bin/activate

# Устанавливаем зависимости
pip install --upgrade pip
pip install --upgrade setuptools wheel
pip install -r requirements.txt
pip install pyinstaller==6.3.0

# Проверяем установку charset-normalizer
python3 -c "import charset_normalizer; print('charset-normalizer version:', charset_normalizer.__version__)"

# Собираем приложение
python3 -m PyInstaller setup.spec --clean --noconfirm

# Исправляем права доступа
if [ -d "dist/PDF to TXT Converter.app" ]; then
    chmod -R 755 "dist/PDF to TXT Converter.app"
    echo "Приложение успешно создано в папке dist/"
    
    # Создаем DMG
    if command -v create-dmg &> /dev/null; then
        # Удаляем старый DMG если существует
        rm -f "dist/PDF to TXT Converter.dmg"
        
        # Создаем DMG
        create-dmg \
            --volname "PDF to TXT Converter" \
            --volicon "app_icon.icns" \
            --window-pos 200 120 \
            --window-size 800 400 \
            --icon-size 100 \
            --icon "PDF to TXT Converter.app" 200 190 \
            --hide-extension "PDF to TXT Converter.app" \
            --app-drop-link 600 185 \
            "dist/PDF to TXT Converter.dmg" \
            "dist/PDF to TXT Converter.app"
            
        echo "DMG файл создан в папке dist/"
    else
        echo "Предупреждение: create-dmg не установлен. DMG файл не был создан."
        echo "Установите create-dmg командой: brew install create-dmg"
    fi
else
    echo "Ошибка: Приложение не было создано"
    exit 1
fi

# Деактивируем виртуальное окружение
deactivate 