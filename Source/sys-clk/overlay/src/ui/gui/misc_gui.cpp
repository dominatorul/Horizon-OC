#include "misc_gui.h"
#include "fatal_gui.h"
#include "../format.h"
#include <cstdio>
#include <cstring>
#include <vector>

MiscGui::MiscGui()
{
    this->configList = new SysClkConfigValueList {};
}

MiscGui::~MiscGui()
{
    delete this->configList;
    this->configToggles.clear();
    this->configTrackbars.clear();
}

void MiscGui::addConfigToggle(SysClkConfigValue configVal, const char* altName) {
    const char* configName = altName ? altName : sysclkFormatConfigValue(configVal, true);
    tsl::elm::ToggleListItem* toggle = new tsl::elm::ToggleListItem(configName, this->configList->values[configVal]);
    toggle->setStateChangedListener([this, configVal](bool state) {
        this->configList->values[configVal] = uint64_t(state);
        Result rc = sysclkIpcSetConfigValues(this->configList);
        if (R_FAILED(rc))
            FatalGui::openWithResultCode("sysclkIpcSetConfigValues", rc);
        this->lastContextUpdate = armGetSystemTick();
    });
    this->listElement->addItem(toggle);
    this->configToggles[configVal] = toggle;
}

void MiscGui::addConfigButton(SysClkConfigValue configVal, const char* altName, SysClkModule module) {
    const char* configName = altName ? altName : sysclkFormatConfigValue(configVal, true);
    // Create button list item
    tsl::elm::ListItem* listItem = new tsl::elm::ListItem(configName);

    // Set initial label text (MHz)
    uint64_t currentMHz = this->configList->values[configVal];
    char valueText[32];
    snprintf(valueText, sizeof(valueText), "%lu MHz", currentMHz);
    listItem->setValue(valueText);

    // Click listener to open FreqChoiceGui
    listItem->setClickListener([this, configVal, module](u64 keys) {
        if ((keys & HidNpadButton_A) == 0)
            return false;
    
        std::uint32_t hzList[SYSCLK_FREQ_LIST_MAX];
        std::uint32_t hzCount;
    
        // Get frequency list from sys-clk
        Result rc = sysclkIpcGetFreqList(module, hzList, SYSCLK_FREQ_LIST_MAX, &hzCount);
        if (R_FAILED(rc)) {
            FatalGui::openWithResultCode("sysclkIpcGetFreqList", rc);
            return false;
        }
    
        std::uint32_t currentHz = this->configList->values[configVal] * 1'000'000;
    
        tsl::changeTo<FreqChoiceGui>(
            currentHz,
            hzList,
            hzCount,
            module,
            [this, configVal](std::uint32_t hz) {
                // Convert to MHz for config storage
                uint64_t mhz = hz / 1'000'000;
                this->configList->values[configVal] = mhz;
        
                // Push new config value
                Result rc = sysclkIpcSetConfigValues(this->configList);
                if (R_FAILED(rc)) {
                    FatalGui::openWithResultCode("sysclkIpcSetConfigValues", rc);
                    return false;
                }
        
                this->lastContextUpdate = armGetSystemTick();
                return true;
            },
            false
        );
        
    
        return true;
    });

    // Add to UI and internal map for refresh updates
    this->listElement->addItem(listItem);
    this->configButtons[configVal] = listItem;
}



void MiscGui::updateConfigToggles() {
    for (const auto& [value, toggle] : this->configToggles) {
        if (toggle != nullptr)
            toggle->setState(this->configList->values[value]);
    }
}

void MiscGui::listUI()
{
    this->listElement->addItem(new tsl::elm::CategoryHeader("Config"));
    addConfigToggle(HocClkConfigValue_UncappedClocks, nullptr);
    addConfigToggle(HocClkConfigValue_OverwriteBoostMode, nullptr);

    addConfigButton(HocClkConfigValue_MaxCpuClock, nullptr, SysClkModule_CPU);
    addConfigButton(HocClkConfigValue_MaxGpuClock, nullptr, SysClkModule_GPU);
}

void MiscGui::refresh() {
    BaseMenuGui::refresh();

    if (this->context && ++frameCounter >= 60) {
        frameCounter = 0;

        sysclkIpcGetConfigValues(this->configList);

        updateConfigToggles();

        for (const auto& [configVal, button] : this->configButtons) {
            uint64_t mhz = this->configList->values[configVal];
            char valueText[32];
            snprintf(valueText, sizeof(valueText), "%lu MHz", mhz);
            button->setValue(valueText);
        }
    }
}
