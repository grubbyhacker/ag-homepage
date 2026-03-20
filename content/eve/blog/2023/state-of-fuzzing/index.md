---
title: The State of Fuzzing in 2023
date: '2023-06-11'
draft: false
tags:
- security
- programming
- linux
summary: Why AFL++ is still the king, and where symbolic execution falls short.
---

Fuzzing is the most brutally effective way to find memory corruption bugs in large C/C++ codebases. Period.

While academic papers love symbolic execution, nothing beats the throughput of a well-instrumented generational fuzzer like AFL++. You just throw CPU cycles at the problem until a segfault shakes out.

{{< highlight-file name="harness.c" lang="c" >}}
#include <stdint.h>
#include <stddef.h>

int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
  // Your target API here
  ParseImage(Data, Size);
  return 0;
}
{{< /highlight-file >}}

If you haven't fuzzed your parser, it is vulnerable.