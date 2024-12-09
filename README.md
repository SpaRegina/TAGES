# Selenium Testing Project for Tages

Проект создан для автоматизации тестирования главной страницы сайта [Tages](https://tages.ru/) в рамках тестового задания. Основная цель — проверить функциональность ссылок, разделов, форм и обратной связи, а также выявить возможные ошибки валидации.

## Функционал

Проект выполняет следующие проверки:

1. **Кликабельность всех ссылок и разделов:**  
   Проверка, что каждая ссылка работает корректно, отсутствуют ошибки загрузки (`404`), корректная работа навигации.

2. **Проверка вызовов email и tel:**  
   Проверка, что ссылки с протоколами `mailto:` и `tel:` работают без ошибок.

3. **Валидация формы обратной связи:**  
   Проверка невозможности отправки формы с некорректными данными и отображения ошибок валидации.

4. **Отправка тестового запроса:**  
   Проверка успешной отправки корректных данных через форму обратной связи.

## Установка

1. Клонируйте репозиторий:
    ```bash
    git clone <URL_репозитория>
    cd <папка_проекта>
    ```
2. Убедитесь, что у вас установлен Python версии 3.8 или выше.
3. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

## Использование

### Запуск тестов

Для запуска тестов выполните команду:
```bash
pytest test_links.py
pytest test_email_tel.py
pytest test_contact_form_validation.py
pytest test_contact_form_submission.py
```

## Что проверяет каждый файл:
test_links.py — проверяет кликабельность всех ссылок на странице.
test_email_tel.py — тестирует корректность работы ссылок с протоколами mailto и tel.
test_contact_form_validation.py — выполняет тесты валидации формы обратной связи, используя различные входные данные.
test_contact_form_submission.py — проверяет возможность успешной отправки формы с различными наборами данных.

## Логи
### Результаты тестов записываются в лог-файлы в папке logs/:

test_links_report.log
test_email_tel_report.log
test_contact_form_validation_report.log
test_contact_form_submission_report.log


## Требования
Установленный браузер Google Chrome последней версии.
Установленный драйвер ChromeDriver (автоматически управляется webdriver-manager).

## Структура проекта
.
├── helpers/
│   ├── utils.py
│   └── contest.py
├── logs/
│   ├── test_links_report.log
│   ├── test_email_tel_report.log
│   ├── test_contact_form_validation_report.log
│   └── test_contact_form_submission_report.log
├── test_links.py
├── test_email_tel.py
├── test_contact_form_validation.py
├── test_contact_form_submission.py
├── requirements.txt
└── README.md


