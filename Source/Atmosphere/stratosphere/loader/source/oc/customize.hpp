/*
 * Copyright (C) Switch-OC-Suite
 *
 * Copyright (c) 2023 hanai3Bi
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms and conditions of the GNU General Public License,
 * version 2, as published by the Free Software Foundation.
 *
 * This program is distributed in the hope it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
 * more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#pragma once

#define CUST_REV 11

#include "oc_common.hpp"
#include "pcv/pcv_common.hpp"

namespace ams::ldr::oc {

#include "mtc_timing_table.hpp"

enum MtcConfig: u32 {
    AUTO_ADJ_ALL = 0,
    CUSTOM_ADJ_ALL = 1,
    NO_ADJ_ALL = 2,
    
    CUSTOMIZED_ALL = 4,
};

using CustomizeCpuDvfsTable = pcv::cvb_entry_t[pcv::DvfsTableEntryLimit];
using CustomizeGpuDvfsTable = pcv::cvb_entry_t[pcv::DvfsTableEntryLimit];
static_assert(sizeof(CustomizeCpuDvfsTable) == sizeof(CustomizeGpuDvfsTable));
static_assert(sizeof(CustomizeCpuDvfsTable) == sizeof(pcv::cvb_entry_t) * pcv::DvfsTableEntryLimit);

constexpr uint32_t ERISTA_MTC_MAGIC = 0x43544D45; // EMTC
constexpr uint32_t MARIKO_MTC_MAGIC = 0x43544D4D; // MMTC

typedef struct CustomizeTable {
    u8  cust[4] = {'C', 'U', 'S', 'T'};
    u32 custRev = CUST_REV;
    u32 mtcConf;
    u32 commonCpuBoostClock;
    u32 commonEmcMemVolt;
    u32 eristaCpuMaxVolt;
    u32 eristaEmcMaxClock;
    u32 marikoCpuMaxVolt;
    u32 marikoEmcMaxClock;
    u32 marikoEmcVddqVolt;
    u32 marikoCpuUV;
    u32 marikoGpuUV;
    u32 commonGpuVoltOffset;
    // advanced config
    u32 marikoEmcDvbShift;
    //
    const uint32_t BL;
    const uint32_t tRFCpb;
    const uint32_t tRFCab;
    const uint32_t tRAS;
    const uint32_t tRPpb;
    const uint32_t tRPab;
    const uint32_t tRC;

    const double tDQSCK_min;
    const double tDQSCK_max;
    const double tWPRE;
    const double tRPST;
    const double tDQSS_max;
    const double tDQS2DQ_max;
    const double tDQSQ;

    const uint32_t tWTR;
    const double tRTP;
    const uint32_t tWR;
    const double tR2REF;

    const uint32_t tRCD;
    const double tRRD;
    const uint32_t tREFpb;

    const double tXP;
    const double tCMDCKE;

    const uint32_t tMRWCKEL;

    const double tCKELCS;
    const double tCSCKEH;
    const double tXSR;
    const double tCKE;

    const uint32_t tSR;
    const uint32_t tFAW;

    const double tCKCKEH;
    const double tCK_avg;

    const uint32_t WL;
    const uint32_t RL;
    u32 marikoGpuVoltArray[17];
    CustomizeCpuDvfsTable eristaCpuDvfsTable;
    CustomizeCpuDvfsTable marikoCpuDvfsTable;
    CustomizeCpuDvfsTable marikoCpuDvfsTableSLT;
    CustomizeGpuDvfsTable eristaGpuDvfsTable;
    CustomizeGpuDvfsTable marikoGpuDvfsTable;
    CustomizeGpuDvfsTable marikoGpuDvfsTableSLT;
    CustomizeGpuDvfsTable marikoGpuDvfsTableHiOPT;
    //EristaMtcTable* eristaMtcTable;
    //MarikoMtcTable* marikoMtcTable;
} CustomizeTable;
//static_assert(sizeof(CustomizeTable) == sizeof(u8) * 4 + sizeof(u32) * 10 + sizeof(CustomizeCpuDvfsTable) * 5 + sizeof(void*) * 2);
//static_assert(sizeof(CustomizeTable) == 7000);

extern volatile CustomizeTable C;

//extern volatile EristaMtcTable EristaMtcTablePlaceholder;
//extern volatile MarikoMtcTable MarikoMtcTablePlaceholder;
}