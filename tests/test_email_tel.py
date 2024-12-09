import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from helpers.utils import write_to_log

# Путь к отчету
REPORT_FILE = "../logs/test_email_tel_report.log"

def test_email_and_tel_links(driver):
    """Тест проверки email и tel ссылок"""
    write_to_log(REPORT_FILE, "Запуск теста проверки email и tel ссылок.")
    links = driver.find_elements(By.TAG_NAME, "a")

    # Фильтруем ссылки с "mailto:" и "tel:"
    email_links = [link.get_attribute("href") for link in links if link.get_attribute("href") and link.get_attribute("href").startswith("mailto:")]
    tel_links = [link.get_attribute("href") for link in links if link.get_attribute("href") and link.get_attribute("href").startswith("tel:")]

    # Проверяем, что ссылки присутствуют
    assert email_links, "Не найдено ссылок с 'mailto:'"
    assert tel_links, "Не найдено ссылок с 'tel:'"

    email_success_count = 0
    tel_success_count = 0
    total_emails = len(email_links)
    total_tels = len(tel_links)

    # Проверяем email ссылки
    write_to_log(REPORT_FILE, "Проверяем email ссылки:")
    for email in email_links:
        write_to_log(REPORT_FILE, f"Проверяется: {email}")
        try:
            email_element = driver.find_element(By.XPATH, f"//a[@href='{email}']")
            email_element.click()
            email_success_count += 1
        except WebDriverException:
            write_to_log(REPORT_FILE, f"Не удалось кликнуть по ссылке: {email}")
            continue

    # Проверяем телефонные ссылки
    write_to_log(REPORT_FILE, "Проверяем телефонные ссылки:")
    for tel in tel_links:
        write_to_log(REPORT_FILE, f"Проверяется: {tel}")
        try:
            tel_element = driver.find_element(By.XPATH, f"//a[@href='{tel}']")
            tel_element.click()
            tel_success_count += 1
        except WebDriverException:
            try:
                driver.execute_script("arguments[0].click();", tel_element)
                tel_success_count += 1
            except WebDriverException:
                write_to_log(REPORT_FILE, f"Не удалось кликнуть по ссылке: {tel}")
                continue

    write_to_log(REPORT_FILE, f"Проверено email ссылок: {total_emails}, Успешно: {email_success_count}")
    write_to_log(REPORT_FILE, f"Проверено телефонных ссылок: {total_tels}, Успешно: {tel_success_count}")
