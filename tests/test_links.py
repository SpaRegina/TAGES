import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers.utils import write_to_log

# Путь к отчету
LOG_FILE = "../logs/test_links_report.log"

def scroll_to_element(driver, element):
    """Метод для прокрутки страницы к элементу"""
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

def click_with_action_chains(driver, element):
    """Метод для клика с использованием ActionChains"""
    actions = ActionChains(driver)
    actions.move_to_element(element).click().perform()

def click_with_js(driver, element):
    """Метод для клика через JavaScript"""
    driver.execute_script("arguments[0].click();", element)

def test_links_clickable(driver):
    """Тест на проверку кликабельности ссылок"""
    write_to_log(LOG_FILE, "Запуск теста проверки кликабельности ссылок.")
    links = driver.find_elements(By.TAG_NAME, "a")
    total_links = len(links)
    write_to_log(LOG_FILE, f"Найдено ссылок на странице: {total_links}")

    # Список для отчета
    report = []

    for i in range(total_links):
        links = driver.find_elements(By.TAG_NAME, "a")
        if i >= len(links):
            break

        link = links[i]
        url = link.get_attribute("href")
        link_text = link.text.strip() if link.text else "Без текста"

        if url and not (url.startswith("tel:") or url.startswith("mailto:") or url.startswith("#")):
            try:
                scroll_to_element(driver, link)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(link))
                click_with_action_chains(driver, link)

                assert "404" not in driver.title, f"Page not found after clicking link: {url}"
                report.append({"link_text": link_text, "url": url, "status": "успешно"})
                driver.get(BASE_URL)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "a")))
            except Exception as e:
                try:
                    click_with_js(driver, link)
                    report.append({"link_text": link_text, "url": url, "status": "успешно (через JS)"})
                except Exception as js_error:
                    report.append({"link_text": link_text, "url": url, "status": f"ошибка: {e}"})

    # Записываем отчет в лог
    for entry in report:
        write_to_log(LOG_FILE, f"Ссылка: {entry['link_text']}, URL: {entry['url']}, Статус: {entry['status']}")

    # Итоговый результат
    successful = sum(1 for r in report if "успешно" in r["status"])
    failed = len(report) - successful
    write_to_log(LOG_FILE, f"Итог: успешно откликнулись {successful} из {len(report)}, ошибок: {failed}")
