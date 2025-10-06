/*
 * HOC Configurator - Nintendo Switch Homebrew
 * Copyright (C) Dominatorul, Souldbminer
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms and conditions of the GNU General Public License,
 * version 2, as published by the Free Software Foundation.
 */

#include <switch.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <algorithm>
#include "kip_handler.hpp"
#include "ui.hpp"
#include "config.hpp"
#include "defaults.hpp"

int main(int argc, char* argv[]) {
    // Initialize services
    socketInitializeDefault();
    nxlinkStdio();
    
    consoleInit(NULL);
    
    // Configure input
    padConfigureInput(1, HidNpadStyleSet_NpadStandard);
    PadState pad;
    padInitializeDefault(&pad);
    
    // Initialize configuration
    Config config;
    config.loadConfig();
    
    // Initialize KIP handler
    KipHandler* kipHandler = new KipHandler(config.kipPath);
    
    // Initialize UI
    UI ui;
    ui.setKipPath(config.kipPath);
    ui.setKipHandler(kipHandler);
    ui.setAutoSave(config.autoSave);
    
    // Check if KIP exists and load it
    if (config.checkKipExists()) {
        if (kipHandler->readKip()) {
            ui.setStatus("KIP loaded successfully from " + config.kipPath);
            ui.setKipLoaded(true);
        } else {
            ui.setStatus("ERROR: Failed to parse KIP file!");
            ui.setKipLoaded(false);
        }
    } else if (config.checkAtmosphereExists()) {
        ui.setStatus("Atmosphere found, but KIP not found at: " + config.kipPath);
        ui.setKipLoaded(false);
    } else {
        ui.setStatus("ERROR: Atmosphere not detected! Is your SD card mounted?");
        ui.setKipLoaded(false);
    }
    
    bool running = true;
    u64 kDownOld = 0;
    int frameCounter = 0;
    const int FRAME_DELAY = 3; // Add input delay for better responsiveness
    
    while (running && appletMainLoop()) {
        padUpdate(&pad);
        u64 kDown = padGetButtonsDown(&pad);
        
        // Exit on Plus button
        if (kDown & HidNpadButton_Plus) {
            running = false;
            break;
        }
        
        // Process input with debouncing and frame delay
        if (kDown && kDown != kDownOld && frameCounter >= FRAME_DELAY) {
            ui.handleInput(kDown);
            frameCounter = 0;
        }
        
        // Render UI
        ui.render();
        consoleUpdate(NULL);
        
        kDownOld = kDown;
        frameCounter++;
        
        // Frame limiter - 30 FPS
        svcSleepThread(33333333); // ~33ms
    }
    
    // Save config before exit
    config.autoSave = ui.isAutoSaveEnabled();
    config.kipPath = ui.getKipPath();
    config.saveConfig();
    
    // Cleanup
    delete kipHandler;
    
    consoleExit(NULL);
    socketExit();
    
    return 0;
}