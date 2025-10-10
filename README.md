<div align="center">

<!-- 🌌 Banner / Title -->
<h1 align="center">
  <img src="assets/logo.png" alt="logo" width="120"/><br>
  <span style="font-size: 2.5rem; background: linear-gradient(90deg, #E60012, #5865F2, #0078D4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
    Horizon OC
  </span>
</h1>

<p align="center">
  <i>Advanced Open Source Overclocking Tool for Nintendo Switch (Atmosphere CFW)</i>
</p>

---

<!-- 🏷️ Badges -->
![License: GPL-2.0](https://img.shields.io/badge/GPL--2.0-red?style=for-the-badge)
![Nintendo Switch](https://img.shields.io/badge/Nintendo_Switch-E60012?style=for-the-badge&logo=nintendo-switch&logoColor=white)
[![Discord](https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/invite/S3eX47dHsB)
![VSCode](https://img.shields.io/badge/VSCode-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)
![C++](https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white)
![Downloads](https://img.shields.io/github/downloads/souldbminersmwc/Horizon-OC/total.svg?style=for-the-badge)

---

</div>

## ⚠️ Disclaimer

> **THIS TOOL CAN BE DANGEROUS IF MISUSED. PROCEED WITH CAUTION.**  
> Overclocking RAM can cause **NAND DAMAGE** due to Horizon OS design.  
> Always ensure you have a **full NAND backup** before proceeding.

---

## 🌀 About

**Horizon OC** is an **open-source overclocking suite** for Nintendo Switch consoles running **Atmosphere** custom firmware.  
It provides safe and flexible control over CPU, GPU, and RAM frequencies, with a modern configuration utility.

---

## 🚀 Features

✅ CPU up to **2397MHz** (Mariko) / **2091MHz** (Erista)  
✅ GPU up to **1305MHz** (Mariko) / **998MHz** (Erista)  
✅ RAM up to **3200MHz** (Mariko) / **2360MHz** (Erista)  
✅ Overclock & undervolt support  
✅ Built-in configuration tool  
✅ Compatible with most homebrew  

> ⚡ *Higher (potentially dangerous) frequencies are unlockable.*  
> ⚙️ *Exact maximums vary per console.*

---

## 🧩 Installation

1. Install the latest versions of:  
   - [Atmosphere](https://github.com/Atmosphere-NX/Atmosphere)  
   - [Ultrahand Overlay](https://github.com/ppkantorski/Ultrahand-Overlay)

2. Download the latest `hoc.kip` from the [Releases](../../releases) tab.  
3. If using **Hekate**, edit `hekate_ipl.ini`:
   ```ini
   kip1=atmosphere/kips/*
````

*(No edits needed if using fusee.)*

4. Download and extract the **Horizon OC sysmodule** to your SD card root.
5. Optionally, use the **Configurator** to install automatically via GUI.

---

## ⚙️ Configuration

1. Download the **Configurator** on your PC.
2. Run the executable.
3. Select your SD card or UMS device.
4. Adjust frequency settings.
5. Click **Save** to apply your configuration.

---

## 🧱 Building from Source

1. Set up a build environment for **Atmosphere**.
2. Clone the repo:

   ```bash
   git clone https://github.com/Atmosphere-NX/Atmosphere.git
   ```
3. Move it into the `build/` folder.
4. Copy your `Source/stratosphere` folder into `build/`.
5. Build with:

   ```bash
   ./build.sh
   ```

**Build the Configurator:**

```bash
cd Source/Configurator
build.bat
# or
python -m PyInstaller --onefile --add-data "assets;assets" --icon=assets/icon.ico --noconsole src/main.py
```

---

## 💎 Credits

| Contributor                     | Contribution           |
| ------------------------------- | ---------------------- |
| **Lightos**, **Dominatorul**    | RAM timings            |
| **KazushiMe**, **meha**         | Switch-OC-Suite        |
| **sys-clk team**                | sys-clk base           |
| **b0rd2death**                  | Ultrahand sys-clk fork |
| **Lightos**, **Sammybigio2011** | Early testing          |

---

<div align="center">

💻 *Built with ❤️ by the Horizon OC community* <br>
⭐ Star this repo if you find it useful!

</div>
