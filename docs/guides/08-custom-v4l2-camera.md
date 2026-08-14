# Vector 8 — Custom V4L2 virtual camera

> [`NOTICE-EVALUATION.md`](../NOTICE-EVALUATION.md) · shared protocol: [`00-protocol.md`](00-protocol.md)

**Class:** motivated. **Property tested:** if a service rejects **common** software cameras (e.g. well-known streaming virtual-camera names), does it still accept a generic Video4Linux2 device that carries the same scene?

## What we measured (not how to build it)

One service in the set detected a typical desktop virtual camera and refused it. We then presented the **same composed scene** through a loopback V4L2 device whose advertised name was not that of a common streaming app.

This is an extension of the software-camera path, not a new stimulus: the independent variable is **how the device identifies itself**, not the face content.

## Scoring

Five trials, fresh session, success = adult/verified outcome. That service still failed this vector.

## What this artifact does not include

- Kernel-module install commands
- Device-creation flags, advertised names to use, or `ffmpeg`/pipe recipes
- How to hide or relabel a virtual camera

Reviewers should treat “name/identity-based virtual-camera detection is insufficient” as the finding. The construction of an evasive device is out of scope for this public artifact.
