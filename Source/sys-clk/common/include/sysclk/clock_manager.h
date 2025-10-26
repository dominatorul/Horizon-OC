/*
 * --------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <p-sam@d3vs.net>, <natinusala@gmail.com>, <m4x@m4xw.net>
 * wrote this file. As long as you retain this notice you can do whatever you
 * want with this stuff. If you meet any of us some day, and you think this
 * stuff is worth it, you can buy us a beer in return.  - The sys-clk authors
 * --------------------------------------------------------------------------
 */

#pragma once

#include <stdint.h>
#include "board.h"

typedef struct
{
    uint8_t enabled;
    uint64_t applicationId;
    SysClkProfile profile;
    uint32_t freqs[SysClkModule_EnumMax];
    uint32_t realFreqs[SysClkModule_EnumMax];
    uint32_t overrideFreqs[SysClkModule_EnumMax];
    uint32_t temps[SysClkThermalSensor_EnumMax];
    int32_t power[SysClkPowerSensor_EnumMax];
    uint32_t ramLoad[SysClkRamLoad_EnumMax];
    uint32_t perfConfId;
} SysClkContext;

typedef struct
{
    union {
        uint32_t mhz[(uint32_t)SysClkProfile_EnumMax * (uint32_t)SysClkModule_EnumMax];
        uint32_t mhzMap[(uint32_t)SysClkProfile_EnumMax][(uint32_t)SysClkModule_EnumMax];
    };
} SysClkTitleProfileList;

#define SYSCLK_FREQ_LIST_MAX 32
#define SYSCLK_GPU_BOOST_HZ 76800000
#define SYSCLK_CPU_BOOST_HZ 1785000000