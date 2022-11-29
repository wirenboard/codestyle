Утилиты на все случаи жизни
===========================

Сборка
------

 * [ccache](https://ccache.dev/) - ускоряет сборку за счёт сохранения скомпилированных файлов

Отладка
-------

 * [valgrind](https://valgrind.org/) - отлавливает утечки памяти в С/С++ проектах

Работа с Git
------------

  * [gitk](https://git-scm.com/docs/gitk/) - рисует дерево коммитов в графическом виде
    * Альтернатива на Qt - [qgit](https://github.com/tibirna/qgit)
  * [gh](https://cli.github.com/) - работа с GitHub через консоль
    * Список всех открытых PR по всем WB репам: `gh search prs --owner=wirenboard --state=open`
    * Список PR для текущей репы: `gh pr list`
    * Посмотреть PR: `gh pr diff <number>`
    * Оставить ревью: `gh pr review <number>`
    * Смержить (сквош) и удалить бранч: `gh pr merge <number> -s -d`
    * Список всех репозиториев: `gh repo list -L 200 --json name wirenboard | jq -r '.[].name'`

Окружение для разработки
------------------------

 * [direnv](https://direnv.net/) - создаёт изолированные окружения под разные проекты (подробнее тут https://github.com/wirenboard/wb-nixpkgs#development)
