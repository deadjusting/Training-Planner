import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

# Глобальный список для хранения тренировок
trainings = []

# Функция для добавления тренировки
def add_training():
    date = entry_date.get()
    workout_type = entry_workout_type.get()
    duration = entry_duration.get()
    
    # Валидация даты
    if not validate_date(date):
        messagebox.showerror("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД.")
        return
    
    # Валидация длительности
    if not duration.isdigit() or int(duration) <= 0:
        messagebox.showerror("Ошибка", "Длительность должна быть положительным числом.")
        return
    
    training = {
        "date": date,
        "workout_type": workout_type,
        "duration": int(duration)
    }
    trainings.append(training)
    save_to_file()
    # Очистка полей ввода
    entry_date.delete(0, tk.END)
    entry_workout_type.delete(0, tk.END)
    entry_duration.delete(0, tk.END)
    messagebox.showinfo("Успех", "Тренировка добавлена!")
    update_table()

# Обновление таблицы
def update_table():
    for row in tree.get_children():
        tree.delete(row)
    for training in trainings:
        tree.insert("", tk.END, values=(training['date'], training['workout_type'], training['duration']))

# Фильтрация по типу тренировки
def filter_by_type():
    workout_type = entry_filter_type.get()
    filtered = [t for t in trainings if t['workout_type'].lower() == workout_type.lower()]
    display_filtered(filtered)

# Фильтрация по дате
def filter_by_date():
    date = entry_filter_date.get()
    # Проверка правильности формата даты
    if not validate_date(date):
        messagebox.showerror("Ошибка", "Введите дату в формате ГГГГ-ММ-ДД.")
        return
    filtered = [t for t in trainings if t['date'] == date]
    display_filtered(filtered)

# Отображение отфильтрованных данных
def display_filtered(filtered):
    for row in tree.get_children():
        tree.delete(row)
    for training in filtered:
        tree.insert("", tk.END, values=(training['date'], training['workout_type'], training['duration']))

# Сохранение данных в файл
def save_to_file():
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(trainings, f, ensure_ascii=False, indent=4)

# Загрузка данных из файла
def load_from_file():
    global trainings
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            trainings = json.load(f)
        update_table()
    except FileNotFoundError:
        trainings = []

# Проверка правильности формата даты
def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Создание основного окна
window = tk.Tk()
window.title("Training Planner")

# Ввод даты
tk.Label(window, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5, sticky='e')
entry_date = tk.Entry(window)
entry_date.grid(row=0, column=1, padx=5, pady=5)

# Ввод типа тренировки
tk.Label(window, text="Тип тренировки:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
entry_workout_type = tk.Entry(window)
entry_workout_type.grid(row=1, column=1, padx=5, pady=5)

# Ввод длительности
tk.Label(window, text="Длительность (мин):").grid(row=2, column=0, padx=5, pady=5, sticky='e')
entry_duration = tk.Entry(window)
entry_duration.grid(row=2, column=1, padx=5, pady=5)

# Кнопка добавления
tk.Button(window, text="Добавить тренировку", command=add_training).grid(row=3, column=0, columnspan=2, pady=10)

# Фильтр по типу
tk.Label(window, text="Фильтр по типу:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
entry_filter_type = tk.Entry(window)
entry_filter_type.grid(row=4, column=1, padx=5, pady=5)
tk.Button(window, text="Фильтровать по типу", command=filter_by_type).grid(row=4, column=2, padx=5, pady=5)

# Фильтр по дате
tk.Label(window, text="Фильтр по дате (ГГГГ-ММ-ДД):").grid(row=5, column=0, padx=5, pady=5, sticky='e')
entry_filter_date = tk.Entry(window)
entry_filter_date.grid(row=5, column=1, padx=5, pady=5)
tk.Button(window, text="Фильтровать по дате", command=filter_by_date).grid(row=5, column=2, padx=5, pady=5)

# Таблица отображения
columns = ("date", "workout_type", "duration")
tree = ttk.Treeview(window, columns=columns, show='headings')
tree.heading("date", text="Дата")
tree.heading("workout_type", text="Тип тренировки")
tree.heading("duration", text="Длительность (мин)")
tree.grid(row=6, column=0, columnspan=3, padx=5, pady=10)

# Загрузка данных при запуске
load_from_file()

# Запуск интерфейса
window.mainloop()