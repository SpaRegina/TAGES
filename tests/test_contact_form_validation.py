import pytest
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers.utils import write_to_log
from helpers.contest import get_valid_data, get_field_locators, get_submit_button_locator, get_success_widget_locator

# Путь к отчёту
REPORT_FILE = "../logs/test_contact_form_validation_report.log"

# Данные для теста
VALID_NAME, VALID_PHONE, VALID_EMAIL = get_valid_data()

# Локаторы
FIELD_LOCATORS = get_field_locators()
SUBMIT_BUTTON_LOCATOR = get_submit_button_locator()
SUCCESS_WIDGET_LOCATOR = get_success_widget_locator()

# Тестовые данные
TEST_DATA = [
    # Тесты для поля "Имя"
    ("Имя", ""),  # Пустое значение
    ("Имя", "     "),  # Только пробелы
    ("Имя", "И"),  # Короткое имя
    ("Имя", "Иван123"),  # Имя с цифрами
    ("Имя", "123"),  # Имя только из цифр
    ("Имя", "@Иван!"),  # Имя с символами
    ("Имя", "Иван"),  # Валидное имя

    # Тесты для поля "Телефон"
    ("Телефон", ""),  # Пустое значение
    ("Телефон", "     "),  # Только пробелы
    ("Телефон", "12345"),  # Короткий номер
    ("Телефон", "12345abc"),  # Номер с буквами
    ("Телефон", "12345@#!"),  # Номер с символами
    ("Телефон", "+7 (123) 456-78-90"),  # Валидный номер (форматированный)
    ("Телефон", "71234567890"),  # Валидный номер (без форматирования)

    # Тесты для поля "Почта"
    ("Почта", ""),  # Пустое значение
    ("Почта", "     "),  # Только пробелы
    ("Почта", "testmail"),  # Почта без @
    ("Почта", "test@"),  # Почта без домена
    ("Почта", "test@@mail.ru"),  # Почта с двойным @
    ("Почта", "test @mail.ru"),  # Почта с пробелами
    ("Почта", "test@mail.ru"),  # Валидный адрес
    ("Почта", "test@sub.mail.ru"),  # Валидный адрес с поддоменом
]

@pytest.mark.parametrize("field_name, input_value", TEST_DATA)
def test_field_validation(driver, field_name, input_value):
    """Проверка полей формы обратной связи"""
    driver.get("https://tages.ru/")

    # Заполнение всех полей валидными значениями
    driver.find_element(*FIELD_LOCATORS["Имя"]).send_keys(VALID_NAME)
    driver.find_element(*FIELD_LOCATORS["Телефон"]).send_keys(VALID_PHONE)
    driver.find_element(*FIELD_LOCATORS["Почта"]).send_keys(VALID_EMAIL)

    # Проверка конкретного поля
    field = driver.find_element(*FIELD_LOCATORS[field_name])
    field.clear()
    field.send_keys(input_value)

    # Нажать кнопку "Отправить"
    driver.find_element(*SUBMIT_BUTTON_LOCATOR).click()

    # Проверка результата
    try:
        if not input_value.strip():
            raise ValueError("Невалидное значение")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(SUCCESS_WIDGET_LOCATOR))
        status = "ТЕСТ УСПЕШЕН"
    except Exception:
        status = "ТЕСТ НЕУСПЕШЕН"

    # Форматировать значение для отчёта
    input_value_display = "Пустое поле" if not input_value.strip() else input_value
    if input_value.isspace():
        input_value_display = "Ввод только пробелов"

    # Логирование результата
    write_to_log(
        REPORT_FILE,
        f"Дата и время: {datetime.now()}\n"
        f"Поле: {field_name}\n"
        f"Значение: {input_value_display}\n"
        f"Статус: {status}\n"
        + "-" * 50
    )
