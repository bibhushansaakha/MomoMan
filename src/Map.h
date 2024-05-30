#pragma once

#include "ofMain.h"

class Map {
public:
    void setup();
    void update();
    void draw();

    static const int gridSize = 32;
    static const int cellSize = 32;
    int mapData[gridSize][gridSize];

    void drawGrid();
    void drawWalls();
    void drawCharacters();

    void loadMap(); // This function will load the map layout

    bool isWall(int x, int y); // Function to check if a cell is a wall
};
