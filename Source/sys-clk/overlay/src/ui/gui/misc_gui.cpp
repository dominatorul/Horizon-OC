#include "misc_gui.h"
#include "fatal_gui.h"
#include "../format.h"
#include <cstdio>
#include <cstring>
//#include <sstream>

MiscGui::MiscGui()
{
    this->configList = new SysClkConfigValueList {};
}

MiscGui::~MiscGui()
{
    delete this->configList;
    this->configToggles.clear();
}

void MiscGui::addConfigToggle(SysClkConfigValue configVal, const char* altName = nullptr) {
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

void MiscGui::updateConfigToggles() {
    for (const auto& [value, toggle] : this->configToggles) {
        if (toggle != nullptr)
            toggle->setState(this->configList->values[value]);
    }
}

void MiscGui::listUI()
{
    this->listElement->addItem(new tsl::elm::CategoryHeader("Options"));
    addConfigToggle(HocClkConfigValue_UncappedClocks);
    addConfigToggle(HocClkConfigValue_OverwriteBoostMode);
//  this->listElement->addItem(new tsl::elm::CategoryHeader("Experemental"));
    addConfigToggle(HocClkConfigValue_SyncReverseNXMode);
    addConfigToggle(HocClkConfigValue_ReadRealTemps);
}

void MiscGui::refresh() {
    BaseMenuGui::refresh();

    // Update the enabled toggle state
    if (this->context && ++frameCounter >= 60)
    {
        frameCounter = 0;
        sysclkIpcGetConfigValues(this->configList);
        updateConfigToggles();
    }

}
