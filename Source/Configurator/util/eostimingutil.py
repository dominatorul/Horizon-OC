import json
import dearpygui.dearpygui as dpg
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

timings = {
    "tRCD": "mariko/ram_trcd.json",
    "tRP": "mariko/ram_trp.json",
    "tRAS": "mariko/ram_tras.json",
    "tRRD": "mariko/ram_trrd.json",
    "tRFC": "mariko/ram_trfc.json",
    "tRTW": "mariko/ram_trtw.json",
    "tWTR": "mariko/ram_twtr.json",
    "tREFI": "mariko/ram_trefi.json"
}

timing_data = {}
for timing_name, rel_path in timings.items():
    path = os.path.join(BASE_DIR, rel_path)
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                raw = json.load(f)
                steps = {}
                if isinstance(raw, list):
                    for i, entry in enumerate(raw):
                        if isinstance(entry, dict) and "name" in entry:
                            steps[i] = entry["name"].strip()
                        else:
                            steps[i] = str(entry)
                elif isinstance(raw, dict):
                    for k, entry in raw.items():
                        if isinstance(entry, dict) and "name" in entry:
                            steps[int(k)] = entry["name"].strip()
                        else:
                            steps[int(k)] = str(entry)
                timing_data[timing_name] = steps
        except Exception as e:
            print(f"Error loading {path}: {e}")
            timing_data[timing_name] = {}
    else:
        print(f"Missing file: {path}")
        timing_data[timing_name] = {}

def update_slider_label(sender, app_data, user_data):
    timing_name = user_data
    step = int(app_data)
    name_value = timing_data[timing_name].get(step, "(no name)")
    new_label = f"{timing_name}: {name_value}"
    dpg.set_item_label(sender, new_label)

# --- GUI ---
dpg.create_context()
dpg.create_viewport(title="EOS Real Timings", width=600, height=500)

with dpg.window(label="Timings", width=580, height=480, tag="main"):
    dpg.add_text("Select timings")
    for timing_name, steps in timing_data.items():
        if steps:
            max_step = max(steps.keys())
            current_name = steps.get(0, "")
            dpg.add_slider_int(
                label=f"{timing_name}: {current_name}",
                min_value=0,
                max_value=max_step,
                default_value=0,
                callback=update_slider_label,
                user_data=timing_name,
                width=400
            )
        else:
            dpg.add_text(f"{timing_name}: (JSON not found or invalid)")
dpg.set_primary_window("main", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
