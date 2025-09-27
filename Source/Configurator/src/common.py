
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

drive = 0

version = "2.0.0"

def show_info_window(sender, app_data, user_data):
    window_tag = "info_window" + user_data
    if not dpg.does_item_exist(window_tag):
        with dpg.window(label="Information", tag=window_tag, width=400, height=200):
            wrap_width = dpg.get_item_width(window_tag) - 10
            dpg.add_text(user_data, wrap=wrap_width)
    else:
        dpg.show_item(window_tag)

def store_value(sender, app_data, user_data=None):
    var_name = f"{dpg.get_item_(sender)}_value"
    globals()[var_name] = app_data
    print(f"{var_name} = {app_data}")

def get_value(tag, default=None):
    var_name = f"{tag}_value"

    return globals().get(var_name, default)
def show_popup(title="Popup", content="Message"):
    if dpg.does_item_exist("popup_window"):
        dpg.delete_item("popup_window")

    with dpg.window(
        label=title,
        tag="popup_window",
        modal=True,
        no_close=True,
        width=150,
        height=150
    ):
        dpg.add_text(content, wrap=145)
        dpg.add_separator()
        dpg.add_button(label="Close", width=100, callback=lambda: dpg.delete_item("popup_window"))
def show_popup_big(title="Popup", content="Message"):
    if dpg.does_item_exist("big_popup_window"):
        dpg.delete_item("big_popup_window")

    with dpg.window(
        label=title,
        tag="big_popup_window",
        modal=True,
        no_close=True,
        width=500,
        height=500
    ):
        dpg.add_text(content, wrap=495)
        dpg.add_separator()
        dpg.add_button(label="Close", width=100, callback=lambda: dpg.delete_item("big_popup_window"))


def load_entry_object(var_name, flag=0):
    if not hasattr(d, var_name):
        print(f"Variable {var_name} not found in d.")
        return

    value = getattr(d, var_name)
    match flag:
        case 0:
            value_str = str(value)
        case 1:
            value_str = f"{value / 1000:.1f} MHz"
        case 2:
            if not value == 0:
                value_str = f"{value / 1000:.1f} mV"
            else:
                value_str = "Disabled"
        case 3:
            if not value == 0:
                value_str = f"{value} mV"
            else:
                value_str = "Disabled"
        case 4:
            match value:
                case 0:
                    value_str = "No Table (UV0)"
                case 1:
                    value_str = "Regular Table (UV1)"
                case 2:
                    value_str = "High Table (UV2)"
                case 3:
                    value_str = "Custom Table (UV3)"
        case 5:
            value_str = value

    if dpg.does_item_exist(var_name):
        dpg.set_value(var_name, value_str)
    else:
        print(f"Entry tagged '{var_name}' does not exist.")
