#!/bin/bash

REPO="bastienptrd/ACL"
EXE="mon-jeu.exe"

URL="https://github.com/$REPO/releases/latest/download/$EXE"

echo "Téléchargement de $EXE..."

mkdir -p bin

curl -fL "$URL" -o "bin/$EXE"

if [ $? -ne 0 ]; then
    echo "Erreur : téléchargement impossible."
    exit 1
fi

echo "Téléchargement terminé !"
echo "Le jeu se trouve dans : bin/$EXE"

./bin/$EXE
