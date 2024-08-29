=========================
Адаптер для yandex.allure
=========================

``edutesting.formatters.allure_formatter`` - модуль содержить адаптер генератор
xml отчетов для yandex.allure. По результатам выполения feature-файлов с тестами
будут сгенерированы отчеты с данными о выполениие тестовдля дальнейшей
генерации allure отчетов

Использование:
==============

При запуске тестов указать класс ``AllureFormatter`` как форматер:
  ::
    behave feature/ --format=edutesting.formatters.allure_formatter:AllureFormatter
