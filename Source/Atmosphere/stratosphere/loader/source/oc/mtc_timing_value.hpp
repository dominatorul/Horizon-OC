/*
 * Copyright (C) hanai3bi (meha) and Souldbminer
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

#include "oc_common.hpp"

namespace ams::ldr::oc {
    #define MAX(A, B)   std::max(A, B)
    #define MIN(A, B)   std::min(A, B)
    #define CEIL(A)     std::ceil(A)
    #define FLOOR(A)    std::floor(A)
    
    // p78 The first valid data is available RL × t CK + t DQSCK + t DQSQ
    //const u32 QUSE = RL + CEIL(C.tDQSCK_min/tCK_avg + C.tDQSQ);

    namespace pcv::erista {
        // tCK_avg (average clock period) in ns
        const double tCK_avg = 1000'000. / C.eristaEmcMaxClock;

        // Write Latency
        const u32 WL = 14 + C.latency;
        // Read Latency
        const u32 RL = 32 + C.latency;

        // minimum number of cycles from any read command to any write command, irrespective of bank
        const u32 R2W = CEIL (RL + CEIL(C.tDQSCK_max/tCK_avg) + C.BL/2 - WL + C.tWPRE + FLOOR(C.tRPST)) + 6;
        
        // Delay Time From WRITE-to-READ
        const u32 W2R = WL + C.BL/2 + 1 + CEIL(C.tWTR/tCK_avg) - 6;
        
        // write-to-precharge time for commands to the same bank in cycles
        const u32 WTP = WL + C.BL/2 + 1 + CEIL(C.tWR/tCK_avg) - 8;
        
        // #_of_rows per die for 8Gb density
        const u32 numOfRows = 65536;
        // {REFRESH, REFRESH_LO} = max[(tREF/#_of_rows) / (emc_clk_period) - 64, (tREF/#_of_rows) / (emc_clk_period) * 97%]
        // emc_clk_period = dram_clk / 2;
        // 1600 MHz: 5894, but N' set to 6176 (~4.8% margin)
        const u32 REFRESH = MIN((u32)65472, u32(std::ceil((double(C.tREFpb) * C.eristaEmcMaxClock / numOfRows * 1.048 / 2 - 64))) / 4 * 4);
        const u32 REFBW = MIN((u32)65536, REFRESH+64);
        
        // Write With Auto Precharge to to Power-Down Entry
        const u32 WTPDEN = WTP + 1 + CEIL(C.tDQSS_max/tCK_avg) + CEIL(C.tDQS2DQ_max/tCK_avg) + 6;
        
        // Additional time after t XP hasexpired until the MRR commandmay be issued
        const double tMRRI = C.tRCD + 3 * tCK_avg;
        
        // tPDEX2MRR (timing delay from exiting powerdown mode to MRR command) in ns
        const double tPDEX2MRR = C.tXP + tMRRI;
    }
    namespace pcv::mariko {
        // tCK_avg (average clock period) in ns
        const double tCK_avg = 1000'000. / C.marikoEmcMaxClock;
        // Write Latency
        const u32 WL = 14 - 2*C.latency;
        // Read Latency
        const u32 RL = 32 - 4*C.latency;

        // minimum number of cycles from any read command to any write command, irrespective of bank
        const u32 R2W = CEIL (RL + CEIL(C.tDQSCK_max/tCK_avg) + C.BL/2 - WL + C.tWPRE + FLOOR(C.tRPST));
        
        // Delay Time From WRITE-to-READ
        const u32 W2R = WL + C.BL/2 + 1 + CEIL(C.tWTR/tCK_avg);
        
        // write-to-precharge time for commands to the same bank in cycles
        const u32 WTP = WL + C.BL/2 + 1 + CEIL(C.tWR/tCK_avg);
        
        // Read-To-MRW delay
        const u32 RTM = RL + C.BL/2 + CEIL(C.tDQSCK_max/tCK_avg) + FLOOR(C.tRPST) + CEIL(7.5/tCK_avg);
        
        // Write-To-MRW/MRR delay
        const u32 WTM = WL + 1 + C.BL/2 + CEIL(7.5/tCK_avg);
        
        // Read With AP-To-MRW/MRR delay
        const u32 RATM = RTM + CEIL(C.tRTP/ 1000/tCK_avg) - 8;
        
        // Write With AP-To-MRW/MRR delay
        const u32 WATM = WTM + CEIL(C.tWR/tCK_avg);
        
        // #_of_rows per die for 8Gb density
        const u32 numOfRows = 65536;
        // {REFRESH, REFRESH_LO} = max[(tREF/#_of_rows) / (emc_clk_period) - 64, (tREF/#_of_rows) / (emc_clk_period) * 97%]
        // emc_clk_period = dram_clk / 2;
        // 1600 MHz: 5894, but N' set to 6176 (~4.8% margin)
        const u32 REFRESH = MIN((u32)65472, u32(std::ceil((double(C.tREFpb) * C.marikoEmcMaxClock / numOfRows * 1.048 / 2 - 64))) / 4 * 4);
        const u32 REFBW = MIN((u32)65536, REFRESH+64);
        
        // Write With Auto Precharge to to Power-Down Entry
        const u32 WTPDEN = WTP + 1 + CEIL(C.tDQSS_max/tCK_avg) + CEIL(C.tDQS2DQ_max/tCK_avg) + 6;
        
        // Additional time after t XP hasexpired until the MRR commandmay be issued
        const double tMRRI = C.tRCD + 3 * tCK_avg;
        
        // tPDEX2MRR (timing delay from exiting powerdown mode to MRR command) in ns
        const double tPDEX2MRR = C.tXP + tMRRI;
    }
}
