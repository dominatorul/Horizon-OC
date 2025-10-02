#pragma once
#include "../../ipc.h"
#include "base_menu_gui.h"
#include <unordered_map>
#include <string>

class MiscGui : public BaseMenuGui
{
    public:
        MiscGui();
        ~MiscGui();

        void listUI() override;
        void refresh() override;
    protected:
        SysClkConfigValueList* configList;
        
        std::map<SysClkConfigValue, tsl::elm::ToggleListItem*> configToggles;
        void addConfigToggle(SysClkConfigValue, const char*);
        void updateConfigToggles();
        
        tsl::elm::ToggleListItem* enabledToggle;
        
        u8 frameCounter = 60;
};