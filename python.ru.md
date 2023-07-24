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

### Запуск pylint

> :warning: На момент подготовки версии 1.0 ошибки `pylint` не будут приводить к падению сборки по умолчанию.
> Это связано с множеством ложных срабатываний, в частности, на тестах с использованием `pytest`.
>
> Тем не менее, проверки будут проводиться и будут собираться их логи для анализа в будущем.

Установка pylint в Debian:

```console
$ sudo apt install python3-pylint
```

На CI запуск `pylint` для проверки репозитория производится так:

```console
$ python3 -m pylint --rcfile "$PATH_TO_CODESTYLE/python/pylintrc" $(find . -name '*.py')
```

### Запуск black + isort

Установка в Debian:

```console
$ sudo apt install black python3-isort
```

На CI запуск производится так:

```console
$ python3 -m black --config "$PATH_TO_CODESTYLE/python/pyproject.toml" --check --diff $(find . -name '*.py')
$ python3 -m isort --settings-file "$PATH_TO_CODESTYLE/python/pyproject.toml" --check --diff $(find . -name '*.py')
```

Для автоматического форматирования кода в репозитории:

```console
$ python3 -m black --config "$PATH_TO_CODESTYLE/python/pyproject.toml" $(find . -name '*.py')
$ python3 -m isort --settings-file "$PATH_TO_CODESTYLE/python/pyproject.toml" $(find . -name '*.py')
```

> :information_source: При изменении форматирования в репозитории может сильно испортиться вывод `git blame`.
>
> Начиная с версии 2.23, `git` умеет игнорировать изменения из таких коммитов.
> Для этого при смене форматирования кода надо будет добавлять в репозиторий файл `.git-blame-ignore-revs`.
>
> Подробнее об этом можно почитать здесь: https://black.readthedocs.io/en/stable/guides/introducing_black_to_your_project.html

Настройка IDE
-------------

### VSCode

Устанавливаем пакеты `black` и `python3-isort`, в Debian/Ubuntu так:

```console
$ sudo apt install black python3-isort
```

Для корректной работы `black` в Ubuntu 20.04 надо поставить `python3-click` версии 8.

Если необходимо использовать одни и те же настройки во всех проектах, нужно скопировать файлы `python/pyproject.toml` и `python/pylintrc` в директорию `~/.config/wb/` (не забыть создать её сначала).

Далее настраиваем VSCode:

 * устанавливаем расширение Python: `Ctrl-Shift-X` (открывает Marketplace), в строке поиска вводим `python`,
   устанавливаем первое расширение из списка (от Microsoft);
 * открываем редактор настроек VSCode: `Ctrl-Shift-P`, в поиске вводим `settings json`,
   выбираем `Preferences: Open Settings (JSON)`;
 * в открывшемся редакторе вводим (или добавляем опции в существующий объект);
 * если файлы настроек расположены не в `~/.config/wb/`, то заменяем `${env:HOME}/.config/wb/` на корректный путь:

```json
{
    "editor.formatOnSave": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": [
        "--config=${env:HOME}/.config/wb/pyproject.toml"
    ],
    "python.sortImports.args": [
        "--settings-file=${env:HOME}/.config/wb/pyproject.toml"
    ],
    "[python]": {
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    },
    "python.linting.pylintEnabled": true,
    "python.linting.pylintArgs": [
        "--rcfile",
        "${env:HOME}/.config/wb/pylintrc"
    ]
}
```

Ещё гайдлайны
-------------

  * [Реализация сервисов на Python](guidelines/service-python.md)
  * [Шаблон setup.py](python/setup.py)

Changelog
---------

### v1.0 (2022/04/19)

 * Initial version
