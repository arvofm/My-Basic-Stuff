#include <stdio.h>
#include "terminalbuffer.h"

// Terminal Buffer Interface
static char buf[s_X * s_Y];

void clearScreen(void) {
    //printf("\x1b[H");
    fputs("\x1b[H", stdout);
}

void Init(void) {
    for (int i = 0; i < s_X*s_Y; i++)
        buf[i] = ' ';
    fputs("\x1b[H", stdout);
}

void Buffer(const char m, int x, int y) {
    buf[y*s_X + x] = m;
}

void Write(void) {
    for (int y = 0; y < s_Y; y++) {
        for (int x = 0; x < s_X; x++) {
            if (buf[y*s_X + x] != ' ')
                putchar(buf[y*s_X + x]);
            else
                putchar(' ');
        }
    }
}

void Del(int x, int y) {
    buf[y*s_X + x] = ' ';
}

