
#ifndef __SNAKE__INTERFACE_H__
#define __SNAKE__INTERFACE_H__

#include "terminalbuffer.h"

#define g_X 180
#define g_Y 45
#define Xmin ((s_X - g_X) / 2)
#define Xmax ((s_X + g_X) / 2)
#define Ymin ((s_Y - g_Y) - 1)
#define Ymax (s_Y - 1)
#define direcUp 1
#define direcRight 2
#define direcDown 3
#define direcLeft 4

typedef struct snakePiece{
    char piece;
    int x, y, x_, y_, direction, rx, ry, rdirection;
} snakePiece ;

typedef struct yum{
    char piece;
    int x, y;
} yum ;

extern long time (long *__timer);   // from time.h
int Random(int, int, int);
snakePiece* InitSnakePieces(int, int, int);
snakePiece generateSnakePiece(const char, int, int, int);
snakePiece makeCopySnakePiece(snakePiece*);
void BufferPieces(snakePiece*, int);
void GoPieces(snakePiece*, int);
void DelPieces(snakePiece*, int);
void InheritRotation(snakePiece*, int);
void rotatePiece(snakePiece*, int, int*, int*);
void goX(snakePiece*, int);
void goY(snakePiece*, int);
int CheckCollapse(snakePiece*, int);
yum* InitYums(int);
yum generateYum(char, int, int);
void BufferYums(yum*, int);
int CheckYum(snakePiece*, yum*, int);
snakePiece* GenerateGreaterSnake(snakePiece*, int, int);

#endif