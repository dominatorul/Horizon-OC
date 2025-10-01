
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
import psutil
import os
import common as c
import urllib.request
import zipfile
import kip as k
from defaults import d
import settings as s

def autosave_toggle(sender, app_data):
    d.autosave=app_data
    print(f"Autosave toggled to {d.autosave}")


def get_drives():
    drives = []
    for part in psutil.disk_partitions(all=False):
        drives.append(part.device)
    return drives


# Change if you plan to fork

def download_and_extract_zip(c, download_url, zip_filename="temp.zip", success_message="Installed file!"):
    """
    Downloads a zip file from the given URL, extracts it to the selected drive, 
    and cleans up the zip afterwards.

    Args:
        c: Context object with attributes:
            - drive (str): Installation path.
            - show_popup (callable): Function to show popup messages.
        download_url (str): The URL of the zip file.
        zip_filename (str, optional): Name for the downloaded zip file. Defaults to "temp.zip".
        success_message (str, optional): Success popup message. Defaults to "Installed hoc-clk!".
    """

    if not c.drive or c.drive == "0" or c.drive == 0:
        c.show_popup(title="Error", content="Please select an installation drive first!")
        return False

    zip_path = os.path.join(c.drive, zip_filename)

    try:
        print(f"Downloading {zip_filename} to {c.drive} ...")
        urllib.request.urlretrieve(download_url, zip_path)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(c.drive)

        c.show_popup(title="Success", content=success_message)
        return True

    except Exception as e:
        c.show_popup(title="Error", content=f"Download failed:\n{e}")
        return False

    finally:
        if os.path.exists(zip_path):
            os.remove(zip_path)

def downloadLoader(): # This has to be different as it extracts to a custom location and downloads a FILE, not a zip
    print("Downloading HOC.kip...")
    if c.drive==0:
        print("Drive not selected!")
        c.show_popup(title="Error:", content="Please select a installation c.drive first!")
    else:
        try:
            directory_make = c.drive + "atmosphere/kips/"
            urllib.request.urlretrieve(s.kip_download_link, directory_make + "hoc.kip")
        except Exception as e:
            c.show_popup(title="Error", content=f"Download failed:\n{e}")
        finally:
            c.show_popup(title="Info:", content="Downloaded kip!")
    
drive_list = get_drives()

def check_atmosphere(sender, app_data, user_data):
    c.drive = app_data
    atmosphere_path = os.path.join(c.drive, "atmosphere")
    package3_path = os.path.join(atmosphere_path, "package3")
    if os.path.isfile(f"{atmosphere_path}/kips/hoc.kip"):
        dpg.set_value("status_text", "Horizon OC Install Found!")
        k.kip_file_path = f"{atmosphere_path}/kips/hoc.kip"
        k.read_kip(c.drive + "atmosphere/kips/hoc.kip")
        print(f"Reading kip from drive {c.drive}")
        s.load_all_vars()
    elif os.path.isdir(atmosphere_path) and os.path.isfile(package3_path):
        dpg.set_value("status_text", "Atmosphere install found!")
    else:
        dpg.set_value("status_text", "Atmosphere not found!")

def download_and_install(download_url, install_path, c=None, 
                         filename=None, success_message="Download complete!"):
    """
    Downloads a file from the given URL, optionally extracts if it's a zip,
    and deletes the temporary zip afterwards if extracted.

    Args:
        download_url (str): The URL of the file.
        install_path (str): Directory where the file will be saved or extracted.
        c (object, optional): Context object with show_popup(title, content). If given, used for popups.
        filename (str, optional): Name for the downloaded file. Defaults to inferred name from URL.
        success_message (str, optional): Message shown on success.
    """

    def show_popup(title, content):
        if c and hasattr(c, "show_popup"):
            c.show_popup(title=title, content=content)
        else:
            print(f"[{title}] {content}")

    if not install_path or not os.path.isdir(install_path):
        msg = f"Invalid installation path: {install_path}"
        show_popup("Error", msg)
        return False

    # Infer filename if not provided
    if not filename:
        filename = os.path.basename(download_url) or "downloaded_file"

    file_path = os.path.join(install_path, filename)

    try:
        print(f"Downloading {filename} to {install_path} ...")
        urllib.request.urlretrieve(download_url, file_path)

        if filename.lower().endswith(".zip"):
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(install_path)
                show_popup("Success", success_message)
                return True
            except zipfile.BadZipFile:
                msg = f"Downloaded file '{filename}' is not a valid archive."
                show_popup("Error", msg)
                return False
            finally:
                if os.path.exists(file_path):
                    os.remove(file_path)
        else:
            # Non-zip file: just keep it
            show_popup("Success", success_message)
            return True

    except Exception as e:
        msg = f"Download failed: {e}"
        show_popup("Error", msg)
        return False