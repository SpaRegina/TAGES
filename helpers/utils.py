import os

def write_to_log(file_path, message):
    """Функция для записи сообщений в лог-файл"""
    logs_dir = os.path.dirname(file_path)
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    with open(file_path, "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")
