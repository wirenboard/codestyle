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

Инструменты проверки устанавливаются в virtualenv рабочего проекта. Поэтому, если в вашем проекте он уже есть, вы можете не создавать его и использовать существующий.

### Установка инструментов (один раз для проекта)

Необходимо настроить virtualenv в соответствии с инструкцией для VSCode - клонировать репозиторий и выполнить скрипт.

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

Необходимо настроить virtualenv в соответствии с инструкцией для VSCode - клонировать репозиторий и выполнить скрипт.

### Запуск

В зависимости от того, как вы запускаете тесты, нужно использовать разные сценарии.
**Минимально допустимое значение покрытия для прохождения тестов указывается в аргументе `--cov-fail-under`** 

1. Внутри [venv](#установка-инструментов-один-раз-для-проекта)

    ```console
    $ pytest --cov --cov-config=.coveragerc --cov-report=term --cov-fail-under=<limit>
    ```

2. Сборка wbdev

    Работает только для `wbdev ndeb` и `wbdev cdeb`
    ```console
    $ export WBDEV_PYBUILD_TEST_ARGS="--cov --cov-config=../../../.coveragerc --cov-report=term --cov-fail-under=<limit>"
    $ wbdev ndeb
    ```

### Отчеты

Для сборки внутри devcontainer и внутри venv есть возможность сгенерировать html отчет (для варианта wbdev сложные аргументы запуска, поэтому не приводим его). Для включения генерации нужно добавить опцию запуска
```console
--cov-report=html
```
В папке проекта создастся папка htmlcov. Чтобы посмотреть отчет, откройте файл index.html в браузере.
