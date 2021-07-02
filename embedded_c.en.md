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
## Кодировка
Все файлы должны быть созданы в кодировке UTF-8.

## Конец строки
Конец файла всегда заканчивается переводом строки.

## Выравнивание
Пробелы

1. Отступы 4 пробела между блоками - не использовать символ табуляции (TAB).
2. Пробелами разделяются знаки ``` + != = == - / ```... с двух сторон.
3. Пробелы между ``` if while do for``` и открывающей скобкой выражения.
4. Аргументы функций перечисляются без пробелов.
5. Для макросов, которые именуют константы, значения от 40 до 60 знакоместа с начала строки сдвигать пробелами кратно 4 символам.
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
## Обозначение и скобки
Перенос скобки на следущую строку начала определения осуществляется в функциях, в остальном нет.
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
}
```
Всегда скобки, даже когда тело функции 1 строчка и даже когда его нет:
```C
while () {};

if () {
    return 0;
} else {
    return 1;
}
```
Ранее допущенные ошибки форматирования исправляются в отдельной ветке с ПР согласно кодстайлу.
