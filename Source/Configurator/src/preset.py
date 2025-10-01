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
import settings as s

def load_defaults():
    apply_timing_preset(s.timing_preset_default)

def temporary_presets_unavailable():
    c.show_popup_big("We need your help!", "This timing preset currently unavailable due to lack of data. If you have a ram module and want to contribute your data, reach out to me (soul_9017) on the OC discord")

def apply_timing_preset(preset):

    if len(preset) != len(s.timing_vars):
        raise ValueError("Preset invalid!")
    
    for var_name, value in zip(s.timing_vars, preset):
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
            apply_timing_preset(s.timing_preset_aamgcl_c)
        case "SK Hynix NEI/NEE/x267":
            apply_timing_preset(s.timing_preset_nee_c)
        case "Micron WT:B":
            apply_timing_preset(s.timing_preset_wtb_c)
        case "Micron AUT:B":
            apply_timing_preset(s.timing_preset_wtb_c)
        case "Micron WT:F":
            apply_timing_preset(s.timing_preset_wtf_c)
        case "Samsung AM-MGCJ":
            apply_timing_preset(s.timing_preset_mgcj_c)
        case "Micron WT:E":
            apply_timing_preset(s.timing_preset_wte_c)
        case "Samsung AB-MGCL":
            apply_timing_preset(s.timing_preset_ab_mgcl_c)
        case "SK Hynix NME":
            apply_timing_preset(s.timing_preset_nme_c)
        case "Samsung HB-MGCH":
            apply_timing_preset(s.timing_preset_hb_mgch_c)
        case _:
            temporary_presets_unavailable()

def apply_st_timings(sender, app_data):
    ram_selected = dpg.get_value("ram_type")
    match(ram_selected):
        case "Choose your RAM Type!":
            c.show_popup("Error", "You must select a ram type to apply a preset")
        case "Samsung AA-MGCL/MGCR":
            apply_timing_preset(s.timing_preset_aamgcl_st)
        case "SK Hynix NEI/NEE/x267":
            apply_timing_preset(s.timing_preset_nee_st)
        case "Micron WT:B":
            apply_timing_preset(s.timing_preset_wtb_st)
        case "Micron AUT:B":
            apply_timing_preset(s.timing_preset_wtb_st)
        case "Micron WT:F":
            apply_timing_preset(s.timing_preset_wtf_st)
        case "Samsung AM-MGCJ":
            apply_timing_preset(s.timing_preset_mgcj_st)
        case "Micron WT:E":
            apply_timing_preset(s.timing_preset_wte_st)
        case "Samsung AB-MGCL":
            apply_timing_preset(s.timing_preset_ab_mgcl_st)
        case "SK Hynix NME":
            apply_timing_preset(s.timing_preset_nme_st)
        case "Samsung HB-MGCH":
            apply_timing_preset(s.timing_preset_hb_mgch_st)
        case _:
            temporary_presets_unavailable()

