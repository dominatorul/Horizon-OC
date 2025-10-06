/*
 * HOC Configurator - Value Editor
 * Copyright (C) Dominatorul, Souldbminer
 */

#pragma once
#include <string>
#include <vector>
#include <functional>
#include <switch.h>
#include "ui.hpp"  // This includes EditorType

class KipHandler;

struct EditorConfig {
    std::string title;
    EditorType type;
    int currentValue;
    int minValue;
    int maxValue;
    int step;
    std::vector<std::string> options;
    std::function<void(int)> onValueChange;
};

class ValueEditor {
private:
    EditorConfig config;
    int selectedValue;
    bool active;
    
public:
    ValueEditor();
    
    void show(const EditorConfig& cfg);
    void hide();
    bool isActive() const { return active; }
    
    void handleInput(u64 kDown);
    void render();
    
    int getSelectedValue() const { return selectedValue; }
};