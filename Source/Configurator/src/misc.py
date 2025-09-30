
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

import os
from pathlib import Path
import dearpygui.dearpygui as dpg
import common
import ini
import re
import installer as ins
from defaults import d
import ram as r

skinTarget = 54  # default value

def get_ini_path():
    if not common.drive or common.drive == 0:
        common.show_popup("Error", "This feature requires a valid drive")
        return None
    return Path(str(common.drive)) / "atmosphere/config/system_settings.ini"

PROFILES = {
    "V1_Erista": {
        "tskin_pcb_coefficients_console_on_fwdbg": 'str!"[6396, 119440]"',
        "tskin_pcb_coefficients_handheld_on_fwdbg": 'str!"[5817, 129580]"',
        "tskin_soc_coefficients_console_on_fwdbg": 'str!"[6182, 112480]"',
        "tskin_soc_coefficients_handheld_on_fwdbg": 'str!"[5464, 174190]"',
    },
    "V2_Mariko": {
        "tskin_pcb_coefficients_console_on_fwdbg": 'str!"[7338, 112161]"',
        "tskin_pcb_coefficients_handheld_on_fwdbg": 'str!"[6357, 168124]"',
        "tskin_soc_coefficients_console_on_fwdbg": 'str!"[6728, 129810]"',
        "tskin_soc_coefficients_handheld_on_fwdbg": 'str!"[5675, 203453]"',
    },
    "Lite_Mariko": {
        "tskin_pcb_coefficients_console_on_fwdbg": 'str!"[7338, 112161]"',
        "tskin_pcb_coefficients_handheld_on_fwdbg": 'str!"[5594, 209601]"',
        "tskin_soc_coefficients_console_on_fwdbg": 'str!"[6728, 129810]"',
        "tskin_soc_coefficients_handheld_on_fwdbg": 'str!"[5235, 199759]"',
    },
    "OLED_Mariko": {
        "tskin_pcb_coefficients_console_on_fwdbg": 'str!"[8051, -45213]"',
        "tskin_pcb_coefficients_handheld_on_fwdbg": 'str!"[7176, -33954]"',
        "tskin_soc_coefficients_console_on_fwdbg": 'str!"[7831, 57590]"',
        "tskin_soc_coefficients_handheld_on_fwdbg": 'str!"[9029, 4274]"',
    },
}

