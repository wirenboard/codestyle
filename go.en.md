## Style guide

Format your code with `go fmt`.

## Static analysis

Install [staticcheck](https://staticcheck.dev/):
```sh
apt install go-staticcheck
```

Running:
```sh
go mod vendor
staticcheck -go 1.13 ./...
```
