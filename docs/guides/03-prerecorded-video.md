# Vector 3 — Pre-recorded video

> [`NOTICE-EVALUATION.md`](../NOTICE-EVALUATION.md) · shared protocol: [`00-protocol.md`](00-protocol.md)

**Class:** technical. **Property tested:** does the service distinguish a live camera from replay of an adult face (including clips that already contain liveness actions)?

## Stimulus

A replay of an adult male face, presented through the software-camera path (1920×1080 / 60 fps) where the service allowed it.

Clip set:

- Public footage of adults with sustained eye contact
- Researcher-recorded clips covering a fixed action list: forward gaze, left/right head turn, up/down gaze, mouth open/close

If a service used a **fixed** liveness script, we learned the script from one genuine attempt, then used a clip that already completed that script. That is a measurement of replay, not of guessing challenges in real time.

No device rooting.

## Liveness handling

Only actions present in the chosen clip. Unpredictable challenge/response that is not in the recording fails this vector (and is then in scope for live-face vectors 4–6).

## Scoring

Five trials, fresh session, success = adult/verified outcome.

## What this artifact does not include

Video files, capture-tool configuration, or how to wire a replay into a browser camera.
