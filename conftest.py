import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

BASE_URL = "https://tages.ru"

@pytest.fixture(scope="module")
def driver():
    """Инициализация WebDriver"""
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get(BASE_URL)
    yield driver
    driver.quit()

