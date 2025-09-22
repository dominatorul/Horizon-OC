<div align="center">


![alt text](assets/logo.png "logo")


![alt text](https://img.shields.io/badge/GPL--2.0-red?style=for-the-badge "logo") ![alt text](https://img.shields.io/badge/Nintendo_Switch-E60012?style=for-the-badge&logo=nintendo-switch&logoColor=white "logo") [![alt text](https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/invite/S3eX47dHsB)  ![alt text](https://img.shields.io/badge/VSCode-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white) ![alt text](https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white)

</div>

##### DISCLAIMER: THIS TOOL CAN BE DANGEROUS IF MISUSED. PROCEED WITH CAUTION
* Due to the design of Horizon OS, overclocking RAM can cause **NAND DAMAGE**. Ensure to have a NAND Backup

A open source overclocking tool for Nintendo Switch consoles running Atmosphere custom firmware


## Features:
CPU overclock up to 2601MHz on Mariko units, 2091MHz on Erista units
GPU up to 1382MHz on Mariko units, 1075MHz on Erista units
RAM up to 3200MHz on Mariko units, 2250MHz on Erista units
Over/undervolting
Configurator
Works with most homebrew

*Higher (potentially dangerous) frequencies are unlockable*
## Installation
Grab latest hoc.kip from releases tab
If using hekate, edit hekate_ipl.ini to include "kip1=atmosphere/kips/*". No need for editing if using fusee
Download latest Horizon OC sysmodule from releases tab
Extract sysmodule into root of SD card

Ensure you are using latest Atmosphere, otherwise the console will not boot

## Building
Set up a development enviorment ready to compile Atmosphere
Git clone Atmosphere, and move the cloned folder into build/
Insert Source/stratosphere folder into build/
Run build.sh

## Credits
meha for Switch-Oc-Suite
sys-clk team for sys-clk
b0rd2auth for Ultrahand sys-clk fork
Lightos and Sammybigio2010 for early testing