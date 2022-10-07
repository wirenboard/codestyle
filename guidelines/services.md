Требования к WB сервисам
===

Возвращаемые значения при завершении работы сервиса
---

Сервис в зависимости от типа возникающих ошибок возвращает код:
* `EXIT_SUCCESS=0` (входит в `stdlib.h`) - успешное завершение
* `EXIT_FAILURE=1` (входит в `stdlib.h`) - общая ошибка при неудачном завершении работы сервиса
* `EXIT_INVALIDARGUMENT=2` (входит в спецификацию [LSB](https://refspecs.linuxbase.org/LSB_5.0.0/LSB-Core-generic/LSB-Core-generic/iniscrptact.html)) - неверные или лишние аргументы командной строки
* `EXIT_NOTCONFIGURED=6` (входит в спецификацию [LSB](https://refspecs.linuxbase.org/LSB_5.0.0/LSB-Core-generic/LSB-Core-generic/iniscrptact.html)) - неверная конфигурация

Дополнительные коды можно взять из спецификации:
https://freedesktop.org/software/systemd/man/systemd.exec.html#Process%20Exit%20Codes

Настройка systemd модуля
---

При неудачном завершении сервиса со статусом `EXIT_FAILURE=1` должна производится попытка поторного запуска. За это отвечает параметр в файле настройки systemd модуля:
```bash
[Service]
...
Restart=always
RestartSec=<Время ожидания перед перезапуском службы, сек>
...
```

Для предотвращения повторного запуска сервиса, если возникла неустранимая ошибка в конфигурационных файлах сервиса, либо ошибках оличных от `EXIT_FAILURE`, то добавляется параметр в файл настройки systemd модуля в секцию `Service`:
```bash
[Service]
...
RestartPreventExitStatus=2 3 4 5 6 7
...
```