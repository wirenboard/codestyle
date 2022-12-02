Интеграция компонентов React в приложение на AngularJS
===
React предназначен для построения UI, он манипулирует DOM. 

Цитата [отсюда](https://reactjs.org/docs/rendering-elements.html#updating-the-rendered-element):
```
React elements are immutable. Once you create an element, you can’t change its children or attributes. An element is like a single frame in a movie: it represents the UI at a certain point in time.

With our knowledge so far, the only way to update the UI is to create a new element, and pass it to root.render().
```

Надо найти компонент AngularJS, который предназначен для управления DOM, и будет вызывать методы React для перерисовки при каждом изменении состояния. Это [директива](https://docs.angularjs.org/guide/directive#creating-a-directive-that-manipulates-the-dom).

Пример минимальной директивы, которая использует React для построения интерфейса:
```js
import React from 'react';
import ReactDOM from 'react-dom/client';

// Импортируем компонент React
import ReactbasedComponent from 'reactbased';

function myDirective() {
    return {
        restrict: 'E',
        scope: {
            // Параметр для передачи состояния в директиву
            data: '='
        },
        link: function (scope, element) {
            // Привяжем React к элементу DOM
            scope.root = ReactDOM.createRoot(element[0]);

            // Отрисуем начальное состояние
            scope.root.render(<ReactbasedComponent {...scope.data}/>);

            // Подпишемся на оповещения об изменении состояния
            scope.watcher = scope.$watch('data', function (newValue) {
                scope.root.render(<ReactbasedComponent {...newValue}/>);
            });

            // Удалим за собой всё, связанное с React, при разрушении элемента
            element.on('$destroy', function() {
                scope.root.unmount();
            });

            // Отпишемся от оповещений об изменении состояния
            scope.$on('$destroy', function() {
                scope.watcher();
            });
        }
    };
}

export default myDirective;
```

Зарегистрируем в приложении нашу директиву:
```js
import myDirective from 'myDirective';

angular.module("MyApp", []).directive("myDirective", myDirective);
```

Теперь директиву можно использовать в шаблоне, где `model` - [модель данных](https://docs.angularjs.org/guide/concepts#model) в терминах AngularJS.
```html
<my-directive data="model"></my-directive>
```
