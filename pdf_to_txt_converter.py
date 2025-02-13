import tkinter as tk
from tkinter import filedialog, messagebox
import os
from pathlib import Path
import pdfplumber
import traceback

class PDFConverter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF в TXT конвертер")
        
        # Настройка размера окна и центрирование
        window_width = 500
        window_height = 250
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Создание и размещение кнопки
        self.convert_button = tk.Button(
            self.root,
            text="Выбрать папку с PDF",
            command=self.process_folder,
            height=2,
            width=30,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 12)
        )
        self.convert_button.pack(pady=30)
        
        # Метка для статуса
        self.status_label = tk.Label(
            self.root, 
            text="Ожидание выбора папки...", 
            wraplength=450,
            font=('Arial', 10)
        )
        self.status_label.pack(pady=10)
        
        # Прогресс бар
        self.progress_label = tk.Label(
            self.root,
            text="",
            font=('Arial', 10)
        )
        self.progress_label.pack(pady=5)
    
    def convert_pdf_to_txt(self, pdf_path, txt_path):
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
                
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(text)
            return True
        except Exception as e:
            error_msg = f"Ошибка при конвертации {pdf_path}:\n{str(e)}"
            print(error_msg)
            print(traceback.format_exc())
            messagebox.showerror("Ошибка", error_msg)
            return False
    
    def process_folder(self):
        try:
            # Выбор директории
            folder_path = filedialog.askdirectory(title="Выберите папку с PDF файлами")
            if not folder_path:
                return
            
            # Создание папки для txt файлов
            txt_folder = os.path.join(folder_path, "TXT VERSION")
            os.makedirs(txt_folder, exist_ok=True)
            
            # Подсчет файлов и конвертация
            pdf_files = list(Path(folder_path).glob("*.pdf"))
            total_files = len(pdf_files)
            
            if total_files == 0:
                messagebox.showinfo("Информация", "PDF файлы не найдены в выбранной папке")
                return
                
            converted_files = 0
            
            for pdf_path in pdf_files:
                txt_path = os.path.join(txt_folder, f"{pdf_path.stem}.txt")
                if self.convert_pdf_to_txt(pdf_path, txt_path):
                    converted_files += 1
                
                # Обновление статуса
                progress = (converted_files / total_files) * 100
                self.status_label.config(
                    text=f"Обработка: {pdf_path.name}"
                )
                self.progress_label.config(
                    text=f"Прогресс: {converted_files}/{total_files} ({progress:.1f}%)"
                )
                self.root.update()
            
            final_message = f"Готово!\nКонвертировано {converted_files} из {total_files} файлов.\nРезультаты в папке 'TXT VERSION'"
            self.status_label.config(text=final_message)
            self.progress_label.config(text="")
            messagebox.showinfo("Завершено", final_message)
            
        except Exception as e:
            error_msg = f"Неожиданная ошибка:\n{str(e)}"
            print(error_msg)
            print(traceback.format_exc())
            messagebox.showerror("Ошибка", error_msg)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PDFConverter()
    app.run() 