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
import sys
import platform
import common as c
import license

def populate():
    dpg.add_text("Horizon OC Configurator")
    dpg.add_separator(label="Contributors")

    with dpg.group(horizontal=True):
        dpg.add_image("soul", width=96, height=96)
        dpg.add_image("lightos", width=96, height=96)
        dpg.add_image("samy", width=96, height=96)

    dpg.add_separator()

    dpg.add_text("Souldbminer - Main contributor. Wrote the full configurator")
    dpg.add_text("Lightos - Dumped L4T Timings")
    dpg.add_text("Lightos, Samybigio, Flopsider - Testers")

    dpg.add_separator(label="Information")

    dpg.add_text(f"Configurator Version {c.version}")
    dpg.add_text(f"Current Python Version: {sys.version}")
    dpg.add_text(f"Current DearPyGui Version: {dpg.get_major_version()}.{dpg.get_minor_version()}")
    dpg.add_text(f"Current OS Version: {platform.system()} {platform.release()} Build {platform.version()}")

    dpg.add_button(label="Debug Mode", callback=lambda: dpg.show_debug())
    dpg.add_button(label="License", callback=lambda: c.show_popup_big("License (GPLv2-or-later)", license.gplv2_text))


