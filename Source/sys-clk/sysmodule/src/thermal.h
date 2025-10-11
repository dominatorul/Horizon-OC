/* * HOS soctherm driver by Souldbminer & Dominatorul * Licensed under the LGPLv3 */
#ifndef _SOCTHERM_H_
#define _SOCTHERM_H_

#include <switch.h>

#define SOCTHERM_BASE 0x700E2000ULL

#define SENSOR_TEMP1 0xCC
#define SENSOR_TEMP2 0x1AC

#define SENSOR_CPU0_CONFIG0  0xC0
#define SENSOR_CPU1_CONFIG0  0xE0
#define SENSOR_CPU2_CONFIG0  0x100
#define SENSOR_CPU3_CONFIG0  0x120
#define SENSOR_GPU_CONFIG0   0x180
#define SENSOR_PLLX_CONFIG0  0x1A0

#define SENSOR_CPU0_CONFIG1  0xC4
#define SENSOR_CPU1_CONFIG1  0xE4
#define SENSOR_CPU2_CONFIG1  0x104
#define SENSOR_CPU3_CONFIG1  0x124
#define SENSOR_GPU_CONFIG1   0x184
#define SENSOR_PLLX_CONFIG1  0x1A4

#define SENSOR_CPU0_STATUS   0xC8
#define SENSOR_GPU_STATUS    0x188
#define SENSOR_PLLX_STATUS   0x1A8

#define SENSOR_CONFIG0_STOP_MASK      (1U << 0)
#define SENSOR_CONFIG0_TALL_SHIFT     8
#define SENSOR_CONFIG0_TALL_MASK      (0xFFFFF << 8)

#define SENSOR_CONFIG1_TEMP_ENABLE_MASK   (1U << 31)
#define SENSOR_CONFIG1_TEN_COUNT_SHIFT    24
#define SENSOR_CONFIG1_TEN_COUNT_MASK     (0x3F << 24)
#define SENSOR_CONFIG1_TIDDQ_EN_SHIFT     15
#define SENSOR_CONFIG1_TIDDQ_EN_MASK      (0x3F << 15)
#define SENSOR_CONFIG1_TSAMPLE_SHIFT      0
#define SENSOR_CONFIG1_TSAMPLE_MASK       0x3FF

#define SENSOR_STATUS_VALID_MASK          (1U << 31)

#define TSENSOR_TALL_DEFAULT      16300
#define TSENSOR_TIDDQ_EN_DEFAULT  1
#define TSENSOR_TEN_COUNT_DEFAULT 1
#define TSENSOR_TSAMPLE_DEFAULT   120

#define SENSOR_TEMP1_CPU_TEMP_MASK  (0xFFFF << 16)
#define SENSOR_TEMP1_GPU_TEMP_MASK  0xFFFF
#define SENSOR_TEMP2_PLLX_TEMP_MASK 0xFFFF

#define READBACK_VALUE_MASK   0xFF00
#define READBACK_VALUE_SHIFT  8
#define READBACK_ADD_HALF     (1 << 7)
#define READBACK_NEGATE       (1 << 0)

#define REG_GET_MASK(r, m) (((r) & (m)) >> (__builtin_ffs(m) - 1))

// Timing constants (in microseconds)
#define SENSOR_STABILIZATION_DELAY_US  2000  // 2ms for sensor to stabilize
#define SENSOR_READ_DELAY_US           100   // 100us between config operations

typedef enum {
    SENSOR_CPU  = 0,
    SENSOR_GPU  = 1,
    SENSOR_PLLX = 2,
} SocthermSensor;

// Track which sensors have been initialized
static bool g_sensor_initialized[3] = {false, false, false};

static inline int soctherm_translate_temp(u16 val) {
    int t;
    
    t = ((val & READBACK_VALUE_MASK) >> READBACK_VALUE_SHIFT) * 1000;
    if (val & READBACK_ADD_HALF)
        t += 500;
    if (val & READBACK_NEGATE)
        t *= -1;
    
    return t;
}

