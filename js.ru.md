Wiren Board JavaScript Style Guide
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

