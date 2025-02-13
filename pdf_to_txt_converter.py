import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from pathlib import Path
import pdfplumber
import traceback
from tkinter import font
import tkinter as tk
from PIL import Image
import sys

def get_resource_path(relative_path):
    """Получаем путь к ресурсу, работающий как в разработке, так и в собранном приложении"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller создает временную папку и хранит путь в _MEIPASS
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

class PDFConverter:
    def __init__(self):
        # Сначала создаем главное окно
        ctk.set_appearance_mode("light")
        self.root = ctk.CTk()
        self.root.title("PDF Converter")
        
        # Теперь загружаем шрифты
        self.load_custom_fonts()
        
        # Размеры и позиционирование
        window_width = 1200
        window_height = 800
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Цвета
        self.colors = {
            'background': "#FFFFFF",
            'text_primary': "#000000",
            'text_secondary': "#666666",
            'accent': "#000000",
            'surface': "#F8F8F8",  # Более светлый серый для фона
            'highlight': "#F4F4F4"  # Едва заметный серый для подсветки
        }
        
        self.root.configure(fg_color=self.colors['background'])
        
        # Главный контейнер
        main_frame = ctk.CTkFrame(
            self.root,
            fg_color=self.colors['background'],
            corner_radius=30
        )
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Основной контент
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20)
        
        # Заголовок
        headline_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        headline_frame.pack(fill="x", pady=(0, 20))
        
        main_title = ctk.CTkLabel(
            headline_frame,
            text="LTUNEOUSLY",
            font=ctk.CTkFont(family=self.fonts['title'][0], size=self.fonts['title'][1]),
            text_color=self.colors['text_primary']
        )
        main_title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            headline_frame,
            text="PDF CONVERSION",
            font=ctk.CTkFont(family=self.fonts['subtitle'][0], size=self.fonts['subtitle'][1]),
            text_color=self.colors['text_primary']
        )
        subtitle.pack(anchor="w")
        
        # Статистика
        stats_frame = ctk.CTkFrame(
            content_frame,
            fg_color=self.colors['surface'],
            corner_radius=20
        )
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # Левая колонка со статистикой
        stats_left = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_left.pack(side="left", padx=20, pady=20)
        
        self.converted_count = ctk.CTkLabel(
            stats_left,
            text="0",
            font=ctk.CTkFont(family=self.fonts['stats'][0], size=self.fonts['stats'][1]),
            text_color=self.colors['text_primary']
        )
        self.converted_count.pack(anchor="w")
        
        converted_label = ctk.CTkLabel(
            stats_left,
            text="Files converted",
            font=ctk.CTkFont(family=self.fonts['label'][0], size=self.fonts['label'][1]),
            text_color=self.colors['text_secondary']
        )
        converted_label.pack(anchor="w")
        
        # Фрейм для процента и кнопки
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(0, 20))
        
        # Процент над кнопкой (увеличиваем размер в 2 раза)
        self.total_percent_label = ctk.CTkLabel(
            button_frame,
            text="0%",
            font=ctk.CTkFont(family=self.fonts['button'][0], size=self.fonts['button'][1] * 2),  # Удваиваем размер
            text_color=self.colors['text_primary']
        )
        self.total_percent_label.pack(anchor="w", pady=(0, 5))
        
        # Кнопка конвертации
        self.convert_button = ctk.CTkButton(
            button_frame,
            text="Select PDF Folder",
            command=self.process_folder,
            font=ctk.CTkFont(family=self.fonts['button'][0], size=self.fonts['button'][1]),
            fg_color=self.colors['accent'],
            hover_color=self.colors['text_secondary'],
            height=45,
            width=180,
            corner_radius=22
        )
        self.convert_button.pack(anchor="w")
        
        # Прогресс
        progress_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        progress_frame.pack(fill="x")
        
        # Изначально скрываем статус "Ready to convert"
        self.status_label = ctk.CTkLabel(
            progress_frame,
            text="",  # Пустой текст
            font=ctk.CTkFont(family=self.fonts['label'][0], size=self.fonts['label'][1]),
            text_color=self.colors['text_secondary']
        )
        self.status_label.pack(anchor="w", pady=(0, 10))
        
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            height=4,
            progress_color=self.colors['accent'],
            fg_color=self.colors['surface']
        )
        self.progress_bar.pack(fill="x")
        self.progress_bar.set(0)
        
        # Область результатов
        self.files_textbox = ctk.CTkTextbox(
            content_frame,
            font=ctk.CTkFont(family=self.fonts['text'][0], size=self.fonts['text'][1]),
            fg_color=self.colors['surface'],
            text_color=self.colors['text_primary'],
            corner_radius=15,
            border_width=0
        )
        self.files_textbox.pack(fill="both", expand=True, pady=(20, 0))
        
        # Обновляем теги для текстбокса только с цветами
        self.files_textbox.tag_config("success", foreground="#000000")  # Завершенные файлы
        self.files_textbox.tag_config("progress", foreground="#666666")  # Текущий прогресс
        self.files_textbox.tag_config("complete", foreground="#000000")  # Финальное сообщение
        self.files_textbox.tag_config("error", foreground="#FF3B30")  # Ошибки

        # Добавляем копирайт внизу
        copyright_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        copyright_frame.pack(fill="x", pady=(15, 0))

        copyright_text = ctk.CTkLabel(
            copyright_frame,
            text="Created by Alexey Evdokimov © 2025",
            font=ctk.CTkFont(family=self.fonts['label'][0], size=12),
            text_color=self.colors['text_secondary']
        )
        copyright_text.pack(side="right")

    def load_custom_fonts(self):
        """Загрузка кастомных шрифтов"""
        try:
            fonts_path = get_resource_path(os.path.join('src', 'fonts'))
            
            # Регистрируем шрифты
            font_files = {
                'Inter-Regular': 'Inter_24pt-Regular.ttf',
                'Inter-Black': 'Inter_28pt-Black.ttf',
                'SpaceGrotesk-Bold': 'SpaceGrotesk-Bold.ttf',
                'SpaceGrotesk-Light': 'SpaceGrotesk-Light.ttf',
                'SpaceGrotesk-Regular': 'SpaceGrotesk-Regular.ttf'
            }

            for font_name, font_file in font_files.items():
                font_path = os.path.join(fonts_path, font_file)
                if os.path.exists(font_path):
                    font.Font(root=self.root, font=font_name, file=font_path)
                else:
                    print(f"Warning: Font file not found: {font_path}")

            # Обновляем шрифты в интерфейсе
            self.fonts = {
                'title': ('Inter-Black', 48),
                'subtitle': ('SpaceGrotesk-Bold', 42),
                'button': ('Inter-Regular', 16),
                'text': ('Inter-Regular', 14),
                'stats': ('SpaceGrotesk-Bold', 36),
                'label': ('Inter-Regular', 14),
                'logo': ('Inter-Black', 24)
            }
        except Exception as e:
            print(f"Error loading fonts: {str(e)}")
            # Fallback to system fonts
            self.fonts = {
                'title': ('Arial', 48, 'bold'),
                'subtitle': ('Arial', 42),
                'button': ('Arial', 16),
                'text': ('Arial', 14),
                'stats': ('Arial', 36, 'bold'),
                'label': ('Arial', 14),
                'logo': ('Arial', 24, 'bold')
            }

    def darken_color(self, color):
        """Затемнение цвета для эффекта при наведении"""
        rgb = [int(color[i:i+2], 16) for i in (1, 3, 5)]
        rgb = [max(0, c - 20) for c in rgb]
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

    def update_status(self, text, icon="⏳"):
        self.status_label.configure(text=text)
        self.root.update()

    def update_total_progress(self, total_files, converted_files):
        """Обновляет общий прогресс конвертации"""
        percent = int((converted_files / total_files) * 100)
        self.total_percent_label.configure(text=f"{percent}%")
        self.progress_bar.set(converted_files / total_files)
        self.root.update()

    def update_file_progress(self, filename, progress):
        """Обновляет прогресс текущего файла"""
        percent = int(progress * 100)
        
        # Ограничиваем длину имени файла
        if len(filename) > 40:
            filename = filename[:37] + "..."
        
        # Всегда показываем процент, даже при 100%
        progress_text = f"{filename:<40} {percent:>3}%\n"
        
        # Обновляем последнюю строку прогресса
        last_line = self.files_textbox.get("end-2c linestart", "end-1c")
        if filename in last_line:
            self.files_textbox.delete("end-2c linestart", "end-1c")
        self.files_textbox.insert(tk.END, progress_text, "progress")
        
        # Если файл завершен, добавляем галочку
        if progress >= 1.0:
            self.files_textbox.insert(tk.END, f"✓ {filename:<40}\n", "success")
        
        self.files_textbox.see(tk.END)
        self.root.update()

    def process_folder(self):
        def select_folder():
            folder_path = filedialog.askdirectory(title="Select PDF folder", parent=self.root)
            if folder_path:
                self.root.after(1, lambda: start_processing(folder_path))
            else:
                self.convert_button.configure(state="normal")

        def start_processing(folder_path):
            try:
                self.files_textbox.delete("1.0", tk.END)
                self.total_percent_label.configure(text="0%")
                self.progress_bar.set(0)
                
                txt_folder = os.path.join(folder_path, "TXT VERSION")
                os.makedirs(txt_folder, exist_ok=True)
                
                pdf_files = list(Path(folder_path).glob("*.pdf"))
                total_files = len(pdf_files)
                
                if total_files == 0:
                    self.update_status("No PDF files found")
                    self.convert_button.configure(state="normal")
                    return
                
                converted_files = 0
                
                def process_next_file(index=0):
                    nonlocal converted_files
                    
                    if index >= len(pdf_files):
                        self.files_textbox.insert(tk.END, "\n")
                        # Увеличиваем размер финального сообщения в 3 раза
                        completion_message = f"Completed! {converted_files} files converted\n"
                        self.files_textbox.configure(font=ctk.CTkFont(family=self.fonts['stats'][0], size=self.fonts['stats'][1] * 3))  # Увеличиваем в 3 раза
                        self.files_textbox.insert(tk.END, completion_message, "complete")
                        self.files_textbox.configure(font=ctk.CTkFont(family=self.fonts['text'][0], size=self.fonts['text'][1]))
                        self.files_textbox.see(tk.END)
                        self.update_status(f"Completed! {converted_files} files")
                        self.convert_button.configure(state="normal")
                        return
                    
                    pdf_path = pdf_files[index]
                    self.update_status(f"Converting: {pdf_path.name}")
                    txt_path = os.path.join(txt_folder, f"{pdf_path.stem}.txt")
                    
                    try:
                        with pdfplumber.open(pdf_path) as pdf:
                            total_pages = len(pdf.pages)
                            text = ""
                            for i, page in enumerate(pdf.pages):
                                text += page.extract_text() + "\n"
                                progress = (i + 1) / total_pages
                                self.update_file_progress(pdf_path.name, progress)
                        
                        with open(txt_path, 'w', encoding='utf-8') as txt_file:
                            txt_file.write(text)
                        
                        converted_files += 1
                        self.converted_count.configure(text=str(converted_files))
                        self.update_total_progress(total_files, converted_files)
                        
                        # Обновляем отображение завершенного файла
                        if progress >= 1.0:
                            pass  # Не добавляем дополнительную строку при завершении файла
                        
                    except Exception as e:
                        self.files_textbox.insert(tk.END, f"× {pdf_path.name} - Error: {str(e)}\n", "error")
                    
                    self.files_textbox.see(tk.END)
                    
                    # Планируем следующий файл
                    self.root.after(10, lambda: process_next_file(index + 1))
                
                # Запускаем обработку первого файла
                process_next_file(0)
                
            except Exception as e:
                self.update_status(f"Error: {str(e)}")
                self.convert_button.configure(state="normal")
                print(traceback.format_exc())

        # Отключаем кнопку
        self.convert_button.configure(state="disabled")
        
        # Запускаем выбор папки в следующем цикле событий
        self.root.after(1, select_folder)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PDFConverter()
    app.run() 