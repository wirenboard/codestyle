#!/bin/bash

TARGET="wb7"

case ${TARGET} in
    wb8) 
        ARCH=arm64 
        export DEB_HOST_MULTIARCH="aarch64-linux-gnu"
        ;;
    *)   
        ARCH=armhf 
        export DEB_HOST_MULTIARCH="arm-linux-gnueabihf"
        ;;
esac

cp ../codestyle/cpp/config/.clang-format ../codestyle/cpp/config/.clang-tidy ./
cp -r ../codestyle/cpp/vscode/.vscode/ ./
envsubst < .vscode/tasks.json > .vscode/tasks.json.tmp && mv .vscode/tasks.json.tmp .vscode/tasks.json

DIR=$(pwd)
DEB_RELEASE="$(source /etc/os-release; echo $VERSION_CODENAME)"
CHROOT="schroot -c ${DEB_RELEASE}-amd64-sbuild --directory=${DIR} --"

echo "${DIR} ${DIR} none rw,bind 0 0" >> /etc/schroot/sbuild/fstab

LIST=$(${CHROOT} dpkg-checkbuilddeps 2>&1 | sed 's/dpkg-checkbuilddeps:\serror:\sUnmet build dependencies: //g' | sed 's/[\(][^)]*[\)] *//g')
DEPS=()

for ITEM in ${LIST}; do
    if [[ ${ITEM} != *:all ]]; then
        ITEM+=":${ARCH}"
    fi
    DEPS+=(${ITEM})
done

${CHROOT} bash -c "echo \"deb http://deb.wirenboard.com/${TARGET}/${DEB_RELEASE} unstable main\" > /etc/apt/sources.list.d/wirenboard-unstable.list"
${CHROOT} apt-get update
${CHROOT} apt install -y ${DEPS[@]} gdbserver:${ARCH}

apt update
apt install gdb-multiarch
