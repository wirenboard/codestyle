# Руководство по установке окружения из fit образа для сборки C++ проектов

## Подготовка

Скачиваем необходимый fit образ либо с билд сервера либо со [страницы](http://fw-releases.wirenboard.com/?prefix=fit_image/stable/).

Устанавливаем в систему зависимости:
```shell
sudo apt install -y u-boot-tools qemu-user-static binfmt-support
```

Извлекаем rootfs из fit образа:
```shell
dumpimage -T flat_dt -p 3 -o rootfs.tar.gz <image>.fit
```

##### Примечание:

Утилита dumpimage входит в пакет u-boot-tools.
Извлечение работает с версиями dumpimage
* 2021.01+dfsg-5
* 2021.01+dfsg-3ubuntu0~20.04.4

Не работает с версией
* 2022.01+dfsg-2ubuntu2

Распаковываем rootfs в директорию:
```shell
mkdir rootfs
sudo tar zxvf rootfs.tar.gz -C rootfs/
```

Запускаем chroot окружение:
```shell
cd rootfs
./chroot_this.sh
```

## В chroot окружении

В chroot окружении устанавливаем необходимые для сборки пакеты. 

Необходимые для сборки зависимости можно найти в директории `debian/control` проекта.
```shell
apt update && apt upgrade
apt install -y build-essential
...
```

Зависимости для google test:
```shell
apt install -y googletest libgtest-dev libgmock-dev
```

Для работы с IDE по ssh устанавливаем:
```shell
apt install -y ssh
```

В файле настройки ssh сервера `/etc/ssh/sshd_config` меняем порт:
```
# Package generated configuration file
# See the sshd_config(5) manpage for details

# What ports, IPs and protocols we listen for
Port 2234
...
```

Генерируем ключи для ssh сервера:
```shell
ssh-keygen -A
```

Запускаем ssh сервер:
```shell
service ssh start
```

При последующем входе в chroot окружение необходимо запускать ssh сервер вручную.

Настраиваем IDE и подключаемся к указанному порту по ssh.
