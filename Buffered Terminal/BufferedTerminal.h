namespace ren {
    #pragma once
    #include <iostream>
    /*      *//*USAGE*//*
    ren::Init();
    while (!isFinished) {
        ren::Buffer('?', x, y);
        ren::Write();   
    
        // make some controls on the x & y.
        // do the changes on x & y.
        ren::Del(x_, y);    // x_ being the x coordinate before the change.
        std::this_thread::sleep_for(std::chrono::milliseconds(T));
        ren::Clear();
    
    */// Terminal Sizes:
    const int X = 159;
    const int Y = 39;

    int ind[X][Y];
    char mes[X*Y];
    static void Clear () {
        system("clear");
    }
    static void Init () {
        for(int y = 0; y < Y; y++) 
            for (int x = 0; x < X; x++) 
                ind[x][y] = 0;
        for(int i = 0; i < X*Y; i++)
            mes[i] = ' ';
        system("clear");
    }
    static void Buffer (const char message, const int& x, const int& y) {
        ind[x][y] = 1;
        mes[y*X+x] = message;
    }
    static void Write () {
        for(int y = 0; y < Y; y++) {
            for(int x = 0; x < X; x++) {
                if (ind[x][y] == 1)
                    std::cerr << mes[y*X+x];
                else std::cerr << ' ';
            }
            std::cerr<<"\n";
        }
    }
    static void Del (const int& x, const int& y) {
        ind[x][y] = 0;
        mes[y*X+x] = ' ';
    }
}
