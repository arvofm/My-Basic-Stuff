
#ifndef __TERMINAL__BUFFER_H__
#define __TERMINAL__BUFFER_H__

#define s_X 170
#define s_Y 43

void clearScreen(void);
void Init(void);
void Buffer(const char, int, int);
void Write(void);
void Del(int, int);

#endif
