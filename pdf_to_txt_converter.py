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
            'surface': "#F4F4F4",
            'highlight': "#E8FFE9"
        }
        
        self.root.configure(fg_color=self.colors['background'])
        
        # Главный контейнер
        main_frame = ctk.CTkFrame(
            self.root,
            fg_color=self.colors['background'],
            corner_radius=30
        )
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Верхняя навигация с логотипом
        nav_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        nav_frame.pack(fill="x", padx=20, pady=(0, 30))
        
        # Загружаем логотип
        try:
            logo_path = get_resource_path(os.path.join('src', 'logo', 'logo_rgb_black.png'))
            if os.path.exists(logo_path):
                # Загружаем PNG
                pil_image = Image.open(logo_path)
                logo_size = (96, 96)
                pil_image = pil_image.resize(logo_size, Image.Resampling.LANCZOS)
                logo_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=logo_size)
                
                logo_label = ctk.CTkLabel(
                    nav_frame,
                    image=logo_image,
                    text=""
                )
                logo_label.pack(side="left", padx=(0, 20))
            else:
                raise FileNotFoundError(f"Logo file not found at {logo_path}")
        except Exception as e:
            print(f"Error loading logo: {str(e)}")
            # Если не удалось загрузить логотип, используем текстовую метку
            logo_label = ctk.CTkLabel(
                nav_frame,
                text="TBTBO",
                font=ctk.CTkFont(family=self.fonts['logo'][0], size=self.fonts['logo'][1] * 4),
                text_color=self.colors['text_primary']
            )
            logo_label.pack(side="left", padx=(0, 20))
        
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
        
        # Кнопка конвертации
        self.convert_button = ctk.CTkButton(
            content_frame,
            text="Select PDF Folder",
            command=self.process_folder,
            font=ctk.CTkFont(family=self.fonts['button'][0], size=self.fonts['button'][1]),
            fg_color=self.colors['accent'],
            hover_color=self.colors['text_secondary'],
            height=45,
            width=180,
            corner_radius=22
        )
        self.convert_button.pack(anchor="w", pady=(0, 20))
        
        # Прогресс
        progress_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        progress_frame.pack(fill="x")
        
        self.status_label = ctk.CTkLabel(
            progress_frame,
            text="Ready to convert",
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

    def process_folder(self):
        try:
            self.convert_button.configure(state="disabled")
            self.files_textbox.delete("1.0", "end")
            self.progress_bar.set(0)
            
            folder_path = filedialog.askdirectory(title="Select PDF folder")
            if not folder_path:
                self.convert_button.configure(state="normal")
                return
            
            txt_folder = os.path.join(folder_path, "TXT VERSION")
            os.makedirs(txt_folder, exist_ok=True)
            
            pdf_files = list(Path(folder_path).glob("*.pdf"))
            total_files = len(pdf_files)
            
            if total_files == 0:
                self.update_status("No PDF files found", "❌")
                self.convert_button.configure(state="normal")
                return
            
            converted_files = 0
            
            for pdf_path in pdf_files:
                self.update_status(f"Converting: {pdf_path.name}", "⚡")
                
                txt_path = os.path.join(txt_folder, f"{pdf_path.stem}.txt")
                
                try:
                    with pdfplumber.open(pdf_path) as pdf:
                        text = ""
                        for page in pdf.pages:
                            text += page.extract_text() + "\n"
                        
                    with open(txt_path, 'w', encoding='utf-8') as txt_file:
                        txt_file.write(text)
                    
                    converted_files += 1
                    self.converted_count.configure(text=str(converted_files))
                    self.files_textbox.insert("end", f"✓ {pdf_path.name}\n")
                except Exception as e:
                    self.files_textbox.insert("end", f"✗ {pdf_path.name} - Error: {str(e)}\n")
                
                self.files_textbox.see("end")
                self.progress_bar.set(converted_files / total_files)
            
            self.update_status(
                f"Completed! Converted {converted_files} of {total_files} files",
                "✨"
            )
            self.convert_button.configure(state="normal")
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}", "❌")
            self.convert_button.configure(state="normal")
            print(traceback.format_exc())

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PDFConverter()
    app.run() 