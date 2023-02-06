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
    * Список всех открытых PR по всем WB репам: `gh search prs --owner=wirenboard --state=open --sort created -L 100`
    * Список всех issues по всем WB репам: `gh search issues --owner=wirenboard --state=open --sort created -L 100`
    * Список PR для текущей репы: `gh pr list`
    * Посмотреть PR: `gh pr diff <number>`
    * Оставить ревью: `gh pr review <number>`
    * Смержить (сквош) и удалить бранч: `gh pr merge <number> -s -d`
    * Список всех репозиториев: `gh repo list -L 200 --json name wirenboard | jq -r '.[].name'`
    * Основная ветка репозитория: `gh repo view --json defaultBranchRef --jq .defaultBranchRef.name`
  * [mu-repo](https://fabioz.github.io/mu-repo/) - работа с множеством git репозиториев (à la монорепа):
```sh
gh repo list -L 200 --json name wirenboard | jq -r '.[].name' | \
  xargs -P1 -I % sh -c 'gh repo clone wirenboard/% -- --recurse-submodules'
mu register --all
...
ulimit -n 10240 # required on macOS
mu fetch --all --prune
mu pull
```

Работа с Jenkins
----------------

 * [jenkins-cli](https://github.com/jenkins-zh/jenkins-cli) - работа с Jenkins через консоль
   * В разделе Configure нужно создать API Token
   * Создать конфиг:
```sh
cat > ~/.jenkins-cli.yaml << EOF
current: wirenboard
jenkins_servers:
- name: wirenboard
  url: https://jenkins.wirenboard.com/job/wirenboard
  username: <username>
  token: <token>
  insecureSkipVerify: true
EOF
```
   * Посмотреть логи: `jcli job log wb-mqtt-serial/job/master`
   * Триггернуть сборку: `jcli job build wb-mqtt-serial/job/master`
   * Скачать deb пакет последней сборки для текущей ветки: `git rev-parse --abbrev-ref HEAD | sed 's#/#%252F#' | xargs -I{} sh -c "jcli job artifact download $(basename $PWD)/job/{}"`

Окружение для разработки
------------------------

 * [direnv](https://direnv.net/) - создаёт изолированные окружения под разные проекты (подробнее тут https://github.com/wirenboard/wb-nixpkgs#development)
