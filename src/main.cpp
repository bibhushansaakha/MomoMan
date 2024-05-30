#include "ofMain.h"
#include "ofApp.h"


//========================================================================
int main() {
    ofSetupOpenGL(1024, 1024, OF_WINDOW);          // <-------- setup the GL context
    ofRunApp(new ofApp());
}
