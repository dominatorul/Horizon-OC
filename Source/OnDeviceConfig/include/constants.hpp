/*
 * HOC Configurator - Constants
 * Copyright (C) Dominatorul, Souldbminer
 */

#pragma once
#include <cstdint>
#include <string>

namespace Constants {
    // Application info
    constexpr const char* APP_VERSION = "2.0.0";
    constexpr const char* APP_NAME = "HOC Configurator";
    constexpr const char* APP_AUTHOR = "Dominatorul";
    
    // Paths
    constexpr const char* DEFAULT_KIP_PATH = "sdmc:/atmosphere/kips/loader.kip";
    constexpr const char* CONFIG_DIR = "sdmc:/config/hoc-configurator";
    constexpr const char* CONFIG_FILE = "sdmc:/config/hoc-configurator/config.ini";
    constexpr const char* ATMOSPHERE_PATH = "sdmc:/atmosphere";
    constexpr const char* SYSTEM_SETTINGS_INI = "sdmc:/atmosphere/config/system_settings.ini";
    
    // Frequency arrays (in kHz)
    constexpr uint32_t MARIKO_GPU_FREQS[] = {
        76800, 153600, 230400, 307200, 384000, 460800, 537600, 614400,
        691200, 768000, 844800, 921600, 998400, 1075200, 1152000, 1228800,
        1267200, 1305600, 1344000, 1382400, 1420800, 1459200, 1497600, 1536000
    };
    
    constexpr uint32_t ERISTA_GPU_FREQS[] = {
        76800, 153600, 230400, 307200, 384000, 460800, 537600, 614400,
        691200, 768000, 844800, 921600, 998400, 1075200
    };
    
    constexpr uint32_t CPU_FREQS[] = {
        1020000, 1122000, 1224000, 1326000, 1428000, 1581000, 1683000,
        1785000, 1887000, 1963500, 2091000, 2193000, 2295000, 2397000,
        2499000, 2601000, 2703000, 2805000, 2907000
    };
    
    constexpr uint32_t RAM_FREQS[] = {
        0, 1600000, 1633000, 1666000, 1700000, 1733000, 1766000, 1800000,
        1833000, 1866000, 1900000, 1933000, 1966000, 2000000, 2033000, 2066000,
        2100000, 2133000, 2166000, 2200000, 2233000, 2266000, 2300000
    };
    
    // Voltage ranges
    constexpr uint32_t MARIKO_GPU_MIN_VOLT = 480;
    constexpr uint32_t MARIKO_GPU_MAX_VOLT = 960;
    constexpr uint32_t MARIKO_GPU_MAX_VMIN = 700;
    
    constexpr uint32_t ERISTA_GPU_MIN_VOLT = 700;
    constexpr uint32_t ERISTA_GPU_MAX_VOLT = 1000;
    constexpr uint32_t ERISTA_GPU_MAX_VMIN = 850;
    
    constexpr uint32_t MARIKO_CPU_MIN_VMIN = 700;
    constexpr uint32_t MARIKO_CPU_MAX_VMIN = 750;
    
    constexpr uint32_t VOLTAGE_STEP = 5;
    constexpr uint32_t GPU_OFFSET_MAX = 50;
    
    // Thresholds
    constexpr uint32_t MARIKO_MEME_THRESHOLD = 1536000;
    constexpr uint32_t MARIKO_DANGEROUS_GPU_THRESHOLD = 1382400;
    constexpr uint32_t MARIKO_UNSAFE_GPU_THRESHOLD = 1152000;
    
    constexpr uint32_t ERISTA_DANGEROUS_GPU_THRESHOLD = 1151000;
    constexpr uint32_t ERISTA_UNSAFE_GPU_THRESHOLD = 922000;
    
    // RAM Types
    const std::string RAM_TYPES[] = {
        "Samsung AA-MGCL/MGCR",
        "SK Hynix NEI/NEE/x267",
        "Micron WT:B",
        "Micron AUT:B",
        "Micron WT:F",
        "Samsung AM-MGCJ",
        "Micron WT:E",
        "Samsung AB-MGCL",
        "SK Hynix NME",
        "Samsung HB-MGCH"
    };
    
    // Fan curve profiles
    namespace FanProfiles {
        constexpr const char* V1_ERISTA = "V1_Erista";
        constexpr const char* V2_MARIKO = "V2_Mariko";
        constexpr const char* LITE_MARIKO = "Lite_Mariko";
        constexpr const char* OLED_MARIKO = "OLED_Mariko";
    }
    
    // PSM (Battery) options
    struct PSMOption {
        const char* name;
        uint32_t value;
    };
    
    constexpr PSMOption PSM_OPTIONS[] = {
        {"1024mA", 0x400},
        {"1280mA", 0x500},
        {"1536mA", 0x600},
        {"1660mA (Lite Default)", 0x67C},
        {"1792mA", 0x700},
        {"2048mA (Default)", 0x800},
        {"2304mA (UNSAFE)", 0x900},
        {"2560mA (UNSAFE)", 0xA00},
        {"2816mA (DANGEROUS)", 0xB00},
        {"3072mA (DANGEROUS)", 0xC00}
    };
    
    // Memory timing presets
    struct TimingPreset {
        uint32_t tRCD;
        uint32_t tRP;
        uint32_t tRAS;
        uint32_t tRRD;
        uint32_t tRFC;
        uint32_t tRTW;
        uint32_t tWTR;
        uint32_t tREFI;
    };
    
    // Default timing preset
    constexpr TimingPreset TIMING_DEFAULT = {0, 0, 0, 0, 0, 0, 0, 0};
    
    // Samsung AA-MGCL/MGCR presets
    constexpr TimingPreset TIMING_AAMGCL_CONSERVATIVE = {4, 4, 5, 5, 5, 5, 7, 6};
    constexpr TimingPreset TIMING_AAMGCL_TIGHT = {4, 4, 8, 6, 5, 7, 8, 6};
    
    // SK Hynix NEE presets
    constexpr TimingPreset TIMING_NEE_CONSERVATIVE = {3, 3, 2, 2, 5, 5, 4, 6};
    constexpr TimingPreset TIMING_NEE_TIGHT = {4, 4, 4, 3, 7, 6, 5, 6};
    
    // Micron WT:B presets
    constexpr TimingPreset TIMING_WTB_CONSERVATIVE = {4, 4, 5, 5, 2, 6, 5, 6};
    constexpr TimingPreset TIMING_WTB_TIGHT = {6, 6, 7, 7, 2, 6, 5, 6};
    
    // UI Constants
    constexpr int MAX_VISIBLE_ITEMS = 20;
    constexpr int MENU_START_Y = 7;
    constexpr int SCREEN_WIDTH = 80;
    constexpr int SCREEN_HEIGHT = 45;
}
