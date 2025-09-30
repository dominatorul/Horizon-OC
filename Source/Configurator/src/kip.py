import dearpygui.dearpygui as dpg
import struct
from defaults import d
import common as c
import gpu as g
import cpu
import defaults as df
import re
import ctypes

g_freq_str = None
kip_file_path = None

variables = [
    ("custRev", "u32"),
    ("mtcConf", "u32"),
    ("commonCpuBoostClock", "u32"),
    ("commonEmcMemVolt", "u32"),
    ("eristaCpuMaxVolt", "u32"),
    ("eristaEmcMaxClock", "u32"),
    ("marikoCpuMaxVolt", "u32"),
    ("marikoEmcMaxClock", "u32"),
    ("marikoEmcVddqVolt", "u32"),
    ("marikoCpuUV", "u32"),
    ("marikoGpuUV", "u32"),
    ("eristaCpuUV", "u32"),
    ("eristaGpuUV", "u32"),
    ("enableMarikoGpuUnsafeFreqs", "u32"),
    ("enableEristaGpuUnsafeFreqs", "u32"),
    ("enableMarikoCpuUnsafeFreqs", "u32"),
    ("enableEristaCpuUnsafeFreqs", "u32"),
    ("commonGpuVoltOffset", "u32"),
    ("marikoEmcDvbShift", "u32"),
    # advanced config
    ("t1_tRCD", "u32"),
    ("t2_tRP", "u32"),
    ("t3_tRAS", "u32"),
    ("t4_tRRD", "u32"),
    ("t5_tRFC", "u32"),
    ("t6_tRTW", "u32"),
    ("t7_tWTR", "u32"),
    ("t8_tREFI", "u32"),
    ("mem_burst_latency", "u32"),

    ("g_volt_76800", "u32"),
    ("g_volt_153600", "u32"),
    ("g_volt_230400", "u32"),
    ("g_volt_307200", "u32"),
    ("g_volt_384000", "u32"),
    ("g_volt_460800", "u32"),
    ("g_volt_537600", "u32"),
    ("g_volt_614400", "u32"),
    ("g_volt_691200", "u32"),
    ("g_volt_768000", "u32"),
    ("g_volt_844800", "u32"),
    ("g_volt_921600", "u32"),
    ("g_volt_998400", "u32"),
    ("g_volt_1075200", "u32"),
    ("g_volt_1152000", "u32"),
    ("g_volt_1228800", "u32"),
    ("g_volt_1267200", "u32"),
    ("g_volt_1305600", "u32"),
    ("g_volt_1344000", "u32"),
    ("g_volt_1382400", "u32"),
    ("g_volt_1420800", "u32"),
    ("g_volt_1459200", "u32"),
    ("g_volt_1497600", "u32"),
    ("g_volt_1536000", "u32"),

    
    ("g_volt_e_76800", "u32"),
    ("g_volt_e_153600", "u32"),
    ("g_volt_e_230400", "u32"),
    ("g_volt_e_307200", "u32"),
    ("g_volt_e_384000", "u32"),
    ("g_volt_e_460800", "u32"),
    ("g_volt_e_537600", "u32"),
    ("g_volt_e_614400", "u32"),
    ("g_volt_e_691200", "u32"),
    ("g_volt_e_768000", "u32"),
    ("g_volt_e_844800", "u32"),
    ("g_volt_e_921600", "u32"),
    ("g_volt_e_998400", "u32"),
    ("g_volt_e_1075200", "u32"),
#    ("g_volt_e_1152000", "u32"),
#    ("g_volt_e_1228800", "u32"),
    ("marikoCpuVmin", "u32"),
    ("eristaGpuVmin", "u32"),
    ("marikoGpuVmin", "u32"),
    ("marikoGpuVmax", "u32"),

]

fmt_map = {
    "u32": "I",
    "double": "d",
}

def make_struct_format(vars_list):
    fmt = "="
    for name, t in vars_list:
        fmt += fmt_map[t]
        if name == "tFAW":
            fmt += "4x"  # i hate hardcoding but this is what it is
    return fmt

def load_all_vars():
    c.load_entry_object("custRev", 0)
    c.load_entry_object("mtcConf", 0)
    c.load_entry_object("commonCpuBoostClock", 1)
    c.load_entry_object("commonEmcMemVolt", 2)
    c.load_entry_object("eristaCpuMaxVolt", 3)
    c.load_entry_object("eristaEmcMaxClock", 1)
    c.load_entry_object("marikoCpuMaxVolt", 3)
    c.load_entry_object("marikoEmcMaxClock", 1)
    c.load_entry_object("marikoEmcVddqVolt", 2)
    c.load_entry_object("marikoCpuUV", 5)
    c.load_entry_object("marikoGpuUV", 4)
    c.load_entry_object("eristaCpuUV", 5)
    c.load_entry_object("eristaGpuUV", 4)
    c.load_entry_object("enableMarikoGpuUnsafeFreqs", 0)
    c.load_entry_object("enableEristaGpuUnsafeFreqs", 0)
    c.load_entry_object("enableMarikoCpuUnsafeFreqs", 0)
    c.load_entry_object("enableEristaCpuUnsafeFreqs", 0)
    c.load_entry_object("commonGpuVoltOffset", 3)
    c.load_entry_object("marikoEmcDvbShift", 0)

    # Advanced memory config
    c.load_entry_object("t1_tRCD", 5)
    c.load_entry_object("t2_tRP", 5)
    c.load_entry_object("t3_tRAS", 5)
    c.load_entry_object("t4_tRRD", 5)
    c.load_entry_object("t5_tRFC", 5)
    c.load_entry_object("t6_tRTW", 5)
    c.load_entry_object("t7_tWTR", 5)
    c.load_entry_object("t8_tREFI", 5)
    c.load_entry_object("mem_burst_latency", 5)
    # GPU voltage arrays
    for freq in [
        "76800", "153600", "230400", "307200", "384000", "460800", "537600",
        "614400", "691200", "768000", "844800", "921600", "998400", "1075200",
        "1152000", "1228800", "1267200", "1305600", "1344000", "1382400",
        "1420800", "1459200", "1497600", "1536000"
    ]:
        c.load_entry_object(f"g_volt_{freq}", 3)

    for e_freq in [
        "76800", "153600", "230400", "307200", "384000", "460800", "537600",
        "614400", "691200", "768000", "844800", "921600", "998400", "1075200"# ,
        # "1152000", "1228800"
    ]:
        c.load_entry_object(f"g_volt_e_{e_freq}", 3)
    c.load_entry_object("marikoCpuVmin", 3)
    c.load_entry_object("eristaGpuVmin", 3)
    c.load_entry_object("marikoGpuVmin", 3)
    c.load_entry_object("marikoGpuVmax", 3)

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
    load_all_vars()

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
    struct_fmt = make_struct_format(variables)
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
        for attr_name, t in variables:
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
    struct_fmt = make_struct_format(variables)
    struct_size = struct.calcsize(struct_fmt)
    with open(filename, "rb") as f:
        data = f.read()
        idx = data.find(MAGIC)
        if idx == -1:
            c.show_popup("Fatal Error", "Unable to find CUST header in kip\nTry reinstalling the kip using the install option")
        pos = idx + len(MAGIC)
        raw = data[pos:pos + struct_size]
        values = struct.unpack(struct_fmt, raw)
        for (attr_name, _), val in zip(variables, values):
            setattr(d, attr_name, val)
        print("=== value layout ===")
        offset = 0
        for (attr_name, t) in variables:
            code = fmt_map[t]
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