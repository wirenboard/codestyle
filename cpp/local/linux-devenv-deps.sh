#!/bin/bash
TARGET_LIST="wb7 wb8"

DIR=$(pwd)
DEB_RELEASE="$(source /etc/os-release; echo $VERSION_CODENAME)"
CHROOT="schroot -c ${DEB_RELEASE}-amd64-sbuild --directory=${DIR} --"

LIST=$(${CHROOT} dpkg-checkbuilddeps 2>&1 | sed 's/dpkg-checkbuilddeps:\serror:\sUnmet build dependencies: //g' | sed 's/[\(][^)]*[\)] *//g')
DEPS=()

for TARGET in ${TARGET_LIST}; do
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
done

${CHROOT} apt install -y ${DEPS[@]}