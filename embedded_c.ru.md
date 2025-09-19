Wiren Board Embedded C Style Guide
========================

Этот документ описывает рекомендации по написанию легко читаемого и хорошо организованного кода на языке C для embedded-разработки.

## Автоформатирование

### clang-format
Для автоформатирования кода используется clang-format с конфигурацией, представленной в файле `.clang-format-embedded-c`.

Для того, чтобы использовать автоформатирование в редакторе VSCode, необходимо установить расширение [C/C++](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools) от Microsoft и указать в settings.json путь к файлу конфигурации:
```json
"C_Cpp.formatting": "clangFormat",
"C_Cpp.clang_format_style": "file:<path-to-.clang-format-embedded-c>",
```
После этого можно:
- форматировать файл комбинацией клавиш Ctrl+Shift+I
- форматировать только выделенный фрагмент с помощью Ctrl+K, Ctrl+F
- форматировать только измененные строки с помощью команды `Format Modified Lines` (можно назначить горячую клавишу)

Для запуска автоформатирования из командной строки можно использовать команду:
```bash
clang-format -style=file:<path-to-.clang-format-embedded-c> -i src/main.c
```

NOTE: расширение C/C++ от Microsoft уже содержит clang-format, поэтому его не нужно устанавливать отдельно. Если вы хотите использовать свою версию clang-format, то можно указать путь к ней в настройках `C_Cpp.clang_format_path`. Обратите внимание на версию clang-format: она может быть разной в зависимости от того, используете ли вы clang-format из расширения или свою версию.

### clang-tidy
Для статического анализа кода используется clang-tidy с конфигурацией, представленной в файле `.clang-tidy-embedded-c`.

Для анализа кода в редакторе VSCode, необходимо установить расширение [C/C++](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools) от Microsoft и указать в settings.json путь к файлу конфигурации:

```json
"C_Cpp.codeAnalysis.clangTidy.enabled": true,
"C_Cpp.codeAnalysis.runAutomatically": true,
"C_Cpp.codeAnalysis.exclude": {
    "**/unittests/**": true,
},
"C_Cpp.codeAnalysis.clangTidy.args": [
    "--config-file=<path-to-.clang-tidy-embedded-c>",
],
```

После этого clang-tidy будет автоматически запускаться при открытии или сохранении файла, а найденные проблемы будут отображаться в панели "Problems".

Для корректной работы clang-tidy из состава расширения C/C++ необходимо, чтобы в проекте присутствовал файл `.vscode/c_cpp_properties.json`, в котором указаны пути к заголовочным файлам и другие параметры компиляции. Стандарт языка должен быть `gnu11`.

<details>
<summary>Пример c_cpp_properties.json для одного таргета</summary>
```json
{
    "name": "SIG_ups_v3",
    "includePath": [
        "include",
        "libwbmcu-system/cmsis",
        "libwbmcu-system/include",
        "libwbmcu-periph",
        "libwbmcu-i2c-eeprom",
        "libwbmcu-modbus",
        "libwbmcu-system/common",
        "libwbmcu-system/flashfs",
        "libfixmath/libfixmath",
        "libwbmcu-system/Unity/src",
        "libwbmcu-system/utest_helpers"
    ],
    "defines": [
        "MODEL_SIG_ups_v3",
        "MODBUS_DEVICE_FW_VERSION_NUMBERS=1,1,0,-2",
        "MODBUS_DEVICE_FW_VERSION_STRING='1','.','1','.','0','-','r','c','2'",
        "MODBUS_DEVICE_FW_VERSION=16842753",
        "GD32E230X",
        "HSE_VALUE=8000000",
        "MODBUS_DEVICE_GIT_INFO=\"bce42f1_feature_parallel-ups\"",
        "MODULE_NAME=startup"
    ],
    "compilerPath": "/usr/bin/arm-none-eabi-gcc",
    "compilerArgs": [
        "-mcpu=cortex-m23",
        "-mthumb"
    ],
    "cStandard": "gnu11",
    "cppStandard": "c++17",
    "intelliSenseMode": "linux-gcc-arm"
}
```
</details>

