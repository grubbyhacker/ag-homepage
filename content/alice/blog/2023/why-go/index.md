---
title: Why We Migrated to Go
date: '2023-06-12'
draft: false
tags:
- programming
- go
summary: Reflections on our transition from C++ to Go for the control plane.
---

Two years ago, we made the controversial decision to halt all new feature development in our C++ codebase and rewrite the entire control plane load balancer in Go. 

It was painful. It was expensive. It was absolutely the right choice.

The biggest win wasn't execution speed—it was deployment velocity. Our compile times dropped from 45 minutes to 30 seconds. Onboarding a new engineer dropped from two months to two weeks. 

We sacrificed a marginal amount of CPU efficiency for a massive gain in developer throughput.