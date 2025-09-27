
"""

HOC Configurator

Copyright (C) Souldbminer

This program is free software; you can redistribute it and/or modify it
under the terms and conditions of the GNU General Public License,
version 2, as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import configparser
import dearpygui.dearpygui as dpg
import kip as k
import common
from pathlib import Path
import ini

def unimplemented():
    pass

def check_gpu_sched():
    if common.drive == 0:
        return False

    ini_path = Path(common.drive) / "atmosphere/config/system_settings.ini"
    if not ini_path.exists():
        return False

    config = configparser.ConfigParser()
    config.read(ini_path)

    return config.get("am.gpu", "gpu_scheduling_enabled", fallback="0x0").strip() == "0x1"

def toggle_gpu_sched(sender, app_data):

    ini_path = Path(common.drive) / "atmosphere/config/system_settings.ini"

    # Determine value
    value = "0x1" if app_data else "0x0"

    # Ensure the parent folder exists
    ini_path.parent.mkdir(parents=True, exist_ok=True)

    # Update using the helper function (requires str path)
    ini.set_ini_values(str(ini_path), "am.gpu", {"gpu_scheduling_enabled": value})

    common.show_popup("Success", f"Set GPU Scheduling to {app_data}")

def populate():
    offsets = list(range(0, 51, 5))
    processed_offsets = ["Disabled" if v == 0 else f"-{v} mV" for v in offsets]
    voltages = [0] + list(range(480, 960 + 1, 5))  # 0 first for Disabled
    processed_voltages = ["Disabled" if v == 0 else f"{v} mV" for v in voltages]
    voltages_e = [0] + list(range(700, 1100 + 1, 5))  # 0 first for Disabled
    processed_voltages_e = ["Disabled" if v == 0 else f"{v} mV" for v in voltages_e]
    processed_voltages_default = ["Default" if v == 0 else f"{v} mV" for v in voltages]
    freqs_khz = [
        76800, 153600, 230400, 307200, 384000, 460800, 537600, 614400, 691200, 768000,
        844800, 921600, 998400, 1075200, 1152000, 1228800, 1267200, 1305600, 1344000, 1382400, 1420800,
        1459200, 1497600, 1536000
    ]
    freqs_khz_e = [
        76800, 153600, 230400, 307200, 384000, 460800, 537600, 614400, 691200, 768000,
        844800, 921600, 998400, 1075200, 1152000
    ]
    freqs_mhz = [
        76.8, 153.6, 230.4, 307.2, 384.0, 460.8, 537.6, 614.4, 691.2, 768.0,
        844.8, 921.6, 998.4, 1075.2, 1152.0, 1228.8, 1267.2, 1305.6, 1344.0, 1382.4,
        1420.8, 1459.2, 1497.6, 1536.0
    ]
    freqs_mhz_label = [f"{f} MHz" for f in freqs_mhz]
    
    dpg.add_separator(label="Frequencies")

    dpg.add_button(
            label="What is this?",
            callback=common.show_info_window,
            user_data="A higher GPU frequency significantly increases power draw. To sustain higher frequencies without exeeding PMIC limit, undervolt your device \nDO NOT disable GPU scheduling without a adequate undervolt as it can cause hardware damage due to the high power consumption",
            width=120,
            height=64,  # height=0 makes it match text
            small=True,
            tag="freqs_info"
    )
    dpg.add_checkbox(label="GPU Scheduling", default_value=True, tag="gpu_sched", callback=toggle_gpu_sched)
    dpg.add_combo(
        items=["Disabled (0)", "Enabled (1)"],
        default_value="Disabled (0)",
        label="Enable GPU Unsafe Frequencies (Mariko)",
        callback=k.grab_kip_storage_values_no_mult,
        tag="enableMarikoGpuUnsafeFreqs"
    )
    dpg.add_combo(
        items=["Disabled (0)", "Enabled (1)"],
        default_value="Disabled (0)",
        label="Enable GPU Unsafe Frequencies (Erista)",
        callback=k.grab_kip_storage_values_no_mult,
        tag="enableEristaGpuUnsafeFreqs"
    )

    dpg.add_separator(label="Voltages")

    dpg.add_button(
            label="What is this?",
            callback=common.show_info_window,
            user_data="Lower voltages reduce power draw and tempratures. Higher voltages can boost available clockspeeds. Choose voltages with caution, as high voltages can cause IRREPERABLE hardware damage",
            width=120,
            height=64,  # height=0 makes it match text
            small=True,
            tag="volt_info"
    )
    # dpg.add_combo(
    #     items=processed_voltages,
    #     default_value="Disabled",
    #     label="Gpu vMin",
    #     callback=k.grab_kip_storage_values_no_mult,
    #     tag="g_vmin"
    # )
    # dpg.add_combo(
    #     items=processed_voltages,
    #     default_value="Disabled",
    #     label="Gpu vMax",
    #     callback=k.grab_kip_storage_values_no_mult,
    #     tag="g_vmax"
    # )

    dpg.add_separator(label="Undervolt")

    dpg.add_button(
        label="What is this?",
        callback=common.show_info_window,
        user_data="A undervolted device consumes less power, heats up less, which enables higher clocks. \nThe GPU Undervolt mode should be set to Default or High, test which one is suitable to your console. Custom is only meant for ADVANCED USERS, as the values in it could cause HARDWARE DAMAGE! \nThe Offset should be kept at the minumum your GPU requires to function at the high ram clock (high ram clock means more GPU power needed)",
        width=120,
        height=64,  # height=0 makes it match text
        small=True,
        tag="uv_info"
    )
    dpg.add_combo(
        items=["No Table (UV0)", "Regular Table (UV1)", "High Table (UV2)", "Custom Table (UV3)"],
        default_value="No Table (UV0)",
        label="Mariko Undervolt Mode",
        callback=k.grab_kip_storage_values_no_mult,
        tag="marikoGpuUV"
    )
    dpg.add_combo(
        items=["No Table (UV0)", "Regular Table (UV1)", "High Table (UV2)", "Custom Table (UV3)"],
        default_value="No Table (UV0)",
        label="Erista Undervolt Mode",
        callback=k.grab_kip_storage_values_no_mult,
        tag="eristaGpuUV"
    )
    dpg.add_combo(
        items=processed_offsets,
        default_value="Disabled",
        label="GPU Volt Offset",
        callback=k.grab_kip_storage_values_no_mult,
        tag="commonGpuVoltOffset"
    )

    dpg.add_separator(label="Custom Table (Mariko)")

    for freq in freqs_khz:
        if(freq > 1535000):
            mhz_label = f"{freq / 1000:.1f} MHz"
        elif(freq > 1382400):
            mhz_label = f"{freq / 1000:.1f} MHz (DANGEROUS)"
        elif(freq > 1152000):
            mhz_label = f"{freq / 1000:.1f} MHz (UNSAFE)"
        else:
            mhz_label = f"{freq / 1000:.1f} MHz"
        mhz_tag = f"combo_{freq}"
        if freq == 1536000:
            with dpg.group(horizontal=True):  # align horizontally
                dpg.add_combo(
                    items=processed_voltages,
                    default_value="Disabled",
                    label=mhz_label,
                    tag="g_volt_" + str(freq),
                    callback=k.grab_kip_storage_values_no_mult
                )
                dpg.add_text("(")
                dpg.add_image("coolerhd", width=16, height=16)
                dpg.add_text(")")
        else:
            dpg.add_combo(
                items=processed_voltages,
                default_value="Disabled",
                label=mhz_label,
                tag="g_volt_" + str(freq),
                callback=k.grab_kip_storage_values_no_mult
            )

    dpg.add_separator(label="Custom Table (Erista)")

    for freq in freqs_khz_e:
        if(freq > 1151000):
            mhz_label = f"{freq / 1000:.1f} MHz (DANGEROUS)"
        elif(freq > 922000):
            mhz_label = f"{freq / 1000:.1f} MHz (UNSAFE)"
        else:
            mhz_label = f"{freq / 1000:.1f} MHz"
        mhz_tag = f"combo_e_{freq}"
        dpg.add_combo(
            items=processed_voltages_e,
            default_value="Disabled",
            label=mhz_label,
            tag="g_volt_e_" + str(freq),
            callback=k.grab_kip_storage_values_no_mult
        )