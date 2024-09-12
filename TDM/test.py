import subprocess

# Команда для запуска вашей программы
command = './program'  # Замените на путь к вашей программе

# Цикл от 0 до 30
for i in range(10000):  # Генерирует числа от 0 до 30 включительно
    try:
        # Запуск программы с передачей числа и получение результата
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Преобразуем число в строку и передаем в программу
        input_number = str(i)
        stdout, stderr = process.communicate(input=input_number)

        # Проверка ошибок и вывод только при их наличии
        if process.returncode != 0:
            print(f"Ошибка на вводе числа {i}: {stderr.strip()}")  # Вывод только ошибки
        
    except FileNotFoundError:
        print("Не удалось найти программу. Проверьте путь к исполняемому файлу.")
        break
    except Exception as e:
        print(f"Произошла непредвиденная ошибка на вводе числа {i}: {e}")
        break
