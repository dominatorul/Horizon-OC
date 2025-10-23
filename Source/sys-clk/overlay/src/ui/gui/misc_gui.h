#pragma once
#include "../../ipc.h"
#include "base_menu_gui.h"
#include <unordered_map>
#include <string>
#include <vector>
#include "freq_choice_gui.h"
class MiscGui : public BaseMenuGui
{
public:
    MiscGui();
    ~MiscGui();

    void listUI() override;
    void refresh() override;

protected:
    std::map<SysClkConfigValue, tsl::elm::ListItem*> configButtons;
    SysClkConfigValueList* configList;
    std::map<SysClkConfigValue, tsl::elm::ToggleListItem*> configToggles;
    std::map<SysClkConfigValue, std::tuple<tsl::elm::TrackBar*, tsl::elm::ListItem*, std::vector<uint64_t>>> configTrackbars;
    void addConfigToggle(SysClkConfigValue configVal, const char* altName);
    void addConfigButton(SysClkConfigValue configVal, const char* altName, SysClkModule module);

    void updateConfigToggles();

    tsl::elm::ToggleListItem* enabledToggle;
    u8 frameCounter = 60;
};
