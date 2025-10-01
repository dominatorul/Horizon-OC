import dearpygui.dearpygui as dpg
import struct
from defaults import d
import common as c
import gpu as g
import re
import settings as s

g_freq_str = None
kip_file_path = None


def make_struct_format(vars_list):
    fmt = "="
    for name, t in vars_list:
        fmt += s.fmt_map[t]
        if name == "tFAW":
            fmt += "4x"  # i hate hardcoding but this is what it is
    return fmt



def freq_to_label(freq):
    if freq > 1382400:
        return f"{freq / 1000:.1f} MHz (DANGEROUS)"
    elif freq > 1152000:
        return f"{freq / 1000:.1f} MHz (UNSAFE)"
    else:
        return f"{freq / 1000:.1f} MHz"

def store(sender, app_data):
    global kip_file_path
    kip_file_path = app_data['file_path_name']
    print("Selected" + kip_file_path)
    read_kip(kip_file_path)
    s.load_all_vars()

def grab_kip_storage_values(sender, app_data):
    tag = dpg.get_item_alias(sender)
    if tag and hasattr(d, tag):
        numeric_str = str(app_data).split(" ")[0]
        try:
            value = int(float(numeric_str) * 1000)
        except (ValueError, TypeError):
            c.show_popup("Error", f"Invalid numeric value for {tag}: {app_data}")
            return
        setattr(d, tag, value)
    print(tag, app_data, getattr(d, tag))
    if d.autosave:
        write_kip()

def grab_kip_storage_values_no_mult(sender, app_data):
    tag = dpg.get_item_alias(sender)
    if not tag or not hasattr(d, tag):
        return
    if isinstance(app_data, str):
        numeric_str = re.sub(r"[^0-9.]", "", app_data)
        if numeric_str == "":
            c.show_popup("Error", f"Invalid numeric value for {tag}: {app_data}")
            return
        try:
            value = int(float(numeric_str))
        except (ValueError, TypeError):
            c.show_popup("Error", f"Invalid numeric value for {tag}: {app_data}")
            return
    else:
        value = app_data
    setattr(d, tag, value)
    print(tag, app_data, getattr(d, tag))
    if d.autosave:
        write_kip()

def grab_value_freq_conversion(sender, app_data):
    global g_freq_str
    g_freq_str = app_data
    try:
        g_freq_val = int(float(g_freq_str.replace(" MHz", "")) * 1000)
    except Exception:
        return
    print(g_freq_val)

def write_kip():
    global kip_file_path
    MAGIC = b"CUST"
    struct_fmt = make_struct_format(s.variables)
    struct_size = struct.calcsize(struct_fmt)
    if kip_file_path is None:
        msg = "You need to select a file to use Autosave!" if d.autosave else "You need to select a file to save the KIP!"
        c.show_popup("Error", msg)
        return
    with open(kip_file_path, "r+b") as f:
        data = f.read()
        idx = data.find(MAGIC)
        if idx == -1:
            c.show_popup("Error", "KIP is invalid!")
            return
        pos = idx + len(MAGIC)
        values = []
        for attr_name, t in s.variables:
            val = getattr(d, attr_name)
            if t == "u32":
                val = int(val) & 0xFFFFFFFF
            else:
                val = float(val)
            values.append(val)
        try:
            packed = struct.pack(struct_fmt, *values)
        except Exception as e:
            c.show_popup("Error", f"Packing error: {e}")
            return
        f.seek(pos)
        f.write(packed)
    if not d.autosave:
        c.show_popup("Success", "KIP saved successfully!")

def read_kip(filename):
    MAGIC = b"CUST"
    struct_fmt = make_struct_format(s.variables)
    struct_size = struct.calcsize(struct_fmt)
    with open(filename, "rb") as f:
        data = f.read()
        idx = data.find(MAGIC)
        if idx == -1:
            c.show_popup("Fatal Error", "Unable to find CUST header in kip\nTry reinstalling the kip using the install option")
        pos = idx + len(MAGIC)
        raw = data[pos:pos + struct_size]
        values = struct.unpack(struct_fmt, raw)
        for (attr_name, _), val in zip(s.variables, values):
            setattr(d, attr_name, val)
        print("=== value layout ===")
        offset = 0
        for (attr_name, t) in s.variables:
            code = s.fmt_map[t]
            align = 8 if code == "d" else 4
            padding = (-offset) % align
            if padding:
                offset += padding
            size = struct.calcsize(code)
            raw_bytes = raw[offset:offset + size]
            val = getattr(d, attr_name)
            print(f"{attr_name:<20} | type={t:<6} | offset={offset:<4} | size={size:<2} | raw=0x{raw_bytes.hex()} | val={val}")
            offset += size
        print("========================")
    dpg.set_value("gpu_sched", g.check_gpu_sched())
    dpg.show_item("gpu_tab")
    dpg.show_item("cpu_tab")
    dpg.show_item("emc_tab")
    dpg.show_item("misc_tab")