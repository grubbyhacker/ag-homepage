---
title: 'FPGA Emulation: The MiSTer Project'
date: '2023-11-30'
draft: false
tags:
- programming
- hardware
- retro
summary: Why cycle-accurate hardware emulation is replacing RetroArch.
---

Software emulation runs a program on your CPU that pretends to be a Super Nintendo. An FPGA (Field-Programmable Gate Array) is a blank microchip configured to physically wire itself into the exact logic gates of a Super Nintendo.

The MiSTer project uses an Altera Cyclone V FPGA to achieve cycle-accurate recreation of dozens of classic arcade and console cores.

There is zero input lag, because there is no OS scheduling overhead. It is a stunning triumph of reverse-engineering and open-source collaboration.