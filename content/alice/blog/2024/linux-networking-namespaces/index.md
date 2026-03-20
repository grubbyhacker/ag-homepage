---
title: Demystifying Linux Network Namespaces
date: '2024-03-22'
draft: false
tags:
- linux
- networking
- containers
summary: How Docker actually isolates your networks under the hood.
---

Containers aren't real. They are just processes with a very specific set of lies told to them by the Linux kernel. The most interesting of these lies is the Network Namespace.

When you create a docker container, you aren't booting a VM. You are just creating an isolated `netns`.

{{< warning title="Kernel Panics" >}}
Do not carelessly delete namespaces if you have active packet captures running on `veth` pairs inside them. Older kernels handle this poorly.
{{< /warning >}}

If you want to create a namespace manually, it's trivial:

{{< highlight-file name="terminal" lang="bash" >}}
ip netns add my_ns
ip netns exec my_ns ip link set lo up
{{< /highlight-file >}}

And just like that, you have an isolated network environment. We build entirely complex orchestrators around this fundamental primitive.