#include "snake.h"
#include <stdio.h>
#include <stdlib.h>

// Snake Interface
int Random(int min, int max, int seed) {
    srand(seed);
    return (random() % (max-min+1)) + min;
}

snakePiece* GenerateGreaterSnake(snakePiece* p, int pieceCount, int growth) {
    snakePiece* temp = (snakePiece*)malloc((pieceCount+growth) * sizeof(snakePiece));
    for (int i = 0; i < pieceCount; i++)
        temp[i] = makeCopySnakePiece(&(p[i]));
    for (int i = pieceCount; i < pieceCount+growth; i++) {
        temp[i] = makeCopySnakePiece(&(p[pieceCount-1]));
        temp[i].piece = ' ';
        switch (temp[i].direction) {
            case direcRight: temp[i].x = p[pieceCount-1].x - 1; break;
            case direcLeft: temp[i].x = p[pieceCount-1].x + 1; break;
            case direcUp: temp[i].y = p[pieceCount-1].y + 1; break;
            case direcDown: temp[i].y = p[pieceCount-1].y - 1; break;
        }
    }
    return temp;
}

int CheckYum(snakePiece* p, yum* y, int count) {
    for (int i = 0; i < count; i++)
        if (p[0].x == y[i].x && p[0].y == y[i].y)
            return i+1;
    return 0;
} 

void BufferYums(yum* y, int count) {
    for (int i = 0; i < count; i++)
        Buffer(y[i].piece, y[i].x, y[i].y);
}

yum* InitYums(int count) {
    yum* yu = (yum*)malloc(count * sizeof(yum));
    for (int i = 0; i < count; i++)
        yu[i] = generateYum("#$&QS"[i < 4 ? i : 0], Random(Xmin+1, Xmax-1, time((void*)0)), Random(Ymin+1, Ymax-1, i));
    return yu;
}

yum generateYum(char c, int x, int y) {
    yum yum;
    yum.piece = c;
    yum.x = x;
    yum.y = y;
    return yum;
}

int CheckCollapse(snakePiece *p, int pieceCount) {
    for(int i = 1; i < pieceCount; i++)
        if (p[0].x == p[i].x && p[0].y == p[i].y)
            return 1;
        else if (p[0].x == Xmin || p[0].y == Ymin || p[0].x == Xmax || p[0].y == Ymax)
            return 1;
    return 0;
}

void InheritRotation(snakePiece* p, int pieceCount) {
    for(int i = pieceCount - 1; i > 0; i--) {
        p[i].rx = p[i-1].rx;
        p[i].ry = p[i-1].ry;
        p[i].rdirection = p[i-1].rdirection;
    }
}

void GoPieces(snakePiece* p, int pieceCount) {
    for(int i = 0; i < pieceCount; i++) {
        if (p[i].x == p[i].rx && p[i].y == p[i].ry)                         p[i].direction = p[i].rdirection;
        if (p[i].direction == direcRight || p[i].direction == direcLeft)    goX(&(p[i]), 1);
        if (p[i].direction == direcUp || p[i].direction == direcDown)       goY(&(p[i]), 1);
    }
}

void DelPieces(snakePiece* p, int pieceCount) {
    for(int i = 0; i < pieceCount; i++)
        Del(p[i].x_, p[i].y_);
}

void BufferPieces(snakePiece* p, int pieceCount) {
    switch (p->direction) {
        case direcRight: p[0].piece = '>'; break;
        case direcLeft: p[0].piece = '<'; break;
        case direcUp: p[0].piece = '^'; break;
        case direcDown: p[0].piece = 'V'; break;
    }
    for(int i = 0; i < pieceCount; i++)
        Buffer(p[i].piece, p[i].x, p[i].y);
}

snakePiece* InitSnakePieces(int pieceCount, int iX, int iY) {
    snakePiece* sp = (snakePiece*)malloc(pieceCount * sizeof(snakePiece));
    for (int i = 0; i < pieceCount; i++)
        sp[i] = generateSnakePiece('O', iX - i, iY, direcRight);
    return sp;
}

snakePiece generateSnakePiece(const char piece, int x, int y, int direction) {
    snakePiece p;
    p.piece = piece;
    p.rdirection = p.direction = direction;
    p.x = p.x_ = x;
    p.y = p.y_ = y;
    p.rx = p.ry = 0;
    return p;
}

snakePiece makeCopySnakePiece(snakePiece* s1) {
    snakePiece p;
    p.piece = s1->piece;
    p.direction = s1->direction;
    p.rdirection = s1->rdirection;
    p.x = s1->x;
    p.y = s1->y;
    p.rx = s1->rx;
    p.ry = s1->ry;
    p.x_ = s1->x_;
    p.y_ = s1->y_;
    return p;
}

void rotatePiece(snakePiece* p, int newDirection, int* rX, int* rY) {
    if ((p->direction + 2) == newDirection || (p->direction - 2) == newDirection) return;
    p->rdirection = p->direction = newDirection;
    p->rx = *rX = p->x;
    p->ry = *rY = p->y;
}

void goX(snakePiece* p, int dx) {
    p->x_ = p->x;
    p->y_ = p->y;
    if (p->direction == direcRight)     p->x += dx;
    if (p->direction == direcLeft)      p->x -= dx;
}

void goY(snakePiece* p, int dy) {
    p->y_ = p->y;
    p->x_ = p->x;
    if (p->direction == direcDown)  p->y += dy;
    if (p->direction == direcUp)    p->y -= dy;
}

