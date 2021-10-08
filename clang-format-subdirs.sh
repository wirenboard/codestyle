#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Apply dry run of clang-format to all *.h and *.cpp files in specified directories recursively."
    echo "Usage: $0 DIR1, DIR2, ..."
    exit 1
fi

FAIL=0

for dir in "$@"; do
    echo $dir
    find ${dir} -iname *.h -o -iname *.cpp | xargs clang-format -n --Werror -i || FAIL=1
done

exit $FAIL
