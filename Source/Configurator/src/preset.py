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
from defaults import d
import common as c
timing_vars = [
    "d.t1_tRCD",
    "d.t2_tRP",
    "d.t3_tRAS",
    "d.t4_tRRD",
    "d.t5_tRFC",
    "d.t6_tRTW",
    "d.t7_tWTR",
    "d.t8_tREFI"
]

timing_preset_default = [
    0, # tRCD
    0, # tRP
    0, # tRAS
    0, # tRRD
    0, # tRFC
    0, # tRTW
    0, # tWTR
    0, # tREFI
]

timing_preset_aamgcl_c = [
    4, # tRCD
    4, # tRP
    5, # tRAS
    5, # tRRD
    5, # tRFC
    5, # tRTW
    7, # tWTR
    6, # tREFI
]

timing_preset_aamgcl_st = [
    4, # tRCD
    4, # tRP
    8, # tRAS
    6, # tRRD
    5, # tRFC
    7, # tRTW
    8, # tWTR
    6, # tREFI
]

timing_preset_mgcj_c = [
    3, # tRCD
    2, # tRP
    4, # tRAS
    2, # tRRD
    4, # tRFC
    4, # tRTW
    4, # tWTR
    6, # tREFI
]

timing_preset_mgcj_st = [
    4, # tRCD
    3, # tRP
    8, # tRAS
    2, # tRRD
    5, # tRFC
    4, # tRTW
    4, # tWTR
    6, # tREFI
]

timing_preset_ab_mgcl_c = [
    4, # tRCD
    4, # tRP
    4, # tRAS
    4, # tRRD
    4, # tRFC
    5, # tRTW
    6, # tWTR
    6, # tREFI
]

timing_preset_ab_mgcl_st = [
    4, # tRCD
    4, # tRP
    8, # tRAS
    5, # tRRD
    5, # tRFC
    6, # tRTW
    8, # tWTR
    6, # tREFI
]
timing_preset_hb_mgch_c = [
    4, # tRCD
    4, # tRP
    4, # tRAS
    0, # tRRD
    1, # tRFC
    5, # tRTW
    4, # tWTR
    6, # tREFI
]
timing_preset_hb_mgch_st = [
    4, # tRCD
    5, # tRP
    9, # tRAS
    1, # tRRD
    2, # tRFC
    6, # tRTW
    4, # tWTR
    6, # tREFI
]

timing_preset_wtf_c = [
    4, # tRCD
    4, # tRP
    2, # tRAS
    5, # tRRD
    4, # tRFC
    6, # tRTW
    3, # tWTR
    6, # tREFI
]

timing_preset_wtf_st = [
    5, # tRCD
    5, # tRP
    4, # tRAS
    5, # tRRD
    5, # tRFC
    6, # tRTW
    5, # tWTR
    6, # tREFI
]

timing_preset_wte_c = [
    2, # tRCD
    2, # tRP
    2, # tRAS
    2, # tRRD
    4, # tRFC
    4, # tRTW
    4, # tWTR
    6, # tREFI
]

timing_preset_wte_st = [
    3, # tRCD
    5, # tRP
    3, # tRAS
    3, # tRRD
    5, # tRFC
    4, # tRTW
    5, # tWTR
    6, # tREFI
]

timing_preset_wtb_c = [
    4, # tRCD
    4, # tRP
    5, # tRAS
    5, # tRRD
    2, # tRFC
    6, # tRTW
    5, # tWTR
    6, # tREFI
]

timing_preset_wtb_st = [
    6, # tRCD
    6, # tRP
    7, # tRAS
    7, # tRRD
    2, # tRFC
    6, # tRTW
    5, # tWTR
    6, # tREFI
]

timing_preset_nee_c = [
    3, # tRCD
    3, # tRP
    2, # tRAS
    2, # tRRD
    5, # tRFC
    5, # tRTW
    4, # tWTR
    6, # tREFI
]

