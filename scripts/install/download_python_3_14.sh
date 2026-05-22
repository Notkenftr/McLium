#!/bin/bash

URL="https://www.python.org/ftp/python/3.14.5/Python-3.14.5.tar.xz"
NAME="Python-3.14.5.tar.xz"

BASE_DIR="$(pwd)"

mkdir -p "$BASE_DIR/../../temp"
mkdir -p "$BASE_DIR/../../runtime/py"

TEMP_DIR="$(cd "$BASE_DIR/../../temp" && pwd)"
RUNTIME_DIR="$(cd "$BASE_DIR/../../runtime/py" && pwd)"

echo $TEMP_DIR
echo $RUNTIME_DIR

if [ -f "$RUNTIME_DIR/bin/python3" ]; then
    echo "Skip download py.."
    exit 0
fi

cd "$TEMP_DIR" || exit 1
if command -v wget >/dev/null 2>&1; then
    wget -O "$NAME" "$URL"
elif command -v curl >/dev/null 2>&1; then
    curl -L "$URL" -o "$NAME"
else
    echo "Error: wget or curl required for downloading."
    exit 1
fi

echo "Extracting..."
tar -xf "$NAME"
EXTRACTED_DIR=$(tar -tf "$NAME" | head -1 | cut -d "/" -f1)

cd "$EXTRACTED_DIR" || exit 1

echo "Configure..."

./configure --prefix="$RUNTIME_DIR" --enable-optimizations

make -j$(nproc)

rm -rf "$RUNTIME_DIR"/*
make install

cd "$BASE_DIR" || exit 1
rm -rf "$TEMP_DIR/$EXTRACTED_DIR"
rm -f "$TEMP_DIR/$NAME"

echo "$RUNTIME_DIR"
