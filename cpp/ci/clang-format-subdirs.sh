#!/usr/bin/env bash

if [ $# -eq 0 ]; then
    echo "Apply dry run of clang-format to all *.h and *.cpp files in specified directories recursively."
    echo "Usage: $0 DIR1, DIR2, ..."
    exit 1
fi

FAIL=0

clang-format --version

for dir in "$@"; do
    find "${dir}" \( -iname '*.h' -o -iname '*.cpp' \) -type f -print0 | xargs -0 clang-format -n --Werror -i || FAIL=1
done

exit $FAIL
