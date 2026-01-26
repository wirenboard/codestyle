#!/bin/bash
TARGET_LIST="wb7 wb8"

cp ../codestyle/cpp/config/.clang-format ../codestyle/cpp/config/.clang-tidy ./
[ -d ./.vscode ] || cp -r ../codestyle/cpp/vscode/.vscode/ ./

DIR=$(pwd)
DEB_RELEASE="$(source /etc/os-release; echo $VERSION_CODENAME)"
CHROOT="schroot -c ${DEB_RELEASE}-amd64-sbuild --directory=${DIR} --"

echo "${DIR} ${DIR} none rw,bind 0 0" >> /etc/schroot/sbuild/fstab

for TARGET in ${TARGET_LIST}; do
    ${CHROOT} bash -c "echo \"deb http://deb.wirenboard.com/${TARGET}/${DEB_RELEASE} unstable main\" > /etc/apt/sources.list.d/wirenboard-unstable-${TARGET}.list"
done
${CHROOT} apt-get update

../codestyle/cpp/local/linux-devenv-deps.sh

apt update
apt install gdb-multiarch
