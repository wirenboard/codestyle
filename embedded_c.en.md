Wiren Board Embedded C Style Guide
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

Плохой пример:
```C
    #define INPUT_1     { GPIOA, 10 }
    #define INPUT_2     { GPIOA, 11 }

    ...

    gpio_init(INPUT_1);
    gpio_init(INPUT_2);
```

В таком виде трудно вносить изменения, легко допустить ошибку, поправить одно и забыть другое.

Лушче написать так:
```C
    #define INPUTS_NUMBER 2
    #define INPUTS       { { GPIOA, 10 }, { GPIOA, 11 } }

    ...

    for (int i = 0; i < INPUTS_NUMBER; i++) {
        gpio_init(INPUTS[i]);
    }
```

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
# switch case
Старайтесь не использовать switch case. Если вы делаете несколько конструкций switch case по одной и той же переменной то это признак того что вам нужно использовать полиморфизм. Объедините в структуру все сущности, зависящие от этой переменной. Создайте массив таких структур и используйте переменную в качестве индекса для доступа к текущей структуре.

Например вместо:
```C
void input_handler(unsigned input) {
    switch (input) {
        case SIGNAL_IRQ:
            signal_irq_handler();
            break;
        case SIGNAL_ERROR:
            signal_error_handler();
            break;
        case SIGNAL_READY:
            signal_ready_handler();
            break;
        default:
            break;
    }
}
```

Лучше использовать:
```C

void input_handler(unsigned input) {
    static const void (*handlers[])(void) = {
        [SIGNAL_IRQ] = signal_irq_handler,
        [SIGNAL_ERROR] = signal_error_handler,
        [SIGNAL_READY] = signal_ready_handler,
    };
    handlers[input]();
}
```

Такой код компактнее, быстрее выполняется. Также он обеспечивает консистентность, так как по этим же индексам у нас наверняка будет описан список портов GPIO на который подключены эти сигналы, итд.

# Не плодите макросы конфигурации
Часто макросами в коде выбирается какая переферия используется в данном варианте, вариантов обычно не много, а переферии наоборот много. Вместо того чтобы прописывать макрос на каждый регистр или значение используйте структуры.

Вместо такого:
```C
    #define MODBUS_HW_USART                 USART1
    #define MODBUS_HW_USART_IRQn            USART1_IRQn
    #define MODBUS_HW_DMA_TX_CH             DMA1_Channel2
```

Лучше написать так:
```C
    struct modbus_hw {
        USART_TypeDef *usart;
        IRQn_Type irqn;
        DMA_Channel_TypeDef *dma_tx_ch;
    };

    #define MODBUS_USART_HW                 { \
            .usart = USART1, \
            .irqn = USART1_IRQn, \
            .dma_tx_ch = DMA1_Channel2 \
        }

```

# Переиспользование
Нужно использовать код повторно. Не нужно писать код если он уже написан. Если чтото существующее подходит не нужно делать чтото новое.
Чтобы не оставлять ошибки в дубликатах, экономить силы программиста и прочее. Читать подробнее в [Википедии](https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D0%B2%D1%82%D0%BE%D1%80%D0%BD%D0%BE%D0%B5_%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5_%D0%BA%D0%BE%D0%B4%D0%B0).
Если есть 2 одинаковые строчки, подумайте, не оформить ли это в функцию, библиотеку или использовать в уже существующую.
Для использования кода с другого устройства - сделайте его библиотекой.



# Поллинг
Не должно быть периодически вызываемых функций с проверкой флагов. Поллинг это плохо. Тратится процессорное время и память для флагов которые проверяются. Также не понятно кто этот флаг ставит, кто его проверяет.

У любого кода есть причина выполнения, вот в обработке причины и нужно вызывать выполнение кода, или запланировать его выполнение.
Используйте инструменты организации кода - корутины и таймменеджер. В прерываниях планируйте задачу с обработкой в бэкграунде. Не используйте флаги.

# Не пишите лишний код, не выполняйте не нужные действия в коде
Пример: если файл с настройками не найден, прошивка использует дефолтные настройки. Не нужно сохранять файл с дефолтными настройками. Файл нужно записывать только если пользователь чтото поменял.
Чтение файла с дефолтными настройками ничем не отличается от отсутствия файла. По этому можно избавиться от лишней операции записи, расхода места иизноса флеш памяти, кода который эту запись делает.

# Не нужно делать в run time все что можно сделать в compile time
Все вычисления констант, генерацию макросов итд, то что не меняется в ходе работы программы нужно вычислять препроцессором на этапе сборки и записывать readonly константами: ресурсы ограничены, и их нужно экономить! Пусть мощный компьютер подготовит все необходимые данные.
По этой же причине следует выделять память статически и не использовать кучу.

# Не нужно делать в контексте прерывания все, что можно сделать в контексте background
Синхронизация асинхронных процессов это источник проблем. У нас есть разные инструменты для организации такой архитектуры. Тайм менеджер, корутины. Мы всегда должны знать что выполняется в прерываниях ВО ВСЕЙ ПРОШИВКЕ, чтобы быть уверенными что там нет ничего лишнего.
Например: в прерывании вызывать только планирование таски, а не само её выполнение.

# Не усложняйте код
Не нужно рассчитывать на тонкости стандартов языка. Не нужно заворачивать сложные конструкции. Код должен прочитать школьник который осилил только первую главу книжки по Си.
Подумайте можно ли сделать ваш код проще ? Часто можно выделить функции, чтото перегруппировать, распутать.
Помните про бритву Оккама.

# Делайте сразу хорошо если понимаете как
Не нужно писать TODO и FIXME. Если в код можно сделать компактнее, алгоритм быстрее, и вы знаете как, то сделайте сразу хорошо. Не надо лениться и аргументировать почему и так пойдет.
Плохо аргументировать фразами "жалко чтоли ? там не много". Такая аргументация не учитывает всю систему целиком, все возможные комбинации и многообразие кейсов применения.
