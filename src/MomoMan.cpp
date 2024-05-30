#include "MomoMan.h"

void MomoMan::setup() {
    x = 1;
    y = 1;
    directionX = 0;
    directionY = 0;
}

void MomoMan::update(Map &map) {
    // Calculate new position
    int newX = x + directionX;
    int newY = y + directionY;

    // Check for collisions with walls
    if (!map.isWall(newX, newY)) {
        x = newX;
        y = newY;
    }
}

void MomoMan::draw() {
    ofSetColor(255, 255, 0);
    ofDrawRectangle(x * Map::cellSize, y * Map::cellSize, size, size);
}

void MomoMan::keyPressed(int key) {
    switch (key) {
        case OF_KEY_LEFT:
            directionX = -1;
            directionY = 0;
            break;
        case OF_KEY_RIGHT:
            directionX = 1;
            directionY = 0;
            break;
        case OF_KEY_UP:
            directionX = 0;
            directionY = -1;
            break;
        case OF_KEY_DOWN:
            directionX = 0;
            directionY = 1;
            break;
    }
}

void MomoMan::keyReleased(int key) {
    directionX = 0;
    directionY = 0;
}
