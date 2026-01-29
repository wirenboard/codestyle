#!/bin/bash

[ -d ./.vscode ] || cp -r ../codestyle/go/vscode/.vscode/ ./

DIR=$(pwd)
DEB_RELEASE="$(source /etc/os-release; echo $VERSION_CODENAME)"
CHROOT="schroot -c ${DEB_RELEASE}-amd64-sbuild --directory=${DIR} --"

echo "${DIR} ${DIR} none rw,bind 0 0" >> /etc/schroot/sbuild/fstab

${CHROOT} apt-get update
${CHROOT} apt-get -y install golang-1.21-go:native gotestsum

${CHROOT} sh -c 'echo "export PATH=/usr/lib/go-1.21/bin:\$PATH" >> /root/.bashrc'
