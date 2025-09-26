[Wiren Board Python Style Guide](#python)
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
$ pytest --cov --cov-config=.coveragerc --cov-report=term --cov-branch --cov-fail-under=<limit>
```

#### Внутри venv

1. Настроить venv [по инструкции для codestyle-проверок](#установка-codestyle-тулзов-один-раз-для-проекта). В venv должен установиться пакет pytest-cov.
2. Скачать из [codestyle-репозитория](https://github.com/wirenboard/codestyle/tree/master/python) файл `.coveragerc` и положить в корень проекта.
3. Запустить
```console
$ pytest --cov --cov-config=.coveragerc --cov-report=term --cov-branch --cov-fail-under=<limit>
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

1. Скачайте из [codestyle-репозитория](https://github.com/wirenboard/codestyle/tree/master/python) файл `.coveragerc` и положите в корень проекта.
2. Установите плагин для Python и настройте запуск тестов через pytest
3. Откройте настройки workspace: нажмите комбинацию `Ctrl-Shift-P`, в поиске введите `settings json`,
   выбираем `Preferences: Open Workspace Settings (JSON)`
4. К массиву опций запуска добавляем:
```
"--cov","--cov-config",".coveragerc","--cov-report","term","--cov-branch","--cov-fail-under","<limit>"
```
Должны получиться примерно такие настройки:
```json
{
    "python.testing.pytestArgs": [
        "tests","--cov","--cov-config",".coveragerc","--cov-report","term","--cov-branch","--cov-fail-under","<limit>"
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



[Wiren Board Embedded C Style Guide](#embedded-c)
========================

The following sheet describes few recomodations in order to make an easy to read
and well organised program code focusing on C programming language convenstions what can be
different from C++ conventions.

## Marking and Parenthesis
These are similar those what we have got used in C++. Read more in: https://github.com/contactless/codestyle. 

## Naming
In embedded C we don't follow CamelCase style however we use snake_case. At snake_case style function and variable names can
include **only lower case characters**, like *snake_case* (even though officially upper case characters are also allowed) and words must be separated by underscore character (_). 

## Library naming
1. When you add a new module to your project you should put it in a new library. 
2. Please avoid libraries like: *peripherals.h*.
3. Library names should describe the module behind the code. Use *mcp230xx.h* isntead of *gpio_chip.h*
4. Try to separate module funtionalities, in order to support your code reusability. Better to implement basic IC
  related functions in one library, and write task specific functions in an other library. Like: *mcp230xx.h* includes
  driver to chip and *wbio-dio.h" library is using functions of *mcp230xx.h".
  
## Function names
Since in C is no option to use namespace or classes, somehow you should mark your function's library and avoid this kind of
program code in *main.c*:
```C
int pin_value = read_value_digit();//function for module1
set_config(CONFIG_1);              //function for module2
```
Better to mark library name as a prefix for each function even if it is a static function and used only in the given
library:
```C
int pin_value = mcp230xx_read_gpio();
ads1015_set_config(ADS_CONFIG_1);
```
It is also true for *defines* where you should mark where is it defined:
```C
#define MCP23008_IODIR                  0x00
#define MCP23008_IPOL                   0x01
#define MCP23008_GPINTEN                0x02
#define MCP23008_DEFVAL                 0x03
#define MCP23008_INTCON                 0x04
```

## Declarations
1. Functions what is not supposed be called from outside of library should be defined as *static*.
2. Static function prototypes should be in *.c* file, because it is related to implementation not to usage.
3. *#defines* used only in *.c* also should be placed in *.c* file.
4. In header file should be *defines* and functions what are necessary to use library.
5. Avoid using hardcoded constants because first, they are not describing their functionality, second harder to modify all
if once it must be. Avoid this:
```C
uint16_t gpio_config = mcp230xx_read_config();
if (gpio_config & 0x04) {
...
```
Better to use *define* and replace magic constant.
```C
#define MCP230xx_REG_IOCON_BANK (1 << 2)
...
uint16_t gpio_config = mcp230xx_read_config();
if (gpio_config & MCP230xx_REG_IOCON_BANK) {
...
```

## C Macros

Using of C preproccessor is generally discouraged because it makes source code hard to read and mantain.

Whenever possible, please use C language features instead.

Common use cases for C macros include:

* `#define`-ing constants, for instance, array sizes, configuration parameters, register addresses or so on. 
* switching on and off particular chunks of firmware via `#if` and friends. Prefereable done at module level.
* compile-time magic otherwise impossible to implement. Say, altering of control flow in coroutines or implementing assert. Try to limit it to few low-level libraries.

If expressions are used in macro, they must be wrapped in `do {} while (0)`. 
Function-like macros should follow function-like calling semantics. Consider `START_TIMER();` instead of `START_TIMER;`.

All macros must be named in `CAPITAL` letters.

Please consider the following alternatives to C preprocessor:
* `if`s with condition evaluating to `true` at compile time insted of `#if`s
* `const` variables instead of `#define`s
* `static inline` functions instead of macros containing expressions.

## Code Tips

### Clearing Interrupt Flags

It is important to NOT use RMW (read-modify-write) operation when clearing interrupt flag in the status register of peripherals. If status register was modified by peripheral during 'modify' operation, the new interrupt flag will be cleared together with the specified flag. As a result, new interrupt will be lost.

Worst exapmle:

```
if (TIM1-SR & TIM_SR_CC1IF) {
    TIM1-SR &= ~TIM_SR_CC1IF;
}
if (TIM1-SR & TIM_SR_CC2IF) {
    TIM1-SR &= ~TIM_SR_CC2IF;
}
```

If CC1 and CC2 events are near in time, one of them may be lost.

Good example:

```
if (TIM1-SR & TIM_SR_CC1IF) {
    TIM1-SR = ~TIM_SR_CC1IF;        // rc_w0
}
if (TIM1-SR & TIM_SR_CC2IF) {
    TIM1-SR = ~TIM_SR_CC2IF;        // rc_w0
}
```

This works because the bits in SR register are rc_w0 type and writing '1' does nothing.

## Кодировка
Все файлы должны быть созданы в кодировке UTF-8.

## Конец строки
Конец файла всегда заканчивается переводом строки.

## Выравнивание
Пробелы

1. Отступы 4 пробела между блоками - не использовать символ табуляции (TAB).
2. Знаки бинарных операций отделяются от переменных пробелами, а знаки унарных операций - нет.
```C
a += b / c;
c++;
c &= ~d;
```
3. Пробелы между ``` if while do for``` и открывающей скобкой выражения.
4. Аргументы функций перечисляются без пробелов вокруг скобок. Когда аргументов несколько - запятая сразу после аргумента, после запятой - пробел:
```C
task_schedule(adc_start_periodic_conversion_task_id, ADC_FILTRATION_PERIOD_MS);
```
5. Значения макросов, которые именуют константы, должны быть расположены от 40 до 60 знакоместа кратно 4 символам.
Это нужно для того чтобы оставить место для макросов с длинными именами, которые могут быть потенциально добавлены позже в процессе разработки.

Отступы и пробелы можно проверять, например, используя команду git diff. С помощью команды git diff master проверяется то что не изменено форматирование уже написанного ранее кода относительно мастер-ветки.

Не использовать отступы для выравнивания

Примеры плохого кода:
```C
static uint16_t task_next_free_id[TASK_TYPE_NUMBER] = {GET_TASK_ID(TASK_IMMEDIATE, 0),
                                                       GET_TASK_ID(TASK_BACKGROUND, 0)};
```

```C
    hlw8012_channels_state[channel].energy_factor = fix16_to_int(fix16_mul(fix16_div(fix16_from_int(hlw8012_channel_defs[channel].energy_unit_time),hlw8012_channels_state[channel].value_factor),F16(HLW8012_PULSE_COUNTING_FACTOR)));
```

```C
    hlw8012_channels_state[channel].energy_factor = fix16_to_int(fix16_mul(fix16_div(fix16_from_int(hlw8012_channel_defs[channel].energy_unit_time),
                                 hlw8012_channels_state[channel].value_factor),F16(HLW8012_PULSE_COUNTING_FACTOR)));
```

Примеры хорошего кода:

```C
static uint16_t task_next_free_id[TASK_TYPE_NUMBER] = {
    GET_TASK_ID(TASK_IMMEDIATE, 0),
    GET_TASK_ID(TASK_BACKGROUND, 0)
};
```

```C
    hlw8012_channels_state[channel].energy_factor = fix16_to_int(
        fix16_mul(
            fix16_div(
                fix16_from_int(
                    hlw8012_channel_defs[channel].energy_unit_time
                ),
                hlw8012_channels_state[channel].value_factor
            ),
            F16(HLW8012_PULSE_COUNTING_FACTOR)
        )
    );
```

Пример расстановки пробелов при обьявлении массива:
```C
static const uint8_t array_example[] = { 0xAA, 0xBB, 0xCC, 0xDD, 0xEE };
```

## Комментарии
Комментарии после строки (короткий) или до строки (длинный):
```C
код         // короткий комментарий
```
или
```C
// длинный комментарий
код
```
```//``` выравнивается кратно 4-м знакоместам (в редакторе vscode клавишей TAB в режиме 4 пробела вместо табуляции).
Текст  от знака ```//``` отделяется пробелом.

## Расстановка скобок
Даже если тело условного блока состоит из одной строки, оно заключается в фигурные скобки.

Перенос скобки на следующую строку начала определения осуществляется в функциях и многострочных условиях (if, else if), в остальном нет.
Расстановка скобок:
```C
void function(void)
{
    if (a == b) {
    // single str action use brackets
    }

    if (c == d) {
    // do if equal
    } else {
    // do if not equal
    }

    if ((a == b) ||
        (c == d))
    {
        // multi str condition use statement body open bracket with newline
    } else if ((a != b) &&
               (c != e))
    {
        // multi str condition use statement body open bracket with newline
    } else if (c == e) {
        // single str condition use statement body open bracket with one line
    }
}

void function(void)
{
    return;
}

```
Скобки ставятся всегда, даже когда тело блока 1 строчка и даже когда его нет:
```C
while () {};

if () {
    return 0;
} else {
    return 1;
}
```

Операции всегда выделяются скобками, даже если порядок действий очевиден:
```C
(a || b && !c) -> (a || (b && (!c)))
```

## Объявления
В заголовочном (.h) файле должен быть только интерфейс к модулю т.е. обьявления функций, структур и макросы которые вызываются и используются в других модулях. Также в заголовочном файле могут помещаться ```static inline``` функции, если они например используются как заглушки.

При переопределении или определении новых типов данных в конце названий добавляется ```_t```.
Пример:

```C
typedef struct {
    uint16_t address;
    uint16_t data;
} hold_reg_t;
```

имена структур не должны иметь в названии ```_t```.

```C
struct hold_reg {
    uint16_t address;
    uint16_t data;
};
```

## Ветвления

Запрещается использование тренарных операций, так как они усложняют понимание кода. ```int a = (cond) ? var1 : var 2```

Если условие содержит логическое И, рекомендуется сделать 2 вложенных if. Такой подход нагляднее демонстрирует условия выполнения, а также заставляет задуматься о порядке проверки условий, и упрощении кода.

```
if (cond1) {
    if (cond2) {
        ...
    }
}
```

## Однотипные сущности

Часто бывает что устройство имеет несколько входов/выходов/шин/светодиодов/кнопок итд, абсолютно всегда все что потенциально может быть больше чем в одном экземпляре должно обрабатываться через индексы и циклы.

## Исправление ошибок в master

Ранее допущенные ошибки форматирования исправляются в отдельной ветке с PR согласно кодстайлу.

## Неинициализированные переменные

Неинициализированных переменных быть не должно. Любая переменная, структура, указатель или массив должны быть инициализированы при объявлении. Даже если где то позже переменная будет принимать значение, например при чтении настроек из файловой системы. Нули уменьшат спектр чудес при ошибке или гарантированно будут вызывать hard fault, ускоряя отладку.

## Логические выражения

Запрещается использовать логические операции где либо кроме операторов условия.

`return (enabled_ch_mask & (1 << channel)) != 0;`

или

`x = (enabled_ch_mask & (1 << channel)) != 0;`

Проверка логического условия в выражении присваивания усложняет понимание. Вместо этого предлагается написать обычный читаемый if.

```
if (enabled_ch_mask & (1 << channel)) {
    return 1;
}
return 0;
```

или

```
x = 0;
if (enabled_ch_mask & (1 << channel)) {
    x = 1;
}
```

## Выбор типа переменной

Типы с явной разрядностью (uint8_t, uint16_t, uint32_t) нужно использовать только в случаях, где это важно для работы (протоколы, структуры данных) или необходимо для читаемости.
* данные
* регистры переферии
* результаты вычисления CRC и подобное
* статически выделенные переменные, для экономии ОЗУ

В остальных случаях использовать unsigned для беззнакового или int для знакового типа, а именно:
* счетчик цикла for
* индексы
* аргументы функций - индекс, длина, все что не данные
* все что на стеке и не критично к размеру, флаги, промежуточные вычисления

Это связано с тем что компилятор вставляет дополнительные инструкции UXTH UXTB SXTH SXTB для приведения типов (зануления старших разрядов). Чтобы uint8 преобразовать к машинному слову 32 бита, нужно отбросить старшие разряды с мусором). Это увеличивает размер кода и время его выполнения. Посмотрите дизасемблером любопытства ради. Используем их осмысленно только при необходимости.

## Порядок полей в структурах

Нужно помнить что компилятор выравнивает поля в структурах по размеру слова архитектуры - 32 бита. Для экономии памяти нужно думать как структура будет хранится в памяти.

Поля расположены плохо, размер структуры 12 байт:
```C
struct hold_reg {
    uint8_t data;
    uint32_t address;
    uint8_t crc;
};
```

Поля расположены хорошо, размер структуры с теми же самыми данными 8 байт:
```C
struct hold_reg {
    uint32_t address;
    uint8_t data;
    uint8_t crc;
};
```

# Имена вариантов enum

Нужно выбирать осмысленное имя типа enum, и все варианты должны начинаться с префикса данного имени

Хорошее именование, по вариантам понятно о каком enum идет речь:
```C
enum w1_transaction {
    W1_TRANSACTION_SEND,
    W1_TRANSACTION_RECEIVE
}
```

Плохое именование, невозможно понять какому enum принадлежит вариант пока не посмотрим определение:
```C
enum w1_transaction {
    W1_PROTOCOL_SEND,
    W1_PROTOCOL_RECEIVE
}
```

Плохое именование, слишком длинные имена, наверное можно подумать и выбрать более короткий вариант без потери смысла:
```C
enum w1_protocol_transaction {
    W1_PROTOCOL_TRANSACTION_SEND,
    W1_PROTOCOL_TRANSACTION_RECEIVE
}
```




[Wiren Board C++ Style Guide](#cplusplus)
========================

За основу взят яндексовский Style Guide для C++.

## Разметка

Для отступов используются только пробелы. Один уровень отступа - это 4 пробела.

Знаки арифметических операций выделяются пробелами:

```C++
int sum = a + b;
```

Запятые выделяются пробелами с одной стороны:

```C++
int sum = GetSum(a, b);
```


## Скобочки

В определениях функций и методов открывающая определение фигурная скобка переносится на следующую строчку. 

```C++
int foo()
{
   std::cout << "foo" << std:endl;
   return 0;
}
```

Используется компактный стиль расстановки фигурных скобок внутри определений функций и методов.

```C++
if (foo && bar) {
   std::cout << "foobar" << std:endl;
}
```

В случае многострочных условий if и циклов фигурная скобка переносится на отдельную строку.

```C++
if (foo &&
    bar)
{
   std::cout << "foobar" << std:endl;
}
```

Блоки кода в циклах и условных выражениях, состоящие из одной строки, заключаются в фигурные скобки при переносе на другую строчку:

```C++
if (foo) return 0;
```

```C++
if (foo) {
    std::cout << "foo" << std:endl;
}
```

Пустое тело в циклах должно быть заключено в фигурные скобки

```C++
while (ReadNoise()) {}
```




## Именование
### Общее
Основным способом создания имён всего является **JavaCamelCase**.
*snake_case* допускается в названиях локальных переменных, при этом они не должны использоваться в одном файле с CamelCase локальными переменными.



Функции и методы называются словосочетанием, описывающим то, что делаем функция, и начинаются с глагола: **const std::string& GetMethodName()**.

Цель к которой нужно стремиться: по названию должно быть понятно, что делает функция, класс или что хранит в себе переменная без необходимости смотреть реализацию.
Стоит избегать названий функций и методов типа *DoWork()*, переменных типа *counter* и т.д, кроме случаев, когда это не мешает пониманию.

Допускаются общепринятые короткие названия для переменных типа *i,j* для счётчиков в циклах.

В аббревиатурах остаётся первая заглавная буква: *TMqttClient*.


### Классы

Классы именуются с заглавной *T*, например *TModbusClient*.

Базовые классы должны иметь название, заканчивающееся на *Base*: *TModbusClientBase*.

Названия классов-интерфейсов начинаются с *I*: *class IException*

### Методы

Методы называются в CamelCase с большой буквы: *GetMethodName*.

### Поля классов
Поля данных (переменные) классов называются с большой буквы:

```C++
class TModbusClient
{
public:

std::string GetMethodName() { return MethodName; };

private:

std::string MethodName;
}
```

### Локальные переменные

Называются с маленькой буквы в camelCase. Допускается наименование с маленькой буквы в snake_case.

## Макросы

Препроцессор C использовать не стоит. Вместо него предпочтительно использовать конструкции C++.

В очень редких случаях использование макросов действительно даёт большой выигрыш в читаемости кода. 
Если вы столкнулись именно с таким случаем, то пользоваться препроцессором можно. Но стоит быть готовыми отстаивать свою правоту на review.

## Примеры

https://github.com/contactless/wb-homa-drivers/tree/master/wb-mqtt-serialo



[Wiren Board JavaScript Style Guide](#js)
==============================

За основу взят стиль [Airbnb](https://airbnb.io/javascript/).

Для форматирования кода используется [Prettier](https://prettier.io/).

Для проверки кода используется [ESLint](https://eslint.org/).


Установка `ESLint` и `Prettier`
-------------

```console
$ npm install --save-dev eslint eslint-config-airbnb eslint-plugin-import eslint-plugin-jsx-a11y eslint-plugin-prettier eslint-plugin-react eslint-plugin-react-hooks @babel/eslint-parser @babel/preset-react
```

Файлы с настройками находятся в репозитории в директории `js`.
Их надо скопировать в каталог проекта под именами
```
.eslintrc
.prettierrc
```

Для wb-rules правил используйте `js/eslintrc-es5`, так как правила пишутся на ECMAScript 5.

В раздел `scripts` файла `package.json` можно добавить строку

```js
    "lint": "eslint \"**/*.{js,jsx}\""
```

### Запуск eslint

```console
$ npx eslint FILE.js
```

### Запуск prettier

```console
$ npx prettier
```


Настройка IDE
-------------

### VSCode

 * устанавливаем расширение ESlint: `Ctrl-Shift-X` (открывает Marketplace), в строке поиска вводим `eslint`,
   устанавливаем первое расширение из списка (от Microsoft);
 * устанавливаем расширение Prettier: `Ctrl-Shift-X` (открывает Marketplace), в строке поиска вводим `prettier`;
 * открываем редактор настроек VSCode: `Ctrl-Shift-P`, в поиске вводим `settings json`,
   выбираем `Preferences: Open Settings (JSON)`;
 * в открывшемся редакторе вводим (или добавляем опции в существующий объект);
```json
{
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  "[javascriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  }
}
```

 * если файлы настройки `prettier` расположены не в каталоге проекта, то надо указать параметр `prettier.configPath`;
 * если файлы настройки `eslint` расположены не в каталоге проекта, то надо добавить параметр:
 
```json
{
  "eslint.options": { 
    "overrideConfigFile": "PATH/.eslintrc"
  }
}
``` 



[Wiren Board GO style guide](#go)
==========================

Форматировать код стандартными тулзами `go fmt`.

## Статический анализ

Установка [staticcheck](https://staticcheck.dev/):
```sh
apt install go-staticcheck
```

Запуск:
```sh
go mod vendor
staticcheck -go 1.13 ./...
```