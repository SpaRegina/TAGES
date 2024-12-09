import pytest
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers.utils import write_to_log
from helpers.contest import get_submit_button_locator, get_field_locators

# Путь к отчёту
REPORT_FILE = "../logs/test_contact_form_submission_report.log"

# Локаторы
FIELD_LOCATORS = get_field_locators()
SUBMIT_BUTTON_LOCATOR = get_submit_button_locator()

@pytest.mark.parametrize("name, phone, company, email, comment", [
    ("User", "9999999999", "Test Company", "test@mail.com", "Тестовый комментарий"),
    ("", "9999999999", "Test Company", "test@mail.com", "Тестовый комментарий"),  # Пустое имя
    ("User", "", "Test Company", "test@mail.com", "Тестовый комментарий"),  # Пустой телефон
    ("User", "9999999999", "Test Company", "", "Тестовый комментарий"),  # Пустая почта
    ("User", "9999999999", "", "test@mail.com", ""),  # Пустая компания и комментарий
])
def test_contact_form_submission(driver, name, phone, company, email, comment):
    """Тест на заполнение и отправку формы обратной связи."""
    driver.get("https://tages.ru/")  # URL страницы с формой

    wait = WebDriverWait(driver, 30)  # Увеличенное время ожидания
    required_fields_status = "Не отправлено"

    try:
        # Проверка обязательных полей
        if not name or not phone or not email:
            write_to_log(
                REPORT_FILE,
                f"Дата и время: {datetime.now()}\n"
                f"Статус: {required_fields_status}\n"
                f"Имя: {name}\n"
                f"Телефон: {phone}\n"
                f"Компания: {company}\n"
                f"Почта: {email}\n"
                f"Комментарий: {comment}\n"
                + "-" * 50
            )
            return

        # Заполнение всех полей
        wait.until(EC.presence_of_element_located(FIELD_LOCATORS["Имя"])).send_keys(name)
        driver.find_element(*FIELD_LOCATORS["Телефон"]).send_keys(phone)
        driver.find_element(*FIELD_LOCATORS["Почта"]).send_keys(email)
        if "Компания" in FIELD_LOCATORS:
            driver.find_element(*FIELD_LOCATORS["Компания"]).send_keys(company)
        if "Комментарий" in FIELD_LOCATORS:
            driver.find_element(*FIELD_LOCATORS["Комментарий"]).send_keys(comment)

        # Клик по кнопке "Отправить"
        submit_button = wait.until(EC.element_to_be_clickable(SUBMIT_BUTTON_LOCATOR))
        submit_button.click()

        # Логируем успешную отправку
        write_to_log(
            REPORT_FILE,
            f"Дата и время: {datetime.now()}\n"
            f"Статус: Отправлено\n"
            f"Имя: {name}\n"
            f"Телефон: {phone}\n"
            f"Компания: {company}\n"
            f"Почта: {email}\n"
            f"Комментарий: {comment}\n"
            + "-" * 50
        )

    except Exception as e:
        # Логируем ошибку
        write_to_log(
            REPORT_FILE,
            f"Дата и время: {datetime.now()}\n"
            f"Статус: Ошибка при отправке\n"
            f"Имя: {name}\n"
            f"Телефон: {phone}\n"
            f"Компания: {company}\n"
            f"Почта: {email}\n"
            f"Комментарий: {comment}\n"
            f"Ошибка: {e}\n"
            + "-" * 50
        )
        raise e
