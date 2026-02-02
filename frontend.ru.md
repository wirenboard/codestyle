# Wiren Board Frontend Style Guide

## Javascript
Для проверки кода и форматирования используется [ESLint](https://eslint.org/).

На наших проектах мы используем конфигурацию из пакета `@wirenboard/eslint`. Инструкция по установке в [репозитории пакета](https://github.com/wirenboard/eslint);

### Запуск eslint

```console
$ npx eslint FILE.js
```

### Настройка VSCode

 * устанавливаем расширение ESlint: `Ctrl-Shift-X` (открывает Marketplace), в строке поиска вводим `eslint`,
   устанавливаем первое расширение из списка (от Microsoft);
 * открываем редактор настроек VSCode: `Ctrl-Shift-P`, в поиске вводим `Open User Settings`;
 * устанавливаем галочку в Format a file on save
 * если файлы настройки `eslint` расположены не в каталоге проекта, то надо добавить параметр:
 
```json
{
  "eslint.options": { 
    "overrideConfigFile": "PATH/.eslintrc"
  }
}
``` 

## CSS

### Использование
Для react стили описываем в отдельных css файлах с именем `styles.css` в папке с компонентом. Это позволит избежать проблем с неиспользуемыми стилями, когда компонент уже удален, а css остался.
Также стоит избегать inline стилей, т.к. они могут перебиваться внешними библиотеками.

### Именование классов
Мы используем методологию **BEM** (Block, Element, Modifier) для именования CSS-классов. Это обеспечивает согласованность и предсказуемость в кодовой базе.

Связку Блок -> Элемент пишем через дефис, а Элемент -> Модификатор через camelCase: `.menu-itemActive`

### BEM структура

- **Block** — независимый компонент (`.button`, `.menu`, `.card`)
- **Element** — часть блока, связанная с ним (`.button-icon`, `.menu-item`, `.card-title`)
- **Modifier** — вариант блока или элемента (`.button-iconMobile`, `.menu-itemActive`, `.card-titleWithButton`)
