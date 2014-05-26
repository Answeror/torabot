#!/usr/bin/env bash

for i in `find torabot/mods/ -exec test -f {}/static/package.json \; -print`; do
    if [ "$#" -lt 1 ] || [ "torabot/mods/$1" == "$i" ]; then
        pushd $i/static > /dev/null
        spm build
        spm install -d ../../../frontend/main/static/sea-modules/ .
        popd > /dev/null
    fi
done

if [ "$#" -lt 1 ] || [ "$1" == "main" ]; then
    pushd torabot/frontend/main/static > /dev/null
    spm build
    spm install .
    popd > /dev/null
fi