BATTERY_SAVE_OPTIONS = {
    "bgtc": {
        "enable_halfawake": "u32!0x0",
        "minimum_interval_normal": "u32!0x7FFFFFFF",
        "minimum_interval_save": "u32!0x7FFFFFFF",
        "battery_threshold_save": "u32!0x64",
        "battery_threshold_stop": "u32!0x64",
    },
    "npns": {
        "background_processing": "u8!0x0",
        "sleep_periodic_interval": "u32!0x7FFFFFFF",
        "sleep_processing_timeout": "u32!0x0",
        "sleep_max_try_count": "u32!0x0",
    },
    "ns.notification": {
        "enable_download_task_list": "u8!0x0",
        "enable_download_ticket": "u8!0x0",
        "enable_network_update": "u8!0x0",
        "enable_random_wait": "u8!0x0",
        "enable_request_on_cold_boot": "u8!0x0",
        "enable_send_rights_usage_status_request": "u8!0x0",
        "enable_sync_elicense_request": "u8!0x0",
        "enable_version_list": "u8!0x0",
        "retry_interval_min": "u32!0x7FFFFFFF",
        "retry_interval_max": "u32!0x7FFFFFFF",
        "version_list_waiting_limit_bias": "u32!0x7FFFFFFF",
        "version_list_waiting_limit_min": "u32!0x7FFFFFFF",
    },
    "account": {
        "na_required_for_network_service": "u8!0x0",
        "na_license_verification_enabled": "u8!0x0",
    },
    "account.daemon": {
        "background_awaking_periodicity": "u32!0x7FFFFFFF",
        "initial_schedule_delay": "u32!0x7FFFFFFF",
        "profile_sync_interval": "u32!0x7FFFFFFF",
        "na_info_refresh_interval": "u32!0x7FFFFFFF",
    },
    "capsrv": {
        "enable_album_screenshot_filedata_verification": "u8!0x0",
        "enable_album_movie_filehash_verification": "u8!0x0",
        "enable_album_movie_filesign_verification": "u8!0x0",
    },
    "friends": {
        "background_processing": "u8!0x0",
    },
    "notification.presenter": {
        "snooze_interval_in_seconds": "u32!0x7FFFFFFF",
        "connection_retry_count": "u32!0x0",
        "alarm_pattern_total_repeat_count": "u32!0x0",
        "alarm_pattern_with_vibration_repeat_count": "u32!0x0",
    },
    "prepo": {
        "transmission_interval_min": "u32!0x7FFFFFFF",
        "transmission_retry_interval_min": "u32!0x7FFFFFFF",
        "transmission_retry_interval_max": "u32!0x7FFFFFFF",
        "transmission_interval_in_sleep": "u32!0x7FFFFFFF",
        "statistics_save_interval_min": "u32!0x7FFFFFFF",
        "statistics_post_interval": "u32!0x7FFFFFFF",
        "save_system_report": "u8!0x0",
    },
    "olsc": {
        "default_auto_upload_global_setting": "u8!0x0",
        "default_auto_download_global_setting": "u8!0x0",
        "autonomy_registration_interval_seconds": "u32!0x7FFFFFFF",
        "network_service_license_info_cache_expiration_seconds": "u32!0x7FFFFFFF",
        "postponed_transfer_task_processing_interval_seconds": "u32!0x7FFFFFFF",
        "retry_offset_seconds": "u32!0x7FFFFFFF",
        "network_trouble_detection_span_seconds": "u32!0x7FFFFFFF",
        "network_connection_polling_interval_seconds": "u32!0x7FFFFFFF",
        "is_save_data_backup_policy_check_required": "u8!0x0",
        "is_global_transfer_task_autonomy_registration_enabled": "u8!0x0",
        "is_on_event_transfer_task_registration_enabled": "u8!0x0",
        "is_periodic_transfer_task_registration_enabled": "u8!0x0",
    },
    "ntc": {
        "is_autonomic_correction_enabled": "u8!0x0",
        "autonomic_correction_interval_seconds": "u32!0x7FFFFFFF",
        "autonomic_correction_failed_retry_interval_seconds": "u32!0x7FFFFFFF",
        "autonomic_correction_immediate_try_count_max": "u32!0x0",
        "autonomic_correction_immediate_try_interval_milliseconds": "u32!0x7FFFFFFF",
    },
    "systemupdate": {
        "bgnup_retry_seconds": "u32!0x7FFFFFFF",
    },
    "ns.rights": {
        "skip_account_validation_on_rights_check": "u8!0x1",
        "next_available_time_of_unexpected_error": "u32!0x7FFFFFFF",
    },
    "pctl": {
        "intermittent_task_interval_seconds": "u32!0x7FFFFFFF",
    },
    "sprofile": {
        "adjust_polling_interval_by_profile": "u8!0x0",
        "polling_interval_sec_max": "u32!0x7FFFFFFF",
        "polling_interval_sec_min": "u32!0x7FFFFFFF",
    },
}

PSM_OPTIONS = [
    {"name": "1024mA", "value": "u32!0x400"},
    {"name": "1280mA", "value": "u32!0x500"},
    {"name": "1536mA", "value": "u32!0x600"},
    {"name": "1660mA (Lite Default)", "value": "u32!0x67C"},
    {"name": "1792mA", "value": "u32!0x700"},
    {"name": "2048mA (Default)", "value": "u32!0x800"},
    {"name": "2304mA (UNSAFE)", "value": "u32!0x900"},
    {"name": "2560mA (UNSAFE)", "value": "u32!0xA00"},
    {"name": "2816mA (DANGEROUS)", "value": "u32!0xB00"},
    {"name": "3072mA (DANGEROUS)", "value": "u32!0xC00"},
]

def set_psm_value(sender, app_data):
    ini_path = get_ini_path()
    if not ini_path:
        return
    value = next((x["value"] for x in PSM_OPTIONS if x["name"] == app_data), None)
    if value:
        ini.set_ini_values(str(ini_path), "psm", {"current_psm_mA": value})
        common.show_popup("Success", f"Charge Limit set to {app_data}")

