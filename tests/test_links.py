import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException
from helpers.utils import write_to_log
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Путь к отчету
REPORT_FILE = "../logs/test_links_report.log"

def test_links_clickable(driver):
    """Тест проверки кликабельности всех ссылок"""
    write_to_log(REPORT_FILE, "Запуск теста проверки кликабельности ссылок.")
    links = driver.find_elements(By.TAG_NAME, "a")

    # Собираем все ссылки
    all_links = [
        (link.get_attribute("href"), link.text.strip() or "Без текста")
        for link in links if link.get_attribute("href")
    ]

    # Проверяем, что ссылки найдены
    assert all_links, "Не найдено ссылок для проверки"

    success_count = 0
    fail_count = 0

    # Проверяем каждую ссылку
    for href, text in all_links:
        write_to_log(REPORT_FILE, f"Проверяется ссылка: {text} ({href})")
        try:
            if href.startswith("tel:") or href.startswith("mailto:"):
                # Проверка специальных ссылок
                write_to_log(REPORT_FILE, f"Проверяется специальная ссылка: {href}")
                element = driver.find_element(By.XPATH, f"//a[@href='{href}']")
                driver.execute_script("arguments[0].click();", element)
                write_to_log(REPORT_FILE, f"Специальная ссылка успешно обработана: {href}")
                success_count += 1
            elif href.startswith("#"):
                # Проверка якорных ссылок
                write_to_log(REPORT_FILE, f"Проверяется якорная ссылка: {href}")
                element = driver.find_element(By.XPATH, f"//a[@href='{href}']")
                element.click()
                write_to_log(REPORT_FILE, f"Якорная ссылка успешно обработана: {href}")
                success_count += 1
            else:
                # Проверка обычных ссылок
                driver.get(href)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                assert "404" not in driver.title, f"Ошибка 404 при открытии {href}"
                write_to_log(REPORT_FILE, f"Ссылка успешно открыта: {href}")
                success_count += 1
        except (WebDriverException, TimeoutException):
            write_to_log(REPORT_FILE, f"Ссылка не обработана: {text} ({href})")
            fail_count += 1
        except AssertionError as e:
            write_to_log(REPORT_FILE, f"Ошибка проверки: {str(e)}")
            fail_count += 1

    # Итоговый отчет
    write_to_log(REPORT_FILE, f"Проверено ссылок: {len(all_links)}, Успешно: {success_count}, Не успешно: {fail_count}")
    print(f"Проверено ссылок: {len(all_links)}, Успешно: {success_count}, Не успешно: {fail_count}")
