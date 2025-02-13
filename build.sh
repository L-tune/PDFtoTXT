#!/bin/bash

# Очищаем предыдущие сборки
sudo rm -rf build dist
rm -rf __pycache__
rm -rf *.pyc

# Создаем виртуальное окружение
python3 -m venv venv

# Активируем виртуальное окружение
source venv/bin/activate

# Очищаем pip кэш
pip cache purge

# Устанавливаем зависимости
pip install --upgrade pip
pip install --upgrade setuptools wheel
pip install --no-cache-dir -r requirements.txt
pip install --no-cache-dir pyinstaller==6.3.0

# Проверяем установку всех необходимых модулей
python3 -c "import tkinter, pypdfium2, pdfplumber, charset_normalizer; print('charset_normalizer version:', charset_normalizer.__version__)"

# Собираем приложение
python3 -m PyInstaller setup.spec --clean --noconfirm

# Исправляем права доступа
if [ -d "dist/PDF to TXT Converter.app" ]; then
    sudo chmod -R 755 "dist/PDF to TXT Converter.app"
    
    # Исправляем права на исполняемые файлы
    sudo find "dist/PDF to TXT Converter.app" -type f -name "*.so" -exec chmod +x {} \;
    sudo find "dist/PDF to TXT Converter.app" -type f -name "*.dylib" -exec chmod +x {} \;
    sudo chmod +x "dist/PDF to TXT Converter.app/Contents/MacOS/"*
    
    echo "Приложение успешно создано в папке dist/"
    
    # Создаем DMG
    if command -v create-dmg &> /dev/null; then
        rm -f "dist/PDF to TXT Converter.dmg"
        
        create-dmg \
            --volname "PDF to TXT Converter" \
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

echo "Для проверки ошибок запустите:"
echo "/Applications/PDF\ to\ TXT\ Converter.app/Contents/MacOS/PDF\ to\ TXT\ Converter" 