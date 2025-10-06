/*
 * HOC Configurator - Value Editor Implementation
 * Copyright (C) Dominatorul, Souldbminer
 */

#include "value_editor.hpp"
#include <cstdio>
#include <algorithm>

ValueEditor::ValueEditor() : selectedValue(0), active(false) {}

void ValueEditor::show(const EditorConfig& cfg) {
    config = cfg;
    selectedValue = cfg.currentValue;
    active = true;
}

void ValueEditor::hide() {
    active = false;
}

void ValueEditor::handleInput(u64 kDown) {
    if (!active) return;
    
    if (kDown & HidNpadButton_B) {
        hide();
        return;
    }
    
    if (kDown & HidNpadButton_A) {
        if (config.onValueChange) {
            config.onValueChange(selectedValue);
        }
        hide();
        return;
    }
    
    switch (config.type) {
        case EditorType::TOGGLE:
            if (kDown & (HidNpadButton_Left | HidNpadButton_Right | 
                         HidNpadButton_Up | HidNpadButton_Down)) {
                selectedValue = !selectedValue;
            }
            break;
            
        case EditorType::LIST:
        case EditorType::FREQUENCY:
        case EditorType::VOLTAGE:
            if (kDown & HidNpadButton_Down) {
                selectedValue++;
                if (selectedValue >= (int)config.options.size()) {
                    selectedValue = 0;
                }
            }
            if (kDown & HidNpadButton_Up) {
                selectedValue--;
                if (selectedValue < 0) {
                    selectedValue = config.options.size() - 1;
                }
            }
            break;
            
        case EditorType::SLIDER:
            if (kDown & HidNpadButton_Right) {
                selectedValue = std::min(selectedValue + config.step, config.maxValue);
            }
            if (kDown & HidNpadButton_Left) {
                selectedValue = std::max(selectedValue - config.step, config.minValue);
            }
            if (kDown & HidNpadButton_Down) {
                selectedValue = std::max(selectedValue - config.step * 5, config.minValue);
            }
            if (kDown & HidNpadButton_Up) {
                selectedValue = std::min(selectedValue + config.step * 5, config.maxValue);
            }
            break;
    }
}

void ValueEditor::render() {
    if (!active) return;
    
    // Draw editor overlay
    printf("\x1b[2J\x1b[1;1H");
    
    // Header
    printf("\x1b[47;30m");
    printf("===============================================================================\n");
    printf(" %s%-73s \n", config.title.c_str(), "");
    printf("===============================================================================\n");
    printf("\x1b[0m");
    
    printf("\x1b[10;1H");
    printf("+- Value Editor ----------------------------------------------------------------+\n");
    printf("|                                                                              |\n");
    
    // Display current value based on type
    switch (config.type) {
        case EditorType::TOGGLE:
            printf("|  Current: %-66s |\n", selectedValue ? "Enabled (1)" : "Disabled (0)");
            printf("|                                                                              |\n");
            printf("|  Use D-Pad to toggle                                                         |\n");
            break;
            
        case EditorType::LIST:
        case EditorType::FREQUENCY:
        case EditorType::VOLTAGE:
            if (selectedValue >= 0 && selectedValue < (int)config.options.size()) {
                printf("|  Current: %-66s |\n", config.options[selectedValue].c_str());
            }
            printf("|                                                                              |\n");
            printf("|  Use Up/Down to change value                                                 |\n");
            break;
            
        case EditorType::SLIDER:
            printf("|  Current: %-66d |\n", selectedValue);
            printf("|                                                                              |\n");
            printf("|  Left/Right: +/-%d    Up/Down: +/-%d                                   |\n", 
                   config.step, config.step * 5);
            printf("|  Range: %d - %d%-56s|\n", config.minValue, config.maxValue, "");
            break;
    }
    
    printf("|                                                                              |\n");
    printf("+------------------------------------------------------------------------------+\n");
    
    // Footer
    printf("\x1b[42;1H");
    printf("\x1b[47;30m");
    printf("===============================================================================\n");
    printf(" [A] Confirm  [B] Cancel                                                       \n");
    printf("===============================================================================\n");
    printf("\x1b[0m");
}
