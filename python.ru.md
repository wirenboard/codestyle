Wiren Board Python Style Guide
==============================

За основу взят стиль, описанный в PEP8 (https://peps.python.org/pep-0008/).

Для форматирования кода используется `black` (https://github.com/psf/black).

Отличия от PEP8
---------------

 * Максимальная длина строки - 110 символов вместо 78. Это позволяет не сильно дробить строки при
   написании кода и в то же время просматривать изменения в две колонки в интерфейсе Github
   (проверил на мониторе с разрешением 1920x1080).
 * Используем двойные кавычки для строк (`"string"`), не используем одинарные (`'string'`).

Общее
-----

Описанные здесь правила взяты напрямую из PEP8 и перечислены здесь для удобства.

### Отступы

Отступы делаются пробелами, по 4 пробела на уровень.

### Именование

Короткий свод правил:

  * Имена классов пишем в `JavaCamelCase` с большой буквы. Аббревиатуры (например, `MQTT`, `HTTP`)
    пишутся большими буквами. Это же касается названий типов (например, для `namedtuple`).
  * Имена функций, методов, аргументов, переменных пишем в `snake_case`.
  * Имена полей и методов класса, задуманных как приватные, должны начинаться с нижнего подчёркивания (`_`).
  * Имена констант пишем в `SNAKE_CASE` заглавными буквами.

При написании кода на python3 может понадобиться создавать классы-интерфейсы (с `metaclass=abc.ABCMeta`).
Имена таких классов начинаем с заглавной буквы `I` (например, `IMyInterface`).

Пример:

```python3
from collections import namedtuple


MY_CONST = 42

MyNamedTuple = namedtuple("MyNamedTuple", "arg_1 arg_2")


class MyClass:
    """
    docstring for this class
    """

    CLASS_PI = 3.14159

    def __init__(self, my_arg):
        self._my_arg = my_arg  # Объявили приватное поле

    def print_my_arg(self):
        print(self._my_arg)
```

### Аннотации типов

При написании кода на python3 рекомендуется по возможности использовать аннотации типов
(https://docs.python.org/3.5/library/typing.html). При написании аннотаций стоит помнить, что на контроллерах
доступна версия Python 3.5, то есть, не все поддерживаемые аннотации типов из Python 3 будут доступны.

Аннотации позволяют использовать автодополнение в редакторах кода, а также позволяют лучше понимать
происходящее в коде при чтении.

Можно не увлекаться созданием сложных описаний типов (вроде `Iterable[Mapping[str, Union[int, str]]]`),
но простые случаи описывать стоит.


```python3
from collections import namedtuple


MyNamedTuple = namedtuple("MyNamedTuple", "arg_1 arg_2")


def format_tuple(tuple: MyNamedTuple, delimiter: str = ", ") -> str:
    return str(tuple.arg_1) + delimiter + str(tuple.arg_2)
```

### Длинные списки аргументов / элементов коллекций

Black форматирует длинные перечисления аргументов функций или элементов коллекций примерно так:

 * пока помещается в строку, положить в одну строку;
 * если не поместилось, перенести начало списка на следующую строку;
 * если и так не поместилось, писать каждый элемент списка на новой строке.

Это может породить неоднородности при форматировании там, где раньше было хорошо. Например:

```python3
# до форматирования

self.parser.add_argument('-m', '--model', dest='device_model', type=str,
                         help='Модель устройства', required=True, choices=some_long_function_name_call())

self.parser.add_argument('-r', '--hw-rev', dest='hw_rev', type=str,
                         help='Версия платы', required=False, default=None)

self.parser.add_argument('-p', '--batch', type=validate_batch,
                         help='Номер партии', required=True)

# после форматирования

self.parser.add_argument(
    "-m",
    "--model",
    dest="device_model",
    type=str,
    help="Модель устройства",
    required=True,
    choices=some_long_function_name_call(),
)

self.parser.add_argument(
    "-r", "--hw-rev", dest="hw_rev", type=str, help="Версия платы", required=False, default=None
)

self.parser.add_argument("-p", "--batch", type=validate_batch, help="Номер партии", required=True)

```

Для того чтобы бороться с такими ситуациями, рекомендуется добавлять после последнего аргумента запятую.
В таком случае black всегда будет разбивать аргументы по строкам:

```python3
# до форматирования

self.parser.add_argument('-m', '--model', dest='device_model', type=str,
                         help='Модель устройства', required=True, choices=some_long_function_name_call(),)

self.parser.add_argument('-r', '--hw-rev', dest='hw_rev', type=str,
                         help='Версия платы', required=False, default=None,)

self.parser.add_argument('-p', '--batch', type=validate_batch,
                         help='Номер партии', required=True,)

# после форматирования

self.parser.add_argument(
    "-m",
    "--model",
    dest="device_model",
    type=str,
    help="Модель устройства",
    required=True,
    choices=some_long_function_name_call(),
)

self.parser.add_argument(
    "-r",
    "--hw-rev",
    dest="hw_rev",
    type=str,
    help="Версия платы",
    required=False,
    default=None,
)

self.parser.add_argument(
    "-p",
    "--batch",
    type=validate_batch,
    help="Номер партии",
    required=True,
)
```

То же самое рекомендуется делать с объявлениями списков и словарей.

Приятным дополнением такого форматирования будет чуть более лаконичный diff при добавлении или перестановке
элементов в списке.

Проверка кода
-------------

Для автоматической проверки кода на CI используется `pylint`.

Для проверки форматирования (и непосредственно форматирования) используются `black` и `isort`.
`black` автоматически форматирует файл согласно своим внутренним правилам. `isort` группирует и
сортирует список подключаемых модулей.

Файлы с настройками находятся в репозитории codestyle в директории `python`.

Что именно происходит на CI - можно посмотреть [здесь](https://github.com/wirenboard/jenkins-pipeline-lib/blob/master/vars/wb.groovy) (поискав по ```runPythonChecks```; все скрипты берутся из codestyle).

> :warning: На момент подготовки версии 1.0 ошибки `pylint` не будут приводить к падению сборки по умолчанию (при снятой галочке "angry pylint").
> Это связано с множеством ложных срабатываний, в частности, на тестах с использованием `pytest`.
>
> Тем не менее, проверки будут проводиться и будут собираться их логи для анализа в будущем.


### Установка codestyle-тулзов (один раз для проекта)
На CI и в локальной системе разработчика тулзы должны быть одинаковыми, поэтому black, isort и pylint устанавливаем путём создания virtualenv внутри каждого проекта. Если нужно, тулзы и конфиги можно доустановить и в существуюший venv проекта.

> :information_source: Isort имеет очень своеобразную захардкоженную внутри логику поиска конфига и определения корня проекта, из-за чего и получались разногласия с запуском локально и на CI.
>
> Похоже, единственно рабочее решение - иметь pyproject.toml в корне проекта.

Если в проекте нет `pyproject.toml`, `requirements.txt` - выкачать их [отсюда](https://github.com/wirenboard/codestyle/tree/master/python) и положить в корень проекта.

> :warning: Только для Linux! (в Windows venv через vscode создаётся не в проекте, а системный)
Открыть в vscode проект -> ```Ctrl+Shift+P``` -> ```Python: Create Environment``` -> ```Venv```

```Ctrl + Shift + P``` -> ```Python: Create Terminal``` -> откроется терминал с уже активным venv; выполнить: ```pip3 install -r requirements.txt```

### Если без vscode
#### Linux (и Jenkins)
Выполнить в корне проекта
```console
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip3 install -r requirements.txt
$ deactivate
```
_Можно доустановить requirements.txt из codestyle и в свой venv._

#### Windows
* открыть в командной строке корневую директорию проекта (запустив от имени администратора!)
* выполнить
```console
$ py -m venv .venv
$ .\.venv\Scripts\activate
$ py -m pip install --upgrade pip
$ py -m pip install -r requirements.txt
$ deactivate
```
* настроить VSCode далее по инструкции; с конфигом для windows

### Запуск руками (в директории проекта; [pyproject.toml](https://raw.githubusercontent.com/wirenboard/codestyle/master/python/pyproject.toml) присутствует)

**Активировать venv** (пример по умолчанию; venv может быть и другим)
```console
$ source .venv/bin/activate
```

#### pylint
```console
$ python3 -m pylint $(find . -name '*.py')
```

#### black + isort (dry-run)
```console
$ python3 -m black --config pyproject.toml --check --diff $(find . -name '*.py')
$ python3 -m isort --settings-file pyproject.toml --check --diff $(find . -name '*.py')
```

#### black + isort (автоформатирование)
```console
$ python3 -m black --config pyproject.toml $(find . -name '*.py')
$ python3 -m isort --settings-file pyproject.toml $(find . -name '*.py')
```

> :information_source: При изменении форматирования в репозитории может сильно испортиться вывод `git blame`.
>
> Начиная с версии 2.23, `git` умеет игнорировать изменения из таких коммитов.
> Для этого при смене форматирования кода надо будет добавлять в репозиторий файл `.git-blame-ignore-revs`.
>
> Подробнее об этом можно почитать здесь: https://black.readthedocs.io/en/stable/guides/introducing_black_to_your_project.html

**по завершению - выйти из venv**
```console
$ deactivate
```

Автоформатирование в IDE
-------------

### VSCode

Один раз настраиваем VSCode:

 * устанавливаем расширение Python: `Ctrl-Shift-X` (открывает Marketplace), в строке поиска вводим `python`,
   устанавливаем первое расширение из списка (от Microsoft);
* аналогично устанавливаем расширения black, isort, pylint (все от Microsoft)
 * открываем редактор настроек VSCode: `Ctrl-Shift-P`, в поиске вводим `settings json`,
   выбираем `Preferences: Open Settings (JSON)`;
 * в открывшемся редакторе вводим (или добавляем опции в существующий объект);
 * если файлы настроек расположены не в `~/.config/wb/`, то заменяем `${env:HOME}/.config/wb/` на корректный путь:

#### Linux
```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python3",
    "python.terminal.activateEnvironment": true,
    "black-formatter.args": [
        "--config=${workspaceFolder}/pyproject.toml"
    ],
    "black-formatter.importStrategy": "fromEnvironment",
    "isort.check": true,
    "isort.args": [
        "--settings-path=${workspaceFolder}"
    ],
    "[python]": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit"
        }
    },
    "pylint.lintOnChange": true,
    "isort.importStrategy": "fromEnvironment",
    "pylint.importStrategy": "fromEnvironment",
    "pylint.severity": {
        "refactor": "Warning"
    },
}
```

#### Windows
```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}\\.venv\\Scripts\\python.exe",
    "python.terminal.activateEnvironment": true,
    "black-formatter.args": [
        "--config=${workspaceFolder}\\pyproject.toml"
    ],
    "black-formatter.importStrategy": "fromEnvironment",
    "isort.check": true,
    "isort.args": [
        "--settings-path=${workspaceFolder}"
    ],
    "[python]": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit"
        }
    },
    "pylint.lintOnChange": true,
    "isort.importStrategy": "fromEnvironment",
    "pylint.importStrategy": "fromEnvironment",
    "pylint.severity": {
        "refactor": "Warning"
    },
}
```

Code coverage
-------------

Для оценки покрытия тестов используется плагин pytest `coverage`. Оценка показывает процент выполнившихся строк кода и веток условий относительно общего объема файлов, использованных в процессе тестирования.

### Запуск

В зависимости от того, как вы запускаете тесты, нужно использовать разные сценарии.
**Минимально допустимое значение покрытия для прохождения тестов указывается в аргументе `--cov-fail-under`** 

#### Внутри devcontainer

1. Скачать из [codestyle-репозитория](https://github.com/wirenboard/codestyle/tree/master/python) файл `.coveragerc` и положить в корень проекта.
2. Запустить
```console
$ pytest --cov --cov-config=./.coveragerc --cov-report=term --cov-branch --cov-fail-under=<limit>
```

#### Внутри venv

1. Настроить venv [по инструкции для codestyle-проверок](#установка-codestyle-тулзов-один-раз-для-проекта). В venv должен установиться пакет pytest-cov.
2. Скачать из [codestyle-репозитория](https://github.com/wirenboard/codestyle/tree/master/python) файл `.coveragerc` и положить в корень проекта.
3. Запустить
```console
$ pytest --cov --cov-config=./.coveragerc --cov-report=term --cov-branch --cov-fail-under=<limit>
```

#### Сборка wbdev

Работает только для `wbdev ndeb` и `wbdev cdeb`
1. Скачать из [codestyle-репозитория](https://github.com/wirenboard/codestyle/tree/master/python) файл `.coveragerc` и положить в корень проекта.
2. Запустить
```console
$ export WBDEV_PYBUILD_TEST_ARGS="--cov --cov-config=../../../.coveragerc --cov-report=term --cov-branch --cov-fail-under=<limit>"
$ wbdev ndeb
```

### Отчеты

Для сборки внутри devcontainer и внутри venv есть возможность сгенерировать html отчет (для варианта wbdev сложные аргументы запуска, поэтому не приводим его). Для включения генерации нужно добавить опцию запуска
```console
--cov-report=html
```
В папке проекта создастся папка htmlcov. Чтобы посмотреть отчет, откройте файл index.html в браузере.

### Настройка VSCode

#### Для запуска тестов из VSCode:
1. Установите плагин для Python и настройте запуск тестов через pytest
2. Откройте настройки workspace: нажмите комбинацию `Ctrl-Shift-P`, в поиске введите `settings json`,
   выбираем `Preferences: Open Workspace Settings (JSON)`
3. К массиву опций запуска добавляем:
```
"--cov","--cov-config","./.coveragerc","--cov-report","term","--cov-branch","--cov-fail-under","<limit>"
```
Должны получиться примерно такие настройки:
```json
{
    "python.testing.pytestArgs": [
        "tests","--cov","--cov-config","./.coveragerc","--cov-report","term","--cov-branch","--cov-fail-under","<limit>"
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true
}
```

#### Для просмотра отчета в исходных файлах:
1. Установите плагин [Coverage Gutters](https://github.com/ryanluker/vscode-coverage-gutters)
2. К опциям запуска добавьте `"--cov-report","xml"`
3. Проведите тестирование
3. Откройте файл, покрытие которого хотите посмотреть. В статус-баре VSCode найдите надпись `Watch` и нажмите ее для включения подсветки.


Ещё гайдлайны
-------------

  * [Реализация сервисов на Python](guidelines/service-python.md)
  * [Шаблон setup.py](python/setup.py)

Changelog
---------

### v1.0 (2022/04/19)

 * Initial version
