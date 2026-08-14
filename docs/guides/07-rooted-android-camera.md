# Vector 7 — Rooted Android virtual camera

> [`NOTICE-EVALUATION.md`](../NOTICE-EVALUATION.md) · shared protocol: [`00-protocol.md`](00-protocol.md)

**Class:** motivated. **Property tested:** if the camera byte stream is substituted **below the application**, does in-app liveness still see a live camera?

## What we measured (not how to build it)

On a researcher-owned Pixel 6, the camera framework was hooked so a chosen app received a **replay clip** (same clip family as vector 3) instead of the physical sensor. Verification ran in a mobile browser on that device.

This is the device-integrity boundary: the app’s own camera API is no longer a faithful sensor.

## Scoring

Five trials, fresh session, success = adult/verified outcome. Headline measurement: this class of substitution defeated 17/18 in-browser services we tested.

## What this artifact does not include

- Bootloader unlock, rooting, or Magisk/Zygisk/Xposed procedures
- Module names, package-targeting steps, or replay-injection code
- Device images or patched browsers

Reviewers should treat “rooted camera-framework substitution + replay clip” as the independent variable. Reproduction of that toolchain is out of scope for this public artifact.
