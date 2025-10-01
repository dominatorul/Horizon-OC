import os
import re
import common as c

def ensure_dir_exists(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def set_ini_values(ini_path, section, entries):
    if not c.drive:
        c.show_popup("Error", "This feature requires a valid drive to be selected")
        return

    ini_path = str(ini_path)

    try:
        with open(ini_path, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []

    output_lines = []
    current_section = None
    section_lines = []
    section_found = False

    def flush_section():
        nonlocal section_lines, output_lines
        if section_lines:
            output_lines.extend(section_lines)
            section_lines = []

    for line in lines:
        section_match = re.match(r"\s*\[([^\]]+)\]", line)
        if section_match:
            if current_section == section and entries:
                new_lines = []
                keys_handled = set()
                for l in section_lines[1:]:
                    key_match = re.match(r"\s*([A-Za-z0-9_.]+)\s*=", l)
                    if key_match:
                        key = key_match.group(1)
                        if key in entries:
                            val = entries[key]
                            if val is None:
                                continue
                            new_lines.append(f"{key} = {val}\n")
                            keys_handled.add(key)
                        else:
                            new_lines.append(l)
                    else:
                        new_lines.append(l)
                for k, v in entries.items():
                    if k not in keys_handled and v is not None:
                        new_lines.append(f"{k} = {v}\n")
                section_lines = [section_lines[0]] + new_lines
            flush_section()
            current_section = section_match.group(1)
            section_lines = [line]
            if current_section == section:
                section_found = True
            continue
        section_lines.append(line)

    if current_section == section and entries:
        new_lines = []
        keys_handled = set()
        for l in section_lines[1:]:
            key_match = re.match(r"\s*([A-Za-z0-9_.]+)\s*=", l)
            if key_match:
                key = key_match.group(1)
                if key in entries:
                    val = entries[key]
                    if val is None:
                        continue
                    new_lines.append(f"{key} = {val}\n")
                    keys_handled.add(key)
                else:
                    new_lines.append(l)
            else:
                new_lines.append(l)
        for k, v in entries.items():
            if k not in keys_handled and v is not None:
                new_lines.append(f"{k} = {v}\n")
        section_lines = [section_lines[0]] + new_lines

    flush_section()

    if not section_found and entries:
        output_lines.append(f"\n[{section}]\n")
        for k, v in entries.items():
            if v is not None:
                output_lines.append(f"{k} = {v}\n")

    ensure_dir_exists(ini_path)

    if output_lines:
        with open(ini_path, "w") as f:
            f.writelines(output_lines)
    else:
        if os.path.exists(ini_path):
            os.remove(ini_path)
