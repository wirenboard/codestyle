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

Также можно добавить алиасы в git конфиг:
```
$ cat ~/.config/git/config
[alias]
	jl = "!git rev-parse --abbrev-ref HEAD | sed 's#/#%252F#' | xargs -I{} sh -c \"jcli job log $(basename $PWD)/job/{}\""
	jb = "!git rev-parse --abbrev-ref HEAD | sed 's#/#%252F#' | xargs -I{} sh -c \"jcli job build $(basename $PWD)/job/{}\""
	jd = "!git rev-parse --abbrev-ref HEAD | sed 's#/#%252F#' | xargs -I{} sh -c \"jcli job artifact download $(basename $PWD)/job/{}\""
```

### Исправление постоянных 404 при переходе по ссылкам

Это обычно происходит в пайплайнах, которые собирают ветки с `/` в имени
(все наши `feature/12345-foo` и `tmp/me/fixing`).

Это происходит из-за бага в Jenkins, который не чинят уже несколько лет:
https://issues.jenkins.io/browse/JENKINS-54044

На месте проблема решается заменой всех `%2F` в пути на `%252F`.
Чтобы не делать это каждый раз вручную, можно использовать плагин Redirector
(доступен для [Firefox](https://addons.mozilla.org/ru/firefox/addon/redirector/),
Chrome и Opera).

Вот набор правил, которые исправляют проблему в самых частых случаях
(экспортировано из Redirector для Firefox):

```json
{
    "createdBy": "Redirector v3.5.3",
    "createdAt": "2023-04-07T18:54:10.163Z",
    "redirects": [
        {
            "description": "Fix Jenkins paths with %2F 3 times",
            "exampleUrl": "https://jenkins.wirenboard.com/job/wirenboard/job/wb-mqtt-serial/job/release%2Fwb-2304%2Fstretch%2Ffoobar/",
            "exampleResult": "https://jenkins.wirenboard.com/job/wirenboard/job/wb-mqtt-serial/job/release%252Fwb-2304%252Fstretch%252Ffoobar/",
            "error": null,
            "includePattern": "(https://jenkins.wirenboard.com/.*)%2F(.*)%2F(.*)%2F(.*)",
            "excludePattern": "",
            "patternDesc": "",
            "redirectUrl": "$1%252F$2%252F$3%252F$4",
            "patternType": "R",
            "processMatches": "noProcessing",
            "disabled": false,
            "grouped": false,
            "appliesTo": [
                "main_frame"
            ]
        },
        {
            "description": "Fix Jenkins paths with %2F 2 times",
            "exampleUrl": "https://jenkins.wirenboard.com/job/wirenboard/job/wb-mqtt-serial/job/release%2Fwb-2304%2Fstretch/",
            "exampleResult": "https://jenkins.wirenboard.com/job/wirenboard/job/wb-mqtt-serial/job/release%252Fwb-2304%252Fstretch/",
            "error": null,
            "includePattern": "(https://jenkins.wirenboard.com/.*)%2F(.*)%2F(.*)",
            "excludePattern": "",
            "patternDesc": "",
            "redirectUrl": "$1%252F$2%252F$3",
            "patternType": "R",
            "processMatches": "noProcessing",
            "disabled": false,
            "grouped": false,
            "appliesTo": [
                "main_frame"
            ]
        },
        {
            "description": "Fix Jenkins paths with %2F 1 times",
            "exampleUrl": "https://jenkins.wirenboard.com/job/wirenboard/job/wb-mqtt-serial/job/release%2Fwb-2304/",
            "exampleResult": "https://jenkins.wirenboard.com/job/wirenboard/job/wb-mqtt-serial/job/release%2Fwb-2304/",
            "error": null,
            "includePattern": "(https://jenkins.wirenboard.com/.*)%2F(.*)",
            "excludePattern": "",
            "patternDesc": "",
            "redirectUrl": "$1%252F$2",
            "patternType": "R",
            "processMatches": "noProcessing",
            "disabled": false,
            "grouped": false,
            "appliesTo": [
                "main_frame"
            ]
        }
    ]
}
```


Окружение для разработки
------------------------

 * [direnv](https://direnv.net/) - создаёт изолированные окружения под разные проекты (подробнее тут https://github.com/wirenboard/wb-nixpkgs#development)

MQTT
----

 * [MQTT-Explorer](https://github.com/thomasnordquist/MQTT-Explorer) - GUI клиент
 * [mqttui](https://github.com/EdJoPaTo/mqttui) - TUI клиент
