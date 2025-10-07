Wiren Board JavaScript Style Guide
==============================

Для проверки кода и форматирования используется [ESLint](https://eslint.org/).

На наших проектах мы используем конфигурацию из пакета `@wirenboard/eslint`. Инструкция по установке в [репозитории пакета](https://github.com/wirenboard/eslint);

### Запуск eslint

```console
$ npx eslint FILE.js
```

Настройка IDE
-------------

### VSCode

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

