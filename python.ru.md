# Wiren Board Python Style Guide

За основу взят стиль, описанный в [PEP8](https://peps.python.org/pep-0008/). 

Отличия от PEP8 и общие правила оформления:
 * Максимальная длина строки - 110 символов вместо 78.
 * Используем двойные кавычки для строк (`"string"`), не используем одинарные (`'string'`).
 * Добавляем аннотации типов.
 * В случае длинных перечислений элементов коллекций или аргументов, после последнего аргумента добавляется запятая (для однородного автоформатирования).

Ниже приведены инструкции по настройке автоформатирования и code coverage из консоли. Для настройки интеграции с VSCode воспользуйтесь [инструкцией](https://docs.google.com/document/d/19gT4BH6MO-XXyqqzTOoz-jhY0ITbeGKDOZ8FbV_J1tc).


## Автоматическая проверка кода

Для автоформатирования кода используется [black](https://github.com/psf/black) и [isort](https://github.com/PyCQA/isort). 

Для статической проверки кода используется [pylint](https://github.com/pylint-dev/pylint).

Что именно происходит на CI - можно посмотреть [здесь](https://github.com/wirenboard/jenkins-pipeline-lib/blob/master/vars/wb.groovy) (поискав по ```runPythonChecks```; все скрипты берутся из codestyle). 

### Установка инструментов (один раз для проекта)

В зависимости от вашего проекта, необходимо настроить virtualenv или devenv по [инструкции для VSCode](https://docs.google.com/document/d/19gT4BH6MO-XXyqqzTOoz-jhY0ITbeGKDOZ8FbV_J1tc).

### Запуск

1. Pylint
    ```console
    $ python3 -m pylint $(../codestyle/python/ci/find-python-files)
    ```

2. Black + isort (dry-run)
    ```console
    $ python3 -m black --config pyproject.toml --check --diff $(../codestyle/python/ci/find-python-files)
    $ python3 -m isort --settings-file pyproject.toml --check --diff $(../codestyle/python/ci/find-python-files)
    ```

3. Black + isort (автоформатирование)
    ```console
    $ python3 -m black --config pyproject.toml $(../codestyle/python/ci/find-python-files)
    $ python3 -m isort --settings-file pyproject.toml $(../codestyle/python/ci/find-python-files)
    ```


## Оценка качества тестирования (code coverage)

Для оценки покрытия кода тестами используется плагин pytest [coverage](https://github.com/pytest-dev/pytest-cov). 
Оценка показывает процент выполнившихся строк кода относительно общего объема файлов, использованных в процессе тестирования.

### Установка инструментов

Для запуска тестов необходимо настроить devenv по [инструкции для VSCode](https://docs.google.com/document/d/19gT4BH6MO-XXyqqzTOoz-jhY0ITbeGKDOZ8FbV_J1tc).

### Запуск

В зависимости от того, как вы запускаете тесты, нужно использовать разные сценарии.
**Минимально допустимое значение покрытия для прохождения тестов указывается в аргументе `--cov-fail-under`** 

1. Внутри devenv

    ```console
    $ pytest --cov --cov-config=.coveragerc --cov-report=term --cov-fail-under=<ЛИМИТ>
    ```

2. Сборка wbdev (без настройки devenv)

    Работает только для `wbdev ndeb` и `wbdev cdeb`
    ```console
    $ export WBDEV_PYBUILD_TEST_ARGS="--cov --cov-config=../../../.coveragerc --cov-report=term --cov-fail-under=<ЛИМИТ>"
    $ wbdev ndeb
    ```

### Отчеты

Для сборки внутри devenv есть возможность сгенерировать html отчет (для варианта wbdev сложные аргументы запуска, поэтому не приводим его). Для включения генерации нужно добавить опцию запуска
```console
--cov-report=html
```
В папке проекта создастся папка htmlcov. Чтобы посмотреть отчет, откройте файл index.html в браузере.
