#include <stdio.h>
#include <stdlib.h>
#include <curses.h>
#include "snake.h"
#include "terminalbuffer.h"

void BufferGameboard(void);
void BufferStats(int,int,int);
void BufferCreator(char*);
void BufferFinishText(char*, int);
int Greetings(void);
int strLen(char*);

int main(int argc, char *argv[]) {
    // Variables
    int rx, ry, pc, key, level, yc, gt, ye, score, timelapse;
    score = 1;
    yc = 1;
    ye = 0;
    gt = 0;
    pc = 9;
    level = 1;
    snakePiece* p = InitSnakePieces(pc, 50, 30);
    yum* y = InitYums(yc);
    char* finishedText = "||| Oops, you died... |||";

    // Greetings
    timelapse = Greetings();

    // Inits
    Init();
    Write();
    clearScreen();
    initscr(); cbreak(); noecho();
    curs_set(0);
    nodelay(stdscr, 1);
    keypad(stdscr, 1);
    BufferGameboard();
    BufferYums(y, yc);
    BufferCreator("Made possible by Zarathustra");
    
    while (1) {
        // Game Logic
        key = getch();
        if (key == KEY_UP)      rotatePiece(&(p[0]), direcUp, &rx, &ry);
        if (key == KEY_DOWN)    rotatePiece(&(p[0]), direcDown, &rx, &ry);
        if (key == KEY_RIGHT)   rotatePiece(&(p[0]), direcRight, &rx, &ry);
        if (key == KEY_LEFT)    rotatePiece(&(p[0]), direcLeft, &rx, &ry);
        GoPieces(p, pc-gt);
        InheritRotation(p, pc);
        if ((ye = CheckYum(p, y, yc))) {
            level++;
            gt = 5;
            y[ye-1] = generateYum("#$&QS"[ye-1 < 4 ? ye-1 : 0], Random(Xmin+1, Xmax-1, ye + time(NULL)), Random(Ymin+1, Ymax-1, time(NULL)));
            if (yc < level/gt + 1) y = InitYums(++yc);
            p = GenerateGreaterSnake(p, pc, gt);
            pc += gt;
            score++;
            if (score % gt == 0 && timelapse > 9) timelapse -= 5;
            BufferYums(y, yc);
        }
        if (gt) p[pc-(gt--)].piece = 'O';
        if (CheckCollapse(p ,pc-gt)) break;

        // Draw
        BufferPieces(p, pc);
        BufferStats((level/5)+1, score, pc-gt);
        Write();
        DelPieces(p, pc);
        napms(timelapse);
        clearScreen();
    }
    for (int i = 0; i < pc; i++) {
        // Show snake died
        p[i].piece = 'X';
        BufferPieces(p, pc);
        Write();
        napms(30);
        clearScreen();
    }
    for (int i = 0; i < strLen(finishedText); i++) {
        // Oops, you died...
        BufferFinishText(finishedText, i);
        Write();
        napms(50);
        clearScreen();
    }
    free(p); free(y);
    curs_set(2);
    getchar();
    getchar();
    getchar();
    exit(0);
}

// Funcs
int Greetings() {
    int difficulty = 0;
    printf("\nWelcome to the snake game!\n");
    printf("--------------------------\n\n");
    printf("On which difficulty level do you wish to play? (1, 2, 3, 4)\n");
    printf("  :: ");
    if ((difficulty = getchar() - 48) == 1 || difficulty == 2 || difficulty == 3 || difficulty == 4) {
        getchar();
        printf("\nYou prefer to play in difficulty level %d. \n", difficulty);
        printf("\nDone!\nPress any key to continue.\n");
        getchar();
    } 
    else {
        printf("\nLooks like we won't get to keep up with you.\n");
        exit(0);
    }
    switch (difficulty) {
        case 1: return 100; break;
        case 2: return 70; break;
        case 3: return 50; break;
        case 4: return 30; break;
        default: return -1; break;
    }
}

void BufferFinishText(char* text, int i) {
    int len = strLen(text);
    Buffer(text[i], s_X / 2 - len / 2 + i, s_Y / 2);
    Buffer(' ', s_X / 2 - len / 2 + i, s_Y / 2 + 1);
    Buffer(' ', s_X / 2 - len / 2 + i, s_Y / 2 + -1);
}

void BufferCreator(char* name){
    int len = strLen(name);
    for (int i = 0; i < len; i++)
        Buffer(name[i], (s_X - len) / 2 + i, 1);
}

void BufferStats(int level, int score, int length) {
    int hundreds, tens, ones, i;

    for (i = 0; i < strLen("Level: "); i++)
        Buffer("Level: "[i], i + Xmin, 2);
    tens = level / 10;
    ones = level % 10;
    i += Xmin;
    Buffer(tens + '0', i++, 2);
    Buffer(ones + '0', i, 2);

    for (i = 0; i < strLen("Score: "); i++)
        Buffer("Score: "[i], i + Xmin + 1, 4);
    tens = score / 10;
    ones = score % 10;
    i += Xmin;
    Buffer(tens + '0', i++, 4);
    Buffer(ones + '0', i, 4);

    for (i = 0; i < strLen("Snake Length: "); i++)
        Buffer("Snake Length: "[i], i + Xmin + 1, 6);
    hundreds = length / 100;
    tens = length / 10;
    ones = length % 10;
    i += Xmin;
    Buffer(hundreds + '0', i++, 6);
    Buffer(tens + '0', i++, 6);
    Buffer(ones + '0', i, 6);

    for (i = 2; i < 7; i++)
        Buffer('|', (i < 3) ? Xmin - 1 : Xmin, i);
}

void BufferGameboard(void) {
    for (int x = Xmin; x < Xmax+1; x++) {
        Buffer('#', x, Ymin);
        Buffer('#', x, Ymax);
    } 
    for (int y = Ymin; y < Ymax+1; y++) {
        Buffer('#', Xmin, y);
        Buffer('#', Xmax, y);
    }
}

int strLen(char* str) {
    char* p = str;
    while (*p++);
    return p - str;
}
