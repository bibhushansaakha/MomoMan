#include "Map.h"

void Map::setup() {
    loadMap();
}

void Map::update() {
    // Update logic for characters and game state
}

void Map::draw() {
    drawGrid();
    drawWalls();
    drawCharacters();
}

void Map::drawGrid() {
    ofSetColor(200, 200, 200);
    for (int i = 0; i <= gridSize; ++i) {
        ofDrawLine(i * cellSize, 0, i * cellSize, gridSize * cellSize);
        ofDrawLine(0, i * cellSize, gridSize * cellSize, i * cellSize);
    }
}

void Map::drawWalls() {
    ofSetColor(0, 0, 255);
    for (int y = 0; y < gridSize; ++y) {
        for (int x = 0; x < gridSize; ++x) {
            if (mapData[y][x] == 1) {
                ofDrawRectangle(x * cellSize, y * cellSize, cellSize, cellSize);
            }
        }
    }
}

void Map::drawCharacters() {
    // Placeholder for other characters
    ofSetColor(255, 0, 0);
    for (int i = 0; i < 4; ++i) {
        ofDrawCircle(32 * (i + 1) - 16, 32 - 16, 15);
    }
}

void Map::loadMap() {
    // Initialize the map with walls (1) and empty spaces (0)
    int tempMap[gridSize][gridSize] = {
        // A simple example map layout with walls (1) and spaces (0)
        {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
        {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
        {1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1},
        {1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1},
        {1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1},
        {1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1},
        {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
        {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
        // Repeat this pattern to fill the grid (for simplicity)
    };

    // Copy the temporary map to the mapData
    for (int y = 0; y < gridSize; ++y) {
        for (int x = 0; x < gridSize; ++x) {
            mapData[y][x] = tempMap[y][x];
        }
    }
}

bool Map::isWall(int x, int y) {
    if (x >= 0 && x < gridSize && y >= 0 && y < gridSize) {
        return mapData[y][x] == 1;
    }
    return false;
}
