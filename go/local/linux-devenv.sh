#!/bin/bash

[ -d ./.vscode ] || cp -r ../codestyle/go/vscode/.vscode/ ./

GOVERSION=1.25.6

curl -LO https://go.dev/dl/go$GOVERSION.linux-amd64.tar.gz
tar -C /usr/local -xzf go$GOVERSION.linux-amd64.tar.gz
rm -f go$GOVERSION.linux-amd64.tar.gz

/usr/local/go/bin/go install github.com/go-delve/delve/cmd/dlv@latest
/usr/local/go/bin/go install golang.org/x/tools/gopls@latest
/usr/local/go/bin/go install gotest.tools/gotestsum@latest
