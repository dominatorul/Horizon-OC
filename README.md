<div align="center">


![alt text](assets/logo.png "logo")


![alt text](https://img.shields.io/badge/GPL--2.0-red?style=for-the-badge "logo") ![alt text](https://img.shields.io/badge/Nintendo_Switch-E60012?style=for-the-badge&logo=nintendo-switch&logoColor=white "logo") [![alt text](https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/invite/S3eX47dHsB)  ![alt text](https://img.shields.io/badge/VSCode-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white) ![alt text](https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white) [![Github All Releases](https://img.shields.io/github/downloads/souldbminersmwc/Horizon-OC/total.svg)]()

</div>

### DISCLAIMER: THIS TOOL CAN BE DANGEROUS IF MISUSED. PROCEED WITH CAUTION
* Due to the design of Horizon OS, overclocking RAM can cause **NAND DAMAGE**. Ensure to have a NAND Backup<br>

A open source overclocking tool for Nintendo Switch consoles running Atmosphere custom firmware<br>


## Features:
CPU overclock up to 2397MHz on Mariko units, 2091MHz on Erista units<br>
GPU up to 1305MHz on Mariko units, 998MHz on Erista units<br>
RAM up to 3200MHz on Mariko units, 2360MHz on Erista units<br>
Over/undervolting<br>
Configurator<br>
Works with most homebrew<br>

*Higher (potentially dangerous) frequencies are unlockable*<br>
*The exact maximum overclock varies per console*<br>
## Installation
Ensure you have the latest version of [Atmosphere](https://github.com/Atmosphere-NX/Atmosphere) and [Ultrahand](https://github.com/ppkantorski/Ultrahand-Overlay) installed before continuing<br>
Grab latest hoc.kip from releases tab<br>
If using hekate, edit hekate_ipl.ini to include "kip1=atmosphere/kips/*". No need for editing if using fusee<br>
Download latest Horizon OC sysmodule from releases tab<br>
Extract sysmodule into root of SD card<br>

Alternatively, you can download the configurator and click the two install buttons<br>


## Configuration
Download the latest configurator on your computer<br>
Run the file<br>
Select the drive your SD card or UMS device is mounted as<br>
Configure the kip to your liking, and in the end, save it<br>

## Building
Set up a development enviorment ready to compile Atmosphere<br>
Git clone Atmosphere, and move the cloned folder into build/<br>
Insert Source/stratosphere folder into build/<br>
Run build.sh

To build the configurator, clone it's repo (souldbminersmwc/ocs2-configurator)<br>
Run build.bat or cd into folder and run "python -m PyInstaller --onefile --add-data "assets;assets" --icon=assets/icon.ico --noconsole src/main.py"<br>


## Credits
meha for Switch-Oc-Suite<br>
sys-clk team for sys-clk<br>
b0rd2death for Ultrahand sys-clk fork<br>
Lightos and Sammybigio2011 for early testing<br>
