/*
 * HOC Configurator - UI Handler
 * Copyright (C) Dominatorul, Souldbminer
 */

#pragma once
#include <string>
#include <vector>
#include <functional>
#include <switch.h>

// Forward declarations
class KipHandler;
class ValueEditor;

enum class EditorType {
    TOGGLE,
    FREQUENCY,
    VOLTAGE,
    SLIDER,
    LIST
};

enum class MenuState {
    MAIN,
    GPU,
    CPU,
    RAM,
    MISC,
    ABOUT,
    SETTINGS
};

class UI {
private:
    MenuState currentState;
    int selectedIndex;
    int scrollOffset;
    std::string statusMessage;
    std::string kipPath;
    bool kipLoaded;
    bool autoSave;
    KipHandler* kipHandler;
    ValueEditor* editor;
    
    const int MAX_VISIBLE_ITEMS = 20;
    
    void renderMainMenu();
    void renderGPUMenu();
    void renderCPUMenu();
    void renderRAMMenu();
    void renderMiscMenu();
    void renderAboutMenu();
    void renderSettingsMenu();
    
    void handleMainMenuInput(u64 kDown);
    void handleGPUMenuInput(u64 kDown);
    void handleCPUMenuInput(u64 kDown);
    void handleRAMMenuInput(u64 kDown);
    void handleMiscMenuInput(u64 kDown);
    void handleAboutMenuInput(u64 kDown);
    void handleSettingsMenuInput(u64 kDown);
    
    void drawHeader();
    void drawFooter();
    void drawMenuItem(const std::string& text, bool selected, int y);
    void drawText(const std::string& text, int x, int y);
    
    void showValueEditor(const std::string& title, EditorType type, int currentValue,
                         std::function<void(int)> callback, 
                         const std::vector<std::string>& options = {},
                         int min = 0, int max = 100, int step = 1);
    
public:
    UI();
    ~UI();
    
    void render();
    void handleInput(u64 kDown);
    
    void setStatus(const std::string& msg) { statusMessage = msg; }
    void setKipPath(const std::string& path) { kipPath = path; }
    void setKipLoaded(bool loaded) { kipLoaded = loaded; }
    void setAutoSave(bool enabled) { autoSave = enabled; }
    void setKipHandler(KipHandler* handler) { kipHandler = handler; }
    
    std::string getStatus() const { return statusMessage; }
    std::string getKipPath() const { return kipPath; }
    bool isKipLoaded() const { return kipLoaded; }
    bool isAutoSaveEnabled() const { return autoSave; }
};