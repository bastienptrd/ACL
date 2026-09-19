#!/bin/bash

REPO="bastienptrd/ACL"
EXE="mon-programme.exe"

mkdir -p bin

echo "Téléchargement..."

curl -fL \
    "https://github.com/$REPO/releases/latest/download/$EXE" \
    -o "bin/$EXE"

if [ $? -ne 0 ]; then
    echo "Erreur lors du téléchargement."
    exit 1
fi

echo "Lancement..."
./bin/$EXE