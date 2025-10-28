#!/bin/bash
cp ../codestyle/cpp/config/.clang-format ../codestyle/cpp/config/.clang-tidy -r ../codestyle/cpp/vscode/.vscode/ ./
schroot -c bullseye-amd64-sbuild --directory=/ -- sh -c 'echo "deb [arch=armhf,armel,amd64] http://deb.wirenboard.com/wb8/bullseye unstable main" >> /etc/apt/sources.list.d/wirenboard.list'
schroot -c bullseye-amd64-sbuild --directory=/ -- apt-get update 
schroot -c bullseye-amd64-sbuild --directory=/ -- apt-get -y install libwbmqtt1-5:armhf libwbmqtt1-5-dev:armhf libwbmqtt1-5-test-utils:armhf libjsoncpp24:armhf libjsoncpp-dev:armhf libdb5.3++-dev:armhf libsqlite3-dev:armhf libsqlite3-0:armhf gdbserver:armhf

dir=$(pwd)
schroot -c bullseye-amd64-sbuild --directory=/ -- mkdir -p $dir
echo "$dir  $dir   none    rw,bind         0       0" >> /etc/schroot/sbuild/fstab