static inline bool socthermEnableSensor(SocthermSensor sensor) {
    Result rc = 0;
    u64 virt_addr = 0;
    u64 out_size = 0;
    u32 config0_offset, config1_offset, status_offset;
    u32 val;
    
    rc = svcQueryMemoryMapping(&virt_addr, &out_size, SOCTHERM_BASE, 0x1000);
    if (R_FAILED(rc))
        return false;
    
    switch (sensor) {
        case SENSOR_CPU:
            config0_offset = SENSOR_CPU0_CONFIG0;
            config1_offset = SENSOR_CPU0_CONFIG1;
            status_offset = SENSOR_CPU0_STATUS;
            break;
        case SENSOR_GPU:
            config0_offset = SENSOR_GPU_CONFIG0;
            config1_offset = SENSOR_GPU_CONFIG1;
            status_offset = SENSOR_GPU_STATUS;
            break;
        case SENSOR_PLLX:
            config0_offset = SENSOR_PLLX_CONFIG0;
            config1_offset = SENSOR_PLLX_CONFIG1;
            status_offset = SENSOR_PLLX_STATUS;
            break;
        default:
            svcUnmapMemory((void *)virt_addr, (void *)SOCTHERM_BASE, 0x1000);
            return false;
    }
    
    // Step 1: Clear STOP bit and configure TALL
    val = *(volatile u32 *)(virt_addr + config0_offset);
    val &= ~SENSOR_CONFIG0_STOP_MASK;  // Clear STOP bit
    val &= ~SENSOR_CONFIG0_TALL_MASK;  // Clear old TALL value
    val |= (TSENSOR_TALL_DEFAULT << SENSOR_CONFIG0_TALL_SHIFT);
    *(volatile u32 *)(virt_addr + config0_offset) = val;
    
    // Small delay after CONFIG0 write
    svcSleepThread(SENSOR_READ_DELAY_US * 1000ULL);
    
    // Step 2: Configure and enable sensor
    val = ((TSENSOR_TSAMPLE_DEFAULT - 1) << SENSOR_CONFIG1_TSAMPLE_SHIFT) |
          (TSENSOR_TIDDQ_EN_DEFAULT << SENSOR_CONFIG1_TIDDQ_EN_SHIFT) |
          (TSENSOR_TEN_COUNT_DEFAULT << SENSOR_CONFIG1_TEN_COUNT_SHIFT) |
          SENSOR_CONFIG1_TEMP_ENABLE_MASK;
    *(volatile u32 *)(virt_addr + config1_offset) = val;
    
    // Wait for sensor to stabilize after enabling
    svcSleepThread(SENSOR_STABILIZATION_DELAY_US * 1000ULL);
    
    // Step 3: Verify sensor is ready by checking status
    u32 status;
    int retries = 10;
    bool sensor_ready = false;
    
    while (retries-- > 0) {
        status = *(volatile u32 *)(virt_addr + status_offset);
        if (status & SENSOR_STATUS_VALID_MASK) {
            sensor_ready = true;
            break;
        }
        svcSleepThread(100000ULL); // 100us between retries
    }
    
    svcUnmapMemory((void *)virt_addr, (void *)SOCTHERM_BASE, 0x1000);
    
    if (sensor_ready) {
        g_sensor_initialized[sensor] = true;
    }
    
    return sensor_ready;
}

static inline int socthermReadTemp(SocthermSensor sensor) {
    Result rc = 0;
    u64 virt_addr = 0;
    u64 out_size = 0;
    void *soctherm_map = NULL;
    int temp = 0;
    
    // Auto-initialize sensor if not already initialized
    if (!g_sensor_initialized[sensor]) {
        if (!socthermEnableSensor(sensor)) {
            return -1;
        }
    }
    
    rc = svcQueryMemoryMapping(&virt_addr, &out_size, SOCTHERM_BASE, 0x1000);
    if (R_FAILED(rc))
        return -1;
    
    soctherm_map = (void *)virt_addr;
    
    u32 reg_val;
    u16 raw_temp;
    
    // Add a small delay before reading to ensure sensor data is fresh
    svcSleepThread(50000ULL); // 50us
    
    switch (sensor) {
        case SENSOR_CPU:
            reg_val = *(volatile u32 *)((u8 *)soctherm_map + SENSOR_TEMP1);
            raw_temp = REG_GET_MASK(reg_val, SENSOR_TEMP1_CPU_TEMP_MASK);
            break;
                 
        case SENSOR_GPU:
            reg_val = *(volatile u32 *)((u8 *)soctherm_map + SENSOR_TEMP1);
            raw_temp = REG_GET_MASK(reg_val, SENSOR_TEMP1_GPU_TEMP_MASK);
            break;
                 
        case SENSOR_PLLX:
            reg_val = *(volatile u32 *)((u8 *)soctherm_map + SENSOR_TEMP2);
            raw_temp = REG_GET_MASK(reg_val, SENSOR_TEMP2_PLLX_TEMP_MASK);
            break;
                 
        default:
            svcUnmapMemory(soctherm_map, (void *)SOCTHERM_BASE, 0x1000);
            return -1;
    }
    
    temp = soctherm_translate_temp(raw_temp);
    
    svcUnmapMemory(soctherm_map, (void *)SOCTHERM_BASE, 0x1000);
    
    return temp;
}

static inline int socthermReadCpuTemp(void) {
    return socthermReadTemp(SENSOR_CPU);
}

static inline int socthermReadGpuTemp(void) {
    return socthermReadTemp(SENSOR_GPU);
}

static inline int socthermReadPllTemp(void) {
    return socthermReadTemp(SENSOR_PLLX);
}

static inline int socthermMCToC(int millicelsius) {
    return millicelsius / 1000;
}

static inline void socthermMCToCWithDecimal(int millicelsius, int *celsius, int *decimal) {
    if (celsius) *celsius = millicelsius / 1000;
    if (decimal) *decimal = (millicelsius % 1000 + 1000) % 1000; // Handle negative temps
}

#endif