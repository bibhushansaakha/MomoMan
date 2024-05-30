#pragma once

#include "ofMain.h"
#include "Map.h"

class MomoMan {
public:
    void setup();
    void update(Map &map);
    void draw();
    void keyPressed(int key);
    void keyReleased(int key);

    int x, y; // Position in the grid
    int directionX, directionY; // Direction for movement

    static const int size = 30; // Size of MomoMan
};
