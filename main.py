import tkinter as tk
from tkinter import messagebox
import subprocess

def run_calculator():
    num1 = entry_num1.get()
    operation = entry_operation.get()
    num2 = entry_num2.get()

    try:
        result = subprocess.check_output(['go', 'run', 'calculator.go', num1, operation, num2], text=True)
        result_label.config(text=f"Результат: {result.strip()}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

# Создание основного окна
root = tk.Tk()
root.title("Простой калькулятор")

# Создание элементов интерфейса
label_num1 = tk.Label(root, text="Число 1:")
entry_num1 = tk.Entry(root)

label_operation = tk.Label(root, text="Операция:")
entry_operation = tk.Entry(root)

label_num2 = tk.Label(root, text="Число 2:")
entry_num2 = tk.Entry(root)

result_label = tk.Label(root, text="Результат:")

calculate_button = tk.Button(root, text="Вычислить", command=run_calculator)

# Размещение элементов интерфейса
label_num1.grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_num1.grid(row=0, column=1, padx=10, pady=5)

label_operation.grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_operation.grid(row=1, column=1, padx=10, pady=5)

label_num2.grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_num2.grid(row=2, column=1, padx=10, pady=5)

calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

result_label.grid(row=4, column=0, columnspan=2, pady=5)

# Запуск основного цикла событий
root.mainloop()