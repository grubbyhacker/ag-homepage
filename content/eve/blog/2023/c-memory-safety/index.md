---
title: C memory safety will never happen
date: '2023-11-20'
draft: false
tags:
- programming
- security
summary: Temporal safety cannot be bolted onto C retroactively.
---

Spatial memory safety in C (bounds checking) is extremely difficult but theoretically possible with hardware assistance like ARM MTE.

Temporal memory safety (use-after-free) in C is fundamentally impossible without massive performance overhead or a different language paradigm altogether.

Stop writing new network-facing parsers in C. It is professional negligence in the modern era.