from selenium.webdriver.common.by import By

def get_valid_data():
    """Возвращает валидные данные для формы"""
    return "Test", "9999999999", "test@mail.com"

def get_field_locators():
    """Возвращает локаторы для полей формы"""
    return {
        "Имя": (By.XPATH, "//input[@placeholder='Имя*']"),
        "Телефон": (By.XPATH, "//input[@placeholder='Телефон*']"),
        "Почта": (By.XPATH, "//input[@placeholder='Почта*']")
    }

def get_submit_button_locator():
    """Возвращает локатор кнопки 'Отправить'"""
    return (By.XPATH, "//button[contains(text(), 'Отправить')]")

def get_success_widget_locator():
    """Возвращает локатор успешного сообщения"""
    return (By.XPATH, "//h4[@class='form__success-badge-title' and text()='Ваше обращение получено']")
