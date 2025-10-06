/*
 * HOC Configurator - Configuration Implementation
 * Copyright (C) Dominatorul, Souldbminer
 */

#include "config.hpp"
#include <fstream>
#include <sys/stat.h>

Config::Config() {
    kipPath = "sdmc:/atmosphere/kips/loader.kip";
    autoSave = false;
}

bool Config::loadConfig() {
    std::ifstream file("sdmc:/config/hoc-configurator/config.ini");
    if (!file.is_open()) {
        return false;
    }
    
    std::string line;
    while (std::getline(file, line)) {
        if (line.find("kip_path=") == 0) {
            kipPath = line.substr(9);
        } else if (line.find("auto_save=") == 0) {
            autoSave = (line.substr(10) == "1");
        }
    }
    
    file.close();
    return true;
}

bool Config::saveConfig() {
    // Create directory if it doesn't exist
    mkdir("sdmc:/config", 0777);
    mkdir("sdmc:/config/hoc-configurator", 0777);
    
    std::ofstream file("sdmc:/config/hoc-configurator/config.ini");
    if (!file.is_open()) {
        return false;
    }
    
    file << "kip_path=" << kipPath << "\n";
    file << "auto_save=" << (autoSave ? "1" : "0") << "\n";
    
    file.close();
    return true;
}

bool Config::checkKipExists() {
    struct stat buffer;
    return (stat(kipPath.c_str(), &buffer) == 0);
}

bool Config::checkAtmosphereExists() {
    struct stat buffer;
    return (stat("sdmc:/atmosphere", &buffer) == 0);
}
