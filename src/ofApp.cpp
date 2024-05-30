#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup() {
    ofSetFrameRate(60);
    gameMap.setup();
    momoMan.setup();
}

//--------------------------------------------------------------
void ofApp::update() {
    momoMan.update(gameMap);
}

//--------------------------------------------------------------
void ofApp::draw() {
    gameMap.draw();
    momoMan.draw();
}

//--------------------------------------------------------------
void ofApp::keyPressed(int key) {
    momoMan.keyPressed(key);
}

//--------------------------------------------------------------
void ofApp::keyReleased(int key) {
    momoMan.keyReleased(key);
}

//--------------------------------------------------------------
void ofApp::mouseMoved(int x, int y) {

}

//--------------------------------------------------------------
void ofApp::mouseDragged(int x, int y, int button) {

}

//--------------------------------------------------------------
void ofApp::mousePressed(int x, int y, int button) {

}

//--------------------------------------------------------------
void ofApp::mouseReleased(int x, int y, int button) {

}

//--------------------------------------------------------------
void ofApp::mouseEntered(int x, int y) {

}

//--------------------------------------------------------------
void ofApp::mouseExited(int x, int y) {

}

//--------------------------------------------------------------
void ofApp::windowResized(int w, int h) {

}

//--------------------------------------------------------------
void ofApp::gotMessage(ofMessage msg) {

}

//--------------------------------------------------------------
void ofApp::dragEvent(ofDragInfo dragInfo) {

}
