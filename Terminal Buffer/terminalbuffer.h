
#ifndef __TERMINAL__BUFFER_H__
#define __TERMINAL__BUFFER_H__

#define s_X 206
#define s_Y 54

void clearScreen(void);
void Init(void);
void Buffer(const char, int, int);
void Write(void);
void Del(int, int);

#endif