#!/bin/bash
clang-format -style='{
    BasedOnStyle: llvm,
    IndentWidth: 4,
    BreakBeforeBraces: Custom,
    BraceWrapping: {
        AfterFunction: true,
        AfterClass: true,
        AfterStruct: true,
        AfterNamespace: true,
        AfterUnion: true,
        AfterEnum: true,
        },
    ColumnLimit: 100,
    AllowShortIfStatementsOnASingleLine: true,
    AllowShortLoopsOnASingleLine: true,
    PointerAlignment: Left,
    AccessModifierOffset: -4,
    AllowShortFunctionsOnASingleLine: Empty,
    }' -i $@
