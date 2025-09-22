/*
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
 *
 * from GCC preprocessor output
 */



 #pragma once

 #include "oc_common.hpp"
 
 namespace ams::ldr::oc {
     #define MAX(A, B)   std::max(A, B)
     #define MIN(A, B)   std::min(A, B)
     #define CEIL(A)     std::ceil(A)
     #define FLOOR(A)    std::floor(A)
 
     //Preset One
     const std::array<u32, 8> tRCD_values  = {18, 17, 16, 15, 14, 13, 12, 11};
     const std::array<u32, 8> tRP_values   = {18, 17, 16, 15, 14, 13, 12, 11};
     const std::array<u32, 10> tRAS_values = {42, 36, 34, 32, 30, 28, 26, 24, 22, 20};
     
     // Preset Two
     const std::array<double, 8> tRRD_values = {10, 7.5, 6, 5, 4, 3, 2, 1};
     const std::array<double, 5> tFAW_values = {40, 30, 24, 16, 12};
     
     // Preset Three
     const std::array<u32, 6> tWR_values     = {18, 15, 15, 12, 12, 8}; // TODO: identify what exactly eos tRTW even is (is it even real?)
     const std::array<double, 6> tRTP_values = {7.5, 7.5, 6, 6, 4, 4};
     
     // Preset Four
     const std::array<u32, 6> tRFC_values = {140, 120, 100, 80, 70, 60};
     
     // Preset Five
     const std::array<u32, 10> tWTR_values = {10, 9, 8, 7, 6, 5, 4, 3, 2, 1};
     
     // Preset Six
     const std::array<u32, 6> tREFpb_values = {488, 976, 1952, 3256, 9999, 9999};
     
     // const u32 TIMING_PRESET_ONE = C.ramTimingPresetOne;
     // const u32 TIMING_PRESET_TWO = C.ramTimingPresetTwo;
     const u32 TIMING_PRESET_THREE = 0;
     // const u32 TIMING_PRESET_FOUR = C.ramTimingPresetFour;
     // const u32 TIMING_PRESET_FIVE = C.ramTimingPresetFive;
     // const u32 TIMING_PRESET_SIX = C.ramTimingPresetSix;
     // const u32 TIMING_PRESET_SEVEN = C.ramTimingPresetSeven;
 
     // Burst Length
     const u32 BL = 16;
 
     // tRFCpb (refresh cycle time per bank) in ns for 8Gb density
     const u32 tRFCpb = !C.t5_tRFC ? 140 : tRFC_values[C.t5_tRFC-1];
     
     // tRFCab (refresh cycle time all banks) in ns for 8Gb density
     const u32 tRFCab = !C.t5_tRFC ? 280 : 2*tRFCpb;
     
     // tRAS (row active time) in ns
     const u32 tRAS = !C.t3_tRAS ? 42 : tRAS_values[C.t3_tRAS-1];
     
     // tRPpb (row precharge time per bank) in ns
     const u32 tRPpb = !C.t2_tRP ? 18 : tRP_values[C.t2_tRP-1];
     
     // tRPab (row precharge time all banks) in ns
     const u32 tRPab = !C.t2_tRP ? 21 : tRPpb + 3;
     
     // tRC (ACTIVATE-ACTIVATE command period same bank) in ns
     const u32 tRC = tRPpb + tRAS;
     
     // DQS output access time from CK_t/CK_c
     const double tDQSCK_min = 1.5;
     // DQS output access time from CK_t/CK_c
     const double tDQSCK_max = 3.5;
     // Write preamble (tCK)
     const double tWPRE = 1.8;
     // Read postamble (tCK)
     const double tRPST = 0.4;
     // WRITE command to first DQS transition(max) (tCK)
     const double tDQSS_max = 1.25;
     // DQ-to-DQS offset(max) (ns)
     const double tDQS2DQ_max = 0.8;
     // DQS_t, DQS_c to DQ skew total, per group, per access (DBI Disabled)
     const double tDQSQ = 0.18;
 
     // Write-to-Read delay
     const u32 tWTR = !C.t7_tWTR ? 10 : tWTR_values[C.t7_tWTR-1];
     
     // Internal READ-to-PRE-CHARGE command delay in ns
     const double tRTP = !TIMING_PRESET_THREE ? 7.5 : tRTP_values[TIMING_PRESET_THREE-1];
     
     // write recovery time
     const u32 tWR = !TIMING_PRESET_THREE ? 18 : tWR_values[TIMING_PRESET_THREE-1];
     
     // Read to refresh delay
     const u32 tR2REF = tRTP + tRPpb;
     
     // tRCD (RAS-CAS delay) in ns
     const u32 tRCD = !C.t1_tRCD ? 18 : tRCD_values[C.t1_tRCD-1];
     
     // tRRD (Active bank-A to Active bank-B) in ns
     const double tRRD = !C.t4_tRRD ? 10. : tRRD_values[C.t4_tRRD-1];
     
     // tREFpb (average refresh interval per bank) in ns for 8Gb density
     const u32 tREFpb = !C.t8_tREFI ? 488 : tREFpb_values[C.t8_tREFI-1];
     // tREFab (average refresh interval all 8 banks) in ns for 8Gb density
     // const u32 tREFab = tREFpb * 8;
     
     // tPDEX2WR, tPDEX2RD (timing delay from exiting powerdown mode to a write/read command) in ns
     // const u32 tPDEX2 = 10;
     // Exit power-down to next valid command delay
     const double tXP = 10;
     
     // Delay from valid command to CKE input LOW in ns
     const double tCMDCKE = 1.75;
     
     // tACT2PDEN (timing delay from an activate, MRS or EMRS command to power-down entry) in ns
     // Valid clock and CS requirement after CKE input LOW after MRW command
     const u32 tMRWCKEL = 14;
     
     // Valid CS requirement after CKE input LOW
     const double tCKELCS = 5;
     
     // Valid CS requirement before CKE input HIGH
     const double tCSCKEH = 1.75;
     
     // tXSR (SELF REFRESH exit to next valid command delay) in ns
     const double tXSR = tRFCab + 7.5;
     
     // tCKE (minimum pulse width(HIGH and LOW pulse width)) in ns
     const double tCKE = 7.5;
     
     // Minimum self refresh time (entry to exit)
     const u32 tSR = 15;
     
     // tFAW (Four-bank Activate Window) in ns
     const u32 tFAW = 40;// !TIMING_PRESET_TWO ? 40 : tFAW_values[TIMING_PRESET_TWO-1]; TOGO
     
     // Valid Clock requirement before CKE Input HIGH in ns
     const double tCKCKEH = 1.75;
     
     // p78 The first valid data is available RL × t CK + t DQSCK + t DQSQ
     //const u32 QUSE = RL + CEIL(tDQSCK_min/tCK_avg + tDQSQ);
 
     namespace pcv::erista {
         // tCK_avg (average clock period) in ns
         const double tCK_avg = 1000'000. / C.eristaEmcMaxClock;
 
         // Write Latency
         const u32 WL = 14 + C.mem_burst_latency;
         // Read Latency
         const u32 RL = 32 - C.mem_burst_latency;
 
         // minimum number of cycles from any read command to any write command, irrespective of bank
         const u32 R2W = CEIL (RL + CEIL(tDQSCK_max/tCK_avg) + BL/2 - WL + tWPRE + FLOOR(tRPST)) + 6;
         
         // Delay Time From WRITE-to-READ
         const u32 W2R = WL + BL/2 + 1 + CEIL(tWTR/tCK_avg) - 6;
         
         // write-to-precharge time for commands to the same bank in cycles
         const u32 WTP = WL + BL/2 + 1 + CEIL(tWR/tCK_avg) - 8;
         
         // #_of_rows per die for 8Gb density
         const u32 numOfRows = 65536;
         // {REFRESH, REFRESH_LO} = max[(tREF/#_of_rows) / (emc_clk_period) - 64, (tREF/#_of_rows) / (emc_clk_period) * 97%]
         // emc_clk_period = dram_clk / 2;
         // 1600 MHz: 5894, but N' set to 6176 (~4.8% margin)
         const u32 REFRESH = MIN((u32)65472, u32(std::ceil((double(tREFpb) * C.eristaEmcMaxClock / numOfRows * 1.048 / 2 - 64))) / 4 * 4);
         const u32 REFBW = MIN((u32)65536, REFRESH+64);
         
         // Write With Auto Precharge to to Power-Down Entry
         const u32 WTPDEN = WTP + 1 + CEIL(tDQSS_max/tCK_avg) + CEIL(tDQS2DQ_max/tCK_avg) + 6;
         
         // Additional time after t XP hasexpired until the MRR commandmay be issued
         const double tMRRI = tRCD + 3 * tCK_avg;
         
         // tPDEX2MRR (timing delay from exiting powerdown mode to MRR command) in ns
         const double tPDEX2MRR = tXP + tMRRI;
     }
     namespace pcv::mariko {
         // tCK_avg (average clock period) in ns
         const double tCK_avg = 1000'000. / C.marikoEmcMaxClock;
         // Write Latency
         const u32 WL = 14 + C.mem_burst_latency;
         // Read Latency
         const u32 RL = 32 - C.mem_burst_latency;
 
         // minimum number of cycles from any read command to any write command, irrespective of bank
         const u32 R2W = CEIL (RL + CEIL(tDQSCK_max/tCK_avg) + BL/2 - WL + tWPRE + FLOOR(tRPST));
         
         // Delay Time From WRITE-to-READ
         const u32 W2R = WL + BL/2 + 1 + CEIL(tWTR/tCK_avg);
         
         // write-to-precharge time for commands to the same bank in cycles
         const u32 WTP = WL + BL/2 + 1 + CEIL(tWR/tCK_avg);
         
         // Read-To-MRW delay
         const u32 RTM = RL + BL/2 + CEIL(tDQSCK_max/tCK_avg) + FLOOR(tRPST) + CEIL(7.5/tCK_avg);
         
         // Write-To-MRW/MRR delay
         const u32 WTM = WL + 1 + BL/2 + CEIL(7.5/tCK_avg);
         
         // Read With AP-To-MRW/MRR delay
         const u32 RATM = RTM + CEIL(tRTP/tCK_avg) - 8;
         
         // Write With AP-To-MRW/MRR delay
         const u32 WATM = WTM + CEIL(tWR/tCK_avg);
         
         // #_of_rows per die for 8Gb density
         const u32 numOfRows = 65536;
         // {REFRESH, REFRESH_LO} = max[(tREF/#_of_rows) / (emc_clk_period) - 64, (tREF/#_of_rows) / (emc_clk_period) * 97%]
         // emc_clk_period = dram_clk / 2;
         // 1600 MHz: 5894, but N' set to 6176 (~4.8% margin)
         const u32 REFRESH = MIN((u32)65472, u32(std::ceil((double(tREFpb) * C.marikoEmcMaxClock / numOfRows * 1.048 / 2 - 64))) / 4 * 4);
         const u32 REFBW = MIN((u32)65536, REFRESH+64);
         
         // Write With Auto Precharge to to Power-Down Entry
         const u32 WTPDEN = WTP + 1 + CEIL(tDQSS_max/tCK_avg) + CEIL(tDQS2DQ_max/tCK_avg) + 6;
         
         // Additional time after t XP hasexpired until the MRR commandmay be issued
         const double tMRRI = tRCD + 3 * tCK_avg;
         
         // tPDEX2MRR (timing delay from exiting powerdown mode to MRR command) in ns
         const double tPDEX2MRR = tXP + tMRRI;
     }
 }
 