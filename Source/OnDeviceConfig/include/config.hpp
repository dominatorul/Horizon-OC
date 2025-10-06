/*
 * HOC Configurator - Configuration Handler
 * Copyright (C) Dominatorul, Souldbminer
 */

#pragma once
#include <string>

class Config {
public:
    std::string kipPath;
    bool autoSave;
    
    Config();
    
    bool loadConfig();
    bool saveConfig();
    bool checkKipExists();
    bool checkAtmosphereExists();
};