Также можно запускать clang-tidy из командной строки. Для этого необходимо сгенерировать файл compile_commands.json с помощью команды `bear`:
```bash
bear -- make MODEL_<model_name>
```
И запустить clang-tidy:
```bash
clang-tidy -p . -config-file=<path-to-.clang-tidy-embedded-c> src/main.c
```

### Отладочные сообщения расширения C/C++ в VSCode
Чтобы видеть, что делает clang-tidy и clang-format при запуске из VSCode, можно включить отладочные сообщения расширения C/C++ в VSCode. Для этого нужно в settings.json добавить:
```json
"C_Cpp.loggingLevel": "Debug",
"C_Cpp.debugShortcut": true,
```
После этого на панели "Output" появится новый пункт "C/C++", в котором будут отображаться отладочные сообщения.

## Именование
### Общее
В embedded C не используется стиль CamelCase, вместо него применяется snake_case. В именах функций и переменных допускаются **только строчные буквы**, слова разделяются символом подчеркивания (`_`).

### Файлы и модули
1. При добавлении нового модуля размещайте его в отдельной библиотеке.
2. Избегайте файлов с именами типа *peripherals.h*.
3. Имя файла должно отражать суть модуля. Используйте *mcp230xx.h* вместо *gpio_chip.h*.
4. Разделяйте функциональность модулей для повышения повторного использования кода. Базовые функции для работы с чипом — в одном файле, задачи — в другом. Например, *mcp230xx.h* содержит драйвер, а *wbio-dio.h* использует его функции.

### Функции
В C нет пространств имен и классов, поэтому рекомендуется добавлять префикс библиотеки к каждой функции, даже если она static и используется только внутри библиотеки:
```C
int pin_value = mcp230xx_read_gpio();
ads1015_set_config(ADS_CONFIG_1);
```
То же касается *define*:
```C
#define MCP23008_IODIR                  0x00
#define MCP23008_IPOL                   0x01
#define MCP23008_GPINTEN                0x02
#define MCP23008_DEFVAL                 0x03
#define MCP23008_INTCON                 0x04
```

При этом для static переменных допускается использовать короткие имена без префикса.

### Имена вариантов enum
Нужно выбирать осмысленное имя типа enum, и все варианты должны начинаться с префикса данного имени.

Хорошее именование: по вариантам понятно, о каком enum идет речь:
```C
enum w1_transaction {
    W1_TRANSACTION_SEND,
    W1_TRANSACTION_RECEIVE
}
```

Плохое именование: невозможно понять, к какому enum принадлежит вариант, пока не посмотрим определение:
```C
enum w1_transaction {
    W1_PROTOCOL_SEND,
    W1_PROTOCOL_RECEIVE
}
```

Плохое именование: слишком длинные имена, можно выбрать более короткий вариант без потери смысла:
```C
enum w1_protocol_transaction {
    W1_PROTOCOL_TRANSACTION_SEND,
    W1_PROTOCOL_TRANSACTION_RECEIVE
}
```

## Объявления
1. Функции, не предназначенные для вызова вне библиотеки, должны быть объявлены как *static*.
2. Прототипы static-функций размещаются в *.c* файле.
3. *#define*, используемые только в *.c*, также должны быть там.
4. В заголовочном файле размещаются только интерфейс для работы с модулем: прототипы публичных функций, дефайны и типы данных.
5. Не используйте "магические" константы. Вместо этого используйте *define*:
```C
#define MCP230xx_REG_IOCON_BANK (1 << 2)
...
uint16_t gpio_config = mcp230xx_read_config();
if (gpio_config & MCP230xx_REG_IOCON_BANK) {
...
```
6. Также в заголовочном файле могут помещаться `static inline` функции, если они, например, используются как заглушки или обёртки для других функций.