def remove_tc_entries():
    ini_path = get_ini_path()
    if not ini_path:
        return

    try:
        with open(ini_path, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return

    output_lines = []
    current_section = None

    for line in lines:
        section_match = re.match(r"\s*\[([^\]]+)\]", line)
        if section_match:
            current_section = section_match.group(1)
            if current_section == "tc":
                current_section = "skip"
                continue
            else:
                output_lines.append(line)
                continue

        if current_section != "skip":
            output_lines.append(line)

    with open(ini_path, "w") as f:
        f.writelines(output_lines)
    common.show_popup("Success", "Reset to default fan curve")


def set_ini_from_profile(sender, app_data, user_data):
    profile_name = user_data
    if profile_name not in PROFILES:
        print(f"Profile '{profile_name}' not found.")
        return

    entries = PROFILES[profile_name]
    ini_path = get_ini_path()
    if not ini_path:
        return
    ini.set_ini_values(str(ini_path), "tc", entries)
    common.show_popup("Success", "Profile has been applied")
    print(f"Applied profile {profile_name} under [tc]")

def update_skin_target(sender, app_data):
    global skinTarget
    skinTarget = app_data
    print("skinTarget =", skinTarget)

    ini_path = get_ini_path()
    if not ini_path:
        return

    entries = {
        "use_configurations_on_fwdbg": "u8!0x1",
        "tskin_rate_table_console_on_fwdbg": f'str!"[[-1000000,40000,0,0],[36000,43000,51,51],[43000,49000,51,128],[49000,{skinTarget}000,128,255],[{skinTarget}000,1000000,255,255]]"',
        "tskin_rate_table_handheld_on_fwdbg": f'str!"[[-1000000,40000,0,0],[36000,43000,51,51],[43000,49000,51,128],[49000,{skinTarget}000,128,255],[{skinTarget}000,1000000,255,255]]"',
        "holdable_tskin": "u32!0xEA60",
        "touchable_tskin": "u32!0xEA60"
    }

    ini.set_ini_values(str(ini_path), "tc", entries)

def toggle_battery_save(sender, user_data):

    if not common.drive:
        common.show_popup("Error", "No drive selected")
        return

    ini_path = Path(common.drive) / "atmosphere/config/system_settings.ini"

    for section, entries in BATTERY_SAVE_OPTIONS.items():
        if dpg.get_item_alias(sender) == "enable_battery_fix":  # hardcoded but otherwise it doesnt work :(
            ini.set_ini_values(str(ini_path), section, entries)
        else:
            remove_entries = {k: None for k in entries}
            ini.set_ini_values(str(ini_path), section, remove_entries)

    common.show_popup("Info", f"Sleep Mode Battery Fix {'enabled' if dpg.get_item_alias(sender) == "enable_battery_fix" else 'disabled'}")
def populate():
    dpg.add_separator(label="Fan")
    dpg.add_button(label="Optimize Fan Curve for V1", user_data="V1_Erista", callback=set_ini_from_profile)
    dpg.add_button(label="Optimize Fan Curve for V2", user_data="V2_Mariko", callback=set_ini_from_profile)
    dpg.add_button(label="Optimize Fan Curve for Lite", user_data="Lite_Mariko", callback=set_ini_from_profile)
    dpg.add_button(label="Optimize Fan Curve for OLED", user_data="OLED_Mariko", callback=set_ini_from_profile)

    dpg.add_slider_int(
        label="Skin Target (Recommended - 54°C)",
        min_value=50, max_value=60,
        default_value=skinTarget,
        callback=update_skin_target
    )
    dpg.add_button(label="Reset Fan Curve", callback=remove_tc_entries)

    dpg.add_separator(label="Battery")
    dpg.add_button(
        label="What is this?",
        callback=common.show_info_window,
        user_data="This option fixes battery life drain in sleep mode\nDO NOT use this if you are using online services",
        tag="battery_fix_info"
    )
    dpg.add_button(label="Enable sleep mode battery fix", tag="enable_battery_fix", callback=toggle_battery_save, user_data=1)
    dpg.add_button(label="Disable sleep mode battery fix", tag="disable_battery_fix",callback=toggle_battery_save, user_data=0)

    dpg.add_separator(label="Downloads")



    nx_ovlloader_link = "https://github.com/ppkantorski/nx-ovlloader/releases/latest/download/nx-ovlloader+.zip"
    dpg.add_button(label="Install nx-ovlloader", callback=lambda: ins.download_and_extract_zip(common, nx_ovlloader_link, zip_filename="ovll_temp.zip", success_message="Installed nx-ovlloader!"))

    ultrahand_link = "https://github.com/ppkantorski/Ultrahand-Overlay/releases/latest/download/ovlmenu.ovl"
    dpg.add_button(label="Install Ultrahand Overlay", callback=lambda: ins.download_and_install(c=common, install_path=common.drive + "switch/.overlays/", download_url=ultrahand_link, filename="ovlMenu.ovl", success_message="Installed Ultrahand!"))

    status_monitor_link = "https://github.com/ppkantorski/Status-Monitor-Overlay/releases/latest/download/ Status-Monitor-Overlay.ovl "
    dpg.add_button(label="Install Status Monitor", callback=lambda: ins.download_and_install(c=common, install_path=common.drive + "switch/.overlays/", download_url=status_monitor_link, filename=" Status-Monitor-Overlay.ovl", success_message="Installed Status Monitor!"))

    saltynx_link = "https://github.com/masagrator/SaltyNX/releases/latest/download/SaltyNX.zip"
    dpg.add_button(label="Install SaltyNX", callback=lambda: ins.download_and_extract_zip(common, saltynx_link, zip_filename="saltynx_temp.zip", success_message="Installed SaltyNX!"))

    reversenx_link = "https://github.com/masagrator/ReverseNX-RT/releases/latest/download/ReverseNX-RT-ovl.ovl"
    dpg.add_button(label="Install ReverseNX-RT", callback=lambda: ins.download_and_install(c=common, install_path=common.drive + "switch/.overlays/", download_url=reversenx_link, filename="ReverseNX-RT-ovl.ovl", success_message="Installed ReverseNX-RT!"))

    status_monitor_link = "https://github.com/ppkantorski/Status-Monitor-Overlay/releases/latest/download/ Status-Monitor-Overlay.ovl "
    dpg.add_button(label="Install Status Monitor", callback=lambda: ins.download_and_install(c=common, install_path=common.drive + "switch/.overlays/", download_url=status_monitor_link, filename=" Status-Monitor-Overlay.ovl", success_message="Installed Status Monitor!"))

    dpg.add_separator(label="Danger Zone")

    dpg.add_text("These options are known to cause hardware issues, PMIC issues or overheating.\nUse with extreme caution!", color=(255, 165, 0, 255))

    dpg.add_separator()

    dpg.add_spacer(height=10)

    psm_items = [x["name"] for x in PSM_OPTIONS]
    dpg.add_combo(items=psm_items, label="Battery Charge Limit", callback=set_psm_value, tag="psm_dropdown", default_value="2048mA (Default)")
    dpg.add_spacer(height=5)

    dpg.add_separator(label="EXTREME DANGER ZONE")
    dpg.add_text("THESE OPTIONS ARE KNOWN TO CAUSE IRREPARABLE HARDWARE DAMAGE THAT CAN AND WILL KILL YOUR CONSOLE\nUSE ONLY IF YOU ARE AN ADVANCED USER AND ARE AWARE OF THE RISKS AND POTENTIAL CONCEQUENCES", color=(255, 0, 0, 255))
    dpg.add_spacer(height=10)
    with dpg.group(horizontal=True):
        dpg.add_checkbox(
            label="",
            callback=set_white_tiger_clocks
        )
        dpg.add_image("coolerhd", width=20, height=20)

def set_white_tiger_clocks(app_data):
    # cooler aah clocks
    # 1400mv emc max
    # 1375mv cpu max
    # 750mv vdd2 mariko max
    base_vddq_uv = [
        0, 550000, 555000, 560000, 565000, 570000, 575000, 580000,
        585000, 590000, 595000, 600000, 605000, 610000, 615000,
        620000, 625000, 630000, 635000, 640000, 645000, 650000
    ]

    vddq_uv = [0] + list(range(250000, 750001, 5000)) if app_data else base_vddq_uv
    vddq_mv = [v // 1000 for v in vddq_uv]
    vddq_mv_label = ["Default (600 mV)" if f == 0 else f"{f} mV" for f in vddq_mv]
    dpg.configure_item("marikoEmcVddqVolt", items=vddq_mv_label)

    base_voltages_uv = [
        0, 1050000, 1062500, 1075000, 1087500, 1100000, 1112500, 1125000,
        1137500, 1150000, 1162500, 1175000, 1187500, 1200000, 1212500, 1237500
    ]
    voltages_uv = base_voltages_uv + list(range(1225000, 1400000 + 1, 12500)) if app_data else base_voltages_uv
    voltages_mv = [v / 1000 for v in voltages_uv]
    voltages_mv_label = ["Default (1175 mV)" if f == 0 else f"{f} mV" for f in voltages_mv]
    dpg.configure_item("commonEmcMemVolt", items=voltages_mv_label)

    voltages = [0] + list(range(1130, 1375 + 1, 5)) if app_data else [0] + list(range(1000, 1160 + 1, 5))
    voltages_e = [0] + list(range(1180, 1375 + 1, 5)) if app_data else [0] + list(range(1120, 1255 + 1, 5)) + [1257]
    processed_voltages_e = ["Disabled" if v == 0 else f"{v}mV" for v in voltages_e]
    processed_voltages = ["Disabled" if v == 0 else f"{v}mV" for v in voltages]
    dpg.configure_item("marikoCpuMaxVolt", items=processed_voltages)
    dpg.configure_item("eristaCpuMaxVolt", items=processed_voltages_e)
