#!/bin/sh
OPTIONS="-Iinclude -lcurses -lm -Wall -O3 -std=gnu17 -o snake"

SRC_FILES="./src/terminalbuffer.c ./src/snake.c ./src/main.c"

cc $OPTIONS $SRC_FILES