7. При переопределении или определении новых типов данных в конце названий добавляется `_t`, при этом сама структура не именуется:
```C
typedef struct {
    uint16_t address;
    uint16_t data;
} hold_reg_t;
```

8. Имена структур не должны иметь в названии `_t`:
```C
struct hold_reg {
    uint16_t address;
    uint16_t data;
};
```

## Макросы C
Использование препроцессора C не рекомендуется, так как это усложняет чтение и поддержку кода. По возможности используйте средства языка C.

Типовые случаи применения макросов:
* Определение констант (`#define`), например, размеров массивов, параметров конфигурации, адресов регистров.
* Включение/отключение частей прошивки через `#if` и подобные директивы (желательно на уровне модуля).
* Компиляторные приёмы, невозможные иначе (например, `assert`). Старайтесь ограничивать такими случаями только низкоуровневые библиотеки.

Если в макросе используются выражения, оборачивайте их в `do {} while (0)`. Макросы, имитирующие функции, должны вести себя как функции. Например, `START_TIMER();` вместо `START_TIMER;`. Все макросы именуются ЗАГЛАВНЫМИ буквами.

Возможные альтернативы:
* `if` с условием, вычисляемым на этапе компиляции, вместо `#if`;
* `const`-переменные вместо `#define`;
* `static inline`-функции вместо макросов с выражениями.

## Кодировка
Все файлы должны быть в кодировке UTF-8.

## Конец файла
Файл всегда заканчивается переводом строки.

## Максимальная длина строки
Максимальная длина строки в исходном коде — 120 символов. Рекомендуется не превышать этот предел для удобства чтения и совместимости с большинством редакторов и средств просмотра кода.

## Выравнивание
Пробелы

1. Для отступов используйте 4 пробела на каждый уровень вложенности. Символ табуляции (TAB) использовать запрещено.
2. Знаки бинарных операций отделяются от переменных пробелами, а знаки унарных операций — нет.
```C
a += b / c;
c++;
c &= ~d;
```
3. Пробелы между ключевыми словами (`if`, `while`, `do`, `for`) и открывающей скобкой выражения.
4. Аргументы функций перечисляются без пробелов вокруг скобок. Когда аргументов несколько, запятая ставится сразу после аргумента, после запятой — пробел:
```C
task_schedule(adc_start_periodic_conversion_task_id, ADC_FILTRATION_PERIOD_MS);
```
5. Значения макросов, которые именуют константы, должны быть расположены от 40 до 60-го знакоместа, кратно 4 символам.
Это нужно для того, чтобы оставить место для макросов с длинными именами, которые могут быть потенциально добавлены позже в процессе разработки.

Отступы и пробелы можно проверять, например, используя команду `git diff`. С помощью команды `git diff master` проверяется, что не изменено форматирование уже написанного ранее кода относительно мастер-ветки.

Не используйте отступы для выравнивания многострочных выражений одного уровня вложенности.

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

Пример расстановки пробелов при объявлении массива:
```C
static const uint8_t array_example[] = { 0xAA, 0xBB, 0xCC, 0xDD, 0xEE };
```

## Комментарии
Комментарии пишутся после строки (короткие) или до строки (длинные):
```C
код         // короткий комментарий
```
или
```C
// длинный комментарий
код
```
```//``` выравнивается по позиции, кратной 4 символам (в редакторе vscode клавишей TAB в режиме 4 пробела вместо табуляции).
Текст от знака ```//``` отделяется пробелом.

## Расстановка скобок
Даже если тело условного блока состоит из одной строки, оно заключается в фигурные скобки.

Перенос скобки на следующую строку начала определения осуществляется в функциях и многострочных условиях (`if`, `else if`), в остальных случаях — нет.
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
Скобки ставятся всегда, даже когда тело блока — одна строка, и даже когда его нет:
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
