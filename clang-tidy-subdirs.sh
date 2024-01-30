#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Apply dry run of clang-tidy to all *.h and *.cpp files in specified directories recursively."
    echo "Usage: $0 DIR1, DIR2, ..."
    exit 1
fi

FAIL=0

clang-tidy --version

for dir in "$@"; do
    find "${dir}" -iname '*.h' -o -iname '*.cpp' -type f -print0 | xargs -0 clang-tidy --extra-arg="${CLANG_TIDY_EXTRA_ARG}" -p . || FAIL=1
done

exit $FAIL
