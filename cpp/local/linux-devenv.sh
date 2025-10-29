#!/bin/bash
cp ../codestyle/cpp/config/.clang-format ../codestyle/cpp/config/.clang-tidy ./
cp -r ../codestyle/cpp/vscode/.vscode/ ./

DIR=$(pwd)
DEB_RELEASE="$(source /etc/os-release; echo $VERSION_CODENAME)"
CHROOT="schroot -c ${DEB_RELEASE}-amd64-sbuild --directory=${DIR} --"

echo "${DIR} ${DIR} none rw,bind 0 0" >> /etc/schroot/sbuild/fstab

LIST=$(${CHROOT} dpkg-checkbuilddeps 2>&1 | sed 's/dpkg-checkbuilddeps:\serror:\sUnmet build dependencies: //g' | sed 's/[\(][^)]*[\)] *//g')
DEPS=()

for TARGET in wb7 wb8; do
    case ${TARGET} in
        wb8) 
            ARCH=arm64 
            ;;
        *)   
            ARCH=armhf 
            ;;
    esac

    for ITEM in ${LIST}; do
        if [[ ${ITEM} != *:all ]]; then
            ITEM+=":${ARCH}"
        fi
        DEPS+=(${ITEM})
    done
    echo ${DEPS[@]}

    ${CHROOT} bash -c "echo \"deb http://deb.wirenboard.com/${TARGET}/${DEB_RELEASE} unstable main\" > /etc/apt/sources.list.d/wirenboard-unstable-${TARGET}.list"
done

${CHROOT} apt-get update
${CHROOT} apt install -y ${DEPS[@]}

apt update
apt install gdb-multiarch
