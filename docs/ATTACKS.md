# Evaluation catalog

This page lists **nine evaluation vectors** used against commercial face-based age-verification services, grouped by the minimum capability required.

**Reviewers:** protocol (apparatus, scoring, per-vector method) is in [`docs/guides/`](guides/README.md). Read [`docs/NOTICE-EVALUATION.md`](NOTICE-EVALUATION.md) first.

This repository does not include exploit code, payloads, toolchain install procedures, or vendor names/URLs.

## Capability model

| Class | Barrier | Vectors |
| --- | --- | --- |
| **Trivial** | Single physical artifact; no software toolchain | Printed photograph; screen-displayed photograph |
| **Technical** | Install and configure unmodified consumer/open-source desktop software; no rooting | 3D head model; real-time deepfake; consumer aging filter; pre-recorded video |
| **Motivated** | Subvert device trust (root / custom kernel camera device) or acquire a reusable credential | Rooted Android virtual camera; custom V4L2 device; reusable passkey acquisition |

The reusable-credential vector is dual-class: **acquisition** is motivated; **reuse** after a shared passkey is trivial for the recipient.

## The nine vectors

| # | Vector | Class | What it tests | Guide |
| --- | --- | --- | --- | --- |
| 1 | Printed photograph | Trivial | Presentation-attack / liveness against a static print | [01](guides/01-printed-photograph.md) |
| 2 | Screen-displayed photograph | Trivial | Same, with a monitor as the presentation surface | [02](guides/02-screen-display.md) |
| 3 | Pre-recorded video | Technical | Replay of an adult face (including scripted liveness actions) | [03](guides/03-prerecorded-video.md) |
| 4 | Consumer aging filter | Technical | Live face with an age-morph lens still satisfying liveness | [04](guides/04-aging-filter.md) |
| 5 | 3D head model | Technical | Synthetic rigged head responding to prompts | [05](guides/05-3d-head-model.md) |
| 6 | Real-time deepfake | Technical | Live face-swap still passing liveness | [06](guides/06-realtime-deepfake.md) |
| 7 | Rooted Android virtual camera | Motivated | Camera-framework substitution below the app | [07](guides/07-rooted-android-camera.md) |
| 8 | Custom V4L2 virtual camera | Motivated | Virtual device that is not identifiable as a common streaming-app camera | [08](guides/08-custom-v4l2-camera.md) |
| 9 | Reusable passkey export and distribution | Motivated acquire / trivial reuse | Non-transferability of ecosystem passkeys via ordinary password-manager sharing — without breaking FIDO2 cryptography | [09](guides/09-reusable-passkey.md) |

Headline outcomes: five services fall to a **trivial** vector alone. Motivated camera substitution defeated 17/18 services in-browser. One service implemented virtual-camera detection and still failed vector 8.

## Not in this repository

- Vendor names, demo URLs, or integration lists
- Browser extensions or scripts that swap selfie bytes, forge success tokens, or skip liveness
- Rooting, kernel-module, or virtual-camera evasion pipelines
- Password-manager sharing playbooks
- Deepfake or 3D-model configuration files

## Using this catalog

If you maintain an age-verification service, treat the nine rows as a **defensive test-plan outline** on systems you are authorized to test: liveness that rejects prints, camera-source attestation, and non-exportable credentials.
