---
title: Introduction to Hardware Fault Injection
date: '2024-03-05'
draft: false
tags:
- security
- hardware
summary: Bypassing secure boot with precisely timed voltage glitches.
---

Software security assumes the hardware reliably executes the instructions it is given. Fault injection attacks (glitching) prove that this assumption is a lie.

If you drop the CPU core voltage for exactly 50 nanoseconds precisely when it's reading the 'SecureBoot=True' register, the CPU will read a 0 instead of a 1. 

{{< warning title="Bricked Devices" >}}
You will destroy hardware doing this. Buy spares. Don't glitch the only prototype.
{{< /warning >}}

It requires an oscilloscope, an FPGA, and a lot of patience. But seeing a root shell pop over UART on a locked device is pure magic.