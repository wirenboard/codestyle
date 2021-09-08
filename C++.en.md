Wiren Board C++ Style Guide
========================

The following sheet is based on Yandex code style for C++. If any guideline is missing from the following document, 
please follow Yandex official documentation: https://github.com/catboost/catboost/blob/master/CPP_STYLE_GUIDE.md . But if you
see any collision between documents, please follow the guide below. 

## Marking

Indent is 4 spaces wide. You can configure your IDE to insert 4 spaces on pressing Tab.

Aritmetic operations are always separated by spaces:
```C++
int sum = a + b;
```
At sequence of variables comma should be placed right after variable name and the comma should be followed by space before
next variable name. It is true for all kind of punctuation mark (comma, semmicolon, question mark, etc):

```C++
int sum = GetSum (a, b);
if (! variable) {
....
```

## Parentheses

At function declaration curly bracket should be placed in new line after function declaration. 
```C++
int foo ()
{
   std::cout << "foo" << std:endl;
   return 0;
}
```

At conditinal expressions please use compact style, where curly bracket is in the same line with condition. 
```C++
if (foo && bar) {
   std::cout << "foobar" << std:endl;
}
```

At multi-line conditions cury bracket is placed in new line. 
```C++
if (foo &&
    bar)
{
   std::cout << "foobar" << std:endl;
}
```

Basically single-line loops or conditional expressions are not allowed. Plese follow the description above and place curly bracket
in the same line with condition and place program body in the next line. 
```C++
//uncorrect
if (foo) {std::cout << "foo" << std:endl;}
```

```C++
//correct
if (foo) {
    std::cout << "foo" << std:endl;
}
```

Loops without body should be enclosed with curly brackets. 
```C++
while (ReadNoise ()) {}
```




## Naming
### General
In C++ the general naming rule is **JavaCamelCase**.
*snake_case* is allowd only for local variables and they should be never used in one file with CamelCase variables. 

Funtion naming should describe purpose of the function: **const std::string& GetMethodName()**.

The goal of naming is making code more readable and easy to understand function purpose, return value, effect without 
checking the actual implementation of code. It is true at varible names as well. 
Please avoid funtion names like: *DoWork()* or variables like: *counter* etc, except if it does not limit readability, like:
```C++
int buffer = zipNumbers[i];
zipNumbers[i] = zipNumbers[j];
zipNumbers[j] = buffer;
```

Short names, like *i ,j* are basically allowed only as loop variables. 
At shortened names, variable name should be started with capital letter: *TMqttClient*

### Classes

 * Class names should start with capital *T*:  *TModbusClient*.
 * Base classes should include *Base* at the end of class name: *TModbusClientBase*.

Intarface class name should start with letter "*I*" for example: *class IException*

### Methods

Class method naming should follow CamelCase style and start each word with capital letter
regardless it is the first word or not: *GetMethodName*.

### Class fields
Class variable names should start with capital letter.

```C++
class TModbusClient
{
public:

std::string GetMethodName () { return MethodName; };

private:

std::string MethodName;
}
```

### Local variables

Local variable names should start with small letter and followed by capital letters (camelCase): *magicVariableName*. As a second
option snake_case could be also used, but please be careful and never mix it with camelCase.

## Examples

https://github.com/contactless/wb-homa-drivers/tree/master/wb-mqtt-serial
