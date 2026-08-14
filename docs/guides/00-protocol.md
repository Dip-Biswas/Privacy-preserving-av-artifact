# Shared experimental protocol

> [`NOTICE-EVALUATION.md`](../NOTICE-EVALUATION.md) — authorized review and defensive testing only.

This page is the common setup for all nine vectors. Per-vector stimulus details are in the numbered guides.

## Threat model (what we were measuring)

Primary adversary: someone who wants age-restricted content without legitimate face-based verification. Identity-document and credit-card flows were **out of scope**.

Adversaries are grouped by the **minimum capability** a vector requires:

| Class | Barrier we treated as the cutoff |
| --- | --- |
| Trivial | A single physical artifact; no software toolchain |
| Technical | Install and configure unmodified consumer or open-source desktop software; device trust boundary intact |
| Motivated | Subvert device trust (rooted phone / custom kernel camera device) **or** acquire a reusable credential that someone else can present |

The passkey vector is dual-class: **acquisition** is motivated; **reuse** after a shared credential is trivial for the recipient.

## Apparatus

| Item | What we used |
| --- | --- |
| Desktop | ThinkPad E14 Gen 7, Linux |
| Phone | Google Pixel 6, Android 13 |
| Lighting | Indoor, ~200 lux (smartphone light-meter app) |
| Browser sessions | Fresh profile per trial; cookies cleared |

We do not publish OS hardening, proxy, or intercept-tool configuration.

## Two input paths

Where a service accepted both, we tested two ways the stimulus reached the verifier. They are **not** the same artifact from a detector’s point of view:

1. **Phone recapture.** Stimulus on the laptop display; phone camera aimed at that screen from about 20–30 cm. Introduces recapture (moiré, refresh) artifacts.
2. **Software camera.** Stimulus composed on the desktop and offered to the verification browser as a camera device at 1920×1080 / 60 fps. Avoids recapture artifacts.

Results for the two paths were recorded separately.

We do not document how to install or name virtual-camera software.

## Trial protocol and scoring

- Each service × vector cell was attempted **five times** under the same lighting and apparatus.
- Success means the service returned an **adult / verified** outcome (or issued a reusable credential, for vector 9).
- We report **k/n**: `k` successful bypasses out of the attempts run, and `n` as the attempt index of first success when that is used to describe consistency.
- A new browser session was required because several services rate-limit retries inside one cookie jar.

A cell is a **failure of the service** (from our measurement) if any of the five trials succeeded. A cell is a **resistance** result only if all five failed under these conditions.

## Liveness: what each stimulus can answer

Operators responded to on-screen prompts with whatever the stimulus allowed. This table is a capability map, not instructions.

| Stimulus | Head turn | Blink | Mouth | Dynamic (live face) |
| --- | --- | --- | --- | --- |
| Printed photograph | pose by tilting the print | no | no | no |
| Screen display | swap among posed stills | no | no | no |
| Aging filter | yes (live face) | yes | yes | yes |
| 3D head model | yes (operator) | yes | yes | yes |
| Real-time deepfake | yes (live face) | yes | yes | yes |
| Pre-recorded video | yes if in the clip | yes if in the clip | yes if in the clip | no (replay) |
| Android camera substitute | same as the replay clip | same | same | no (replay) |

Vector 9 does not present a face after the credential exists.

## Targets (how services were reached)

We used:

- Vendor **public demos** and **free trials** when they existed
- Otherwise, **researcher-controlled accounts** on consumer platforms that embed a face-based check

We do not list vendor or platform names in this artifact. Several integrations of the same vendor were tested when configuration (liveness threshold, session handling) might differ.

## What counts as in-scope vs omitted

In-scope for reviewers: apparatus, lighting, paths, scoring, stimulus class, liveness map, disclosure.

Omitted on purpose: exploit code, vendor URLs, rooting/kernel procedures, camera-evasion pipelines, password-manager sharing steps.
