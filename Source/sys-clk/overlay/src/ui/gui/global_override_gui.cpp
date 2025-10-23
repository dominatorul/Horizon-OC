/*
 * --------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <p-sam@d3vs.net>, <natinusala@gmail.com>, <m4x@m4xw.net>
 * wrote this file. As long as you retain this notice you can do whatever you
 * want with this stuff. If you meet any of us some day, and you think this
 * stuff is worth it, you can buy us a beer in return.  - The sys-clk authors
 * --------------------------------------------------------------------------
 */

#include "global_override_gui.h"

#include "fatal_gui.h"
#include "../format.h"

GlobalOverrideGui::GlobalOverrideGui()
{
    for(std::uint16_t m = 0; m < SysClkModule_EnumMax; m++)
    {
        this->listItems[m] = nullptr;
        this->listHz[m] = 0;
    }
}

void GlobalOverrideGui::openFreqChoiceGui(SysClkModule module)
{
    std::uint32_t hzList[SYSCLK_FREQ_LIST_MAX];
    std::uint32_t hzCount;
    Result rc = sysclkIpcGetFreqList(module, &hzList[0], SYSCLK_FREQ_LIST_MAX, &hzCount);
    if(R_FAILED(rc))
    {
        FatalGui::openWithResultCode("sysclkIpcGetFreqList", rc);
        return;
    }
    tsl::changeTo<FreqChoiceGui>(this->context->overrideFreqs[module], hzList, hzCount, module, [this, module](std::uint32_t hz) {
        Result rc = sysclkIpcSetOverride(module, hz);
        if(R_FAILED(rc))
        {
            FatalGui::openWithResultCode("sysclkIpcSetOverride", rc);
            return false;
        }

        this->lastContextUpdate = armGetSystemTick();
        this->context->overrideFreqs[module] = hz;

        return true;
    }, true);
}

void GlobalOverrideGui::addModuleListItem(SysClkModule module)
{
    tsl::elm::ListItem* listItem = new tsl::elm::ListItem(sysclkFormatModule(module, true));
    listItem->setValue(formatListFreqMHz(0));
    listItem->setClickListener([this, module](u64 keys) {
        if((keys & HidNpadButton_A) == HidNpadButton_A)
        {
            this->openFreqChoiceGui(module);
            return true;
        }
        else if((keys & HidNpadButton_Y) == HidNpadButton_Y)
        {
            // Reset override to "Do not override" (0 Hz)
            Result rc = sysclkIpcSetOverride(module, 0);
            if(R_FAILED(rc))
            {
                FatalGui::openWithResultCode("sysclkIpcSetOverride", rc);
                return false;
            }
            
            // Update context and tracking variables
            this->lastContextUpdate = armGetSystemTick();
            this->context->overrideFreqs[module] = 0;
            this->listHz[module] = 0;
            
            // Update display
            this->listItems[module]->setValue(formatListFreqHz(0));
            
            return true;
        }
        return false;
    });
    this->listElement->addItem(listItem);
    this->listItems[module] = listItem;
}

void GlobalOverrideGui::listUI()
{
    this->listElement->addItem(new tsl::elm::CategoryHeader("Temporary Overrides " + ult::DIVIDER_SYMBOL + "  Reset"));
    this->addModuleListItem(SysClkModule_CPU);
    this->addModuleListItem(SysClkModule_GPU);
    this->addModuleListItem(SysClkModule_MEM);
}

void GlobalOverrideGui::refresh()
{
    BaseMenuGui::refresh();
    if(this->context)
    {
        for(std::uint16_t m = 0; m < SysClkModule_EnumMax; m++)
        {
            if(this->listItems[m] != nullptr && this->listHz[m] != this->context->overrideFreqs[m])
            {
                this->listItems[m]->setValue(formatListFreqHz(this->context->overrideFreqs[m]));
                this->listHz[m] = this->context->overrideFreqs[m];
            }
        }
    }
}
