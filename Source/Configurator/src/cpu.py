
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


import dearpygui.dearpygui as dpg
import common
import kip as k
import gpu as g
def populate():
    freqs_hz_cpu = [
        1020000, 1122000, 1224000, 1326000, 1428000, 1581000, 1683000,
        1785000, 1887000, 1963500, 2091000, 2193000, 2295000, 2397000,
        2499000, 2601000, 2703000, 2805000, 2907000
    ]
    freqs_mhz_cpu = [
        1020.0, 1122.0, 1224.0, 1326.0, 1428.0, 1581.0, 1683.0,
        1785.0, 1887.0, 1963.5, 2091.0, 2193.0, 2295.0, 2397.0,
        2499.0, 2601.0, 2703.0, 2805.0, 2907.0
    ]
    freqs_mhz_cpu_label = [f"{f} MHz" for f in freqs_mhz_cpu]
    offsets = list(range(0, 101, 5))
    processed_offsets = ["Disabled" if v == 0 else f"-{v}mV" for v in offsets]
    voltages = [0] + list(range(1000, 1160 + 1, 5))  # 0 first for Disabled
    processed_voltages = ["Disabled" if v == 0 else f"{v}mV" for v in voltages]
    processed_voltages_default = ["Default" if v == 0 else f"{v}mV" for v in voltages]
    voltages_e = [0] + list(range(1120, 1255 + 1, 5)) + [1257]  # 0 first for Disabled
    processed_voltages_e = ["Disabled" if v == 0 else f"{v}mV" for v in voltages_e]
    processed_voltages_default_e = ["Default" if v == 0 else f"{v}mV" for v in voltages_e]

    vmin_voltages = list(range(500, 700 + 1, 5))  # 0 first for Disabled
    vmin_processed_voltages = ["Disabled" if v == 0 else f"{v}mV" for v in vmin_voltages]

    dpg.add_separator(label="Frequencies")

    dpg.add_button(
            label="What is this?",
            callback=common.show_info_window,
            user_data="A higher CPU frequency significantly increases power draw. To sustain higher frequencies without exeeding PMIC limit, undervolt your device. \nThe CPU Boost Frequency is used to speed up game loading",
            width=120,
            height=64,  # height=0 makes it match text
            small=True,
            tag="c_freqs_info"
    )
    dpg.add_combo(
        items=["Disabled (0)", "Enabled (1)"],
        default_value="Disabled (0)",
        label="Enable CPU Unsafe Frequencies (Mariko)",
        callback=k.grab_kip_storage_values_no_mult,
        tag="enableMarikoCpuUnsafeFreqs"
    )
    dpg.add_combo(
        items=["Disabled (0)", "Enabled (1)"],
        default_value="Disabled (0)",
        label="Enable CPU Unsafe Frequencies (Erista)",
        callback=k.grab_kip_storage_values_no_mult,
        tag="enableEristaCpuUnsafeFreqs"
    )

    dpg.add_combo(
        items=freqs_mhz_cpu_label,
        default_value="1785.0MHz",
        label="CPU Boost Frequency",
        callback=k.grab_kip_storage_values,
        tag="commonCpuBoostClock"
    )

    dpg.add_separator(label="Voltages")

    dpg.add_button(
            label="What is this?",
            callback=common.show_info_window,
            user_data="Lower voltages reduce power draw and tempratures. Higher voltages can boost available clockspeeds. Choose voltages with caution, as high voltages can cause IRREPERABLE hardware damage",
            width=120,
            height=64,  # height=0 makes it match text
            small=True,
            tag="c_volt_info"
    )
    dpg.add_combo(
        items=vmin_processed_voltages,
        default_value="Default (600mV)",
        label="CPU vMin (Mariko)",
        tag="marikoCpuVmin",
        callback=k.grab_kip_storage_values_no_mult
    )

    dpg.add_combo(
        items=processed_voltages,
        default_value="Disabled",
        label="CPU vMax (Mariko)",
        tag="marikoCpuMaxVolt",
        callback=k.grab_kip_storage_values_no_mult
    )
    dpg.add_combo(
        items=processed_voltages_e,
        default_value="Disabled",
        label="CPU vMax (Erista)",
        tag="eristaCpuMaxVolt",
        callback=k.grab_kip_storage_values_no_mult
    )

    dpg.add_separator(label="Undervolt (Mariko ONLY)")

    dpg.add_button(
        label="What is this?",
        callback=common.show_info_window,
        user_data="A undervolted device consumes less power, heats up less, which enables higher clocks. \nThe GPU Undervolt mode should be set to Default or High, test which one is suitable to your console. Custom is only meant for ADVANCED USERS, as the values in it could cause HARDWARE DAMAGE! \nThe Offset should be kept at the minumum your GPU requires to function at the high ram clock (high ram clock means more GPU power needed, usually 600mV is sufficient)",
        width=120,
        height=64,  # height=0 makes it match text
        small=True,
        tag="c_uv_info"
    )
    dpg.add_combo(
        items=list(range(0, 8 + 1, 1)),
        default_value="Default Table",
        label="Mariko CPU Undervolt",
        tag="marikoCpuUV",
        callback=k.grab_kip_storage_values_no_mult
    )
    dpg.add_combo(
        items=list(range(0, 5 + 1, 1)),
        default_value="Default Table",
        label="Erista CPU Undervolt",
        tag="eristaCpuUV",
        callback=k.grab_kip_storage_values_no_mult
    )
    # dpg.add_combo(
    #     items=["0","1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
    #     default_value="0",
    #     label="High Frequency Undervolt",
    #     tag="m_cpu_huv",
    #     callback=k.grab_kip_storage_values_no_mult
    # )
    # dpg.add_combo(
    #     items=processed_offsets,
    #     default_value="Disabled",
    #     label="CPU Volt Offset",
    #     callback=k.grab_kip_storage_values_no_mult,
    #     tag="m_cpu_hv_offset"
    # )