#include <iostream>
#include <thread>
#include "BufferedTerminal.h"

class Player {
public:
    int x, y;
    int x_, y_;
    char* name;
    Player(int X, int Y, char* Name): x(X), y(Y), name(Name), x_(X), y_(Y) {}
    void GoX (const int& dx) {
        x_=x;
        x+=dx;
    }
    void GoY (const int& dy) {
        y_=y;
        y+=dy;
    }
};


int main() {  
    Player player(0,0,"Mary");
    ren::Init();
    while (1) {
        ren::Buffer('X', player.x, player.y);
        ren::Write();

        if (player.y == ren::Y)
            player.y = 0;
        if (player.x == ren::X) {
            player.x = 0;
            player.GoY(1);
        }
        player.GoX(1);
        ren::Del(player.x_, player.y);
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
        ren::Clear();
    }

}
