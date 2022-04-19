Wiren Board Python Style Guide
==============================

За основу взят стиль, описанный в PEP8 (https://peps.python.org/pep-0008/).

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

Проверка кода
-------------

Для автоматической проверки кода на CI используется flake8 и pylint. Файлы с настройками находятся
в репозитории codestyle в директории `python`.

### Запуск pylint

Установка pylint в Debian:

```console
$ sudo apt install python3-pylint
```

На CI запуск `pylint` для проверки репозитория производится так:

```console
$ python3 -m pylint --rcfile "$PATH_TO_RCFILE" $(find . -name '*.py')
```

### Запуск flake8

Для проверки используется `flake8` и плагин `flake8-quotes`.

```console
$ sudo apt install python3-flake8 python3-flake8-quotes
```

На CI запуск производится так:

```console
$ python3 -m flake8 --append-config "$PATH_TO_FLAKE8_FILE" $(find . -name '*.py')
```

Changelog
---------

### v1.0 (2022/04/19)

 * Initial version