timing_preset_nee_st = [
    4, # tRCD
    4, # tRP
    4, # tRAS
    3, # tRRD
    7, # tRFC
    6, # tRTW
    5, # tWTR
    6, # tREFI
]

timing_preset_nme_c = [
    2, # tRCD
    2, # tRP
    1, # tRAS
    0, # tRRD
    1, # tRFC
    4, # tRTW
    3, # tWTR
    6, # tREFI
]

timing_preset_nme_st = [
    3, # tRCD
    3, # tRP
    4, # tRAS
    0, # tRRD
    1, # tRFC
    4, # tRTW
    4, # tWTR
    6, # tREFI
]


def load_defaults():
    apply_timing_preset(timing_preset_default)

def temporary_presets_unavailable():
    c.show_popup_big("We need your help!", "This timing preset currently unavailable due to lack of data. If you have a ram module and want to contribute your data, reach out to me (soul_9017) on the OC discord")

def apply_timing_preset(preset):

    if len(preset) != len(timing_vars):
        raise ValueError("Preset invalid!")
    
    for var_name, value in zip(timing_vars, preset):
        setattr(d, var_name.split('.')[-1], value)

        flag = 0 if var_name.endswith("tBL") else 5

        c.load_entry_object(var_name.split('.')[-1], flag)
    c.show_popup("Sucess", "Preset Applied!")

def apply_reg_timings(sender, app_data):
    ram_selected = dpg.get_value("ram_type")
    print(ram_selected)
    match(ram_selected):
        case "Choose your RAM Type!":
            c.show_popup("Error", "You must select a ram type to apply a preset")
        case "Samsung AA-MGCL/MGCR":
            apply_timing_preset(timing_preset_aamgcl_c)
        case "SK Hynix NEI/NEE/x267":
            apply_timing_preset(timing_preset_nee_c)
        case "Micron WT:B":
            apply_timing_preset(timing_preset_wtb_c)
        case "Micron AUT:B":
            apply_timing_preset(timing_preset_wtb_c)
        case "Micron WT:F":
            apply_timing_preset(timing_preset_wtf_c)
        case "Samsung AM-MGCJ":
            apply_timing_preset(timing_preset_mgcj_c)
        case "Micron WT:E":
            apply_timing_preset(timing_preset_wte_c)
        case "Samsung AB-MGCL":
            apply_timing_preset(timing_preset_ab_mgcl_c)
        case "SK Hynix NME":
            apply_timing_preset(timing_preset_nme_c)
        case "Samsung HB-MGCH":
            apply_timing_preset(timing_preset_hb_mgch_c)
        case _:
            temporary_presets_unavailable()

def apply_st_timings(sender, app_data):
    ram_selected = dpg.get_value("ram_type")
    match(ram_selected):
        case "Choose your RAM Type!":
            c.show_popup("Error", "You must select a ram type to apply a preset")
        case "Samsung AA-MGCL/MGCR":
            apply_timing_preset(timing_preset_aamgcl_st)
        case "SK Hynix NEI/NEE/x267":
            apply_timing_preset(timing_preset_nee_st)
        case "Micron WT:B":
            apply_timing_preset(timing_preset_wtb_st)
        case "Micron AUT:B":
            apply_timing_preset(timing_preset_wtb_st)
        case "Micron WT:F":
            apply_timing_preset(timing_preset_wtf_st)
        case "Samsung AM-MGCJ":
            apply_timing_preset(timing_preset_mgcj_st)
        case "Micron WT:E":
            apply_timing_preset(timing_preset_wte_st)
        case "Samsung AB-MGCL":
            apply_timing_preset(timing_preset_ab_mgcl_st)
        case "SK Hynix NME":
            apply_timing_preset(timing_preset_nme_st)
        case "Samsung HB-MGCH":
            apply_timing_preset(timing_preset_hb_mgch_st)
        case _:
            temporary_presets_unavailable()

