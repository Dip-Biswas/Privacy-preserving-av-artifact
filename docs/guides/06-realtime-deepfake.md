# Vector 6 — Real-time deepfake

> [`NOTICE-EVALUATION.md`](../NOTICE-EVALUATION.md) · shared protocol: [`00-protocol.md`](00-protocol.md)

**Class:** technical. **Property tested:** does liveness still pass when a live face is swapped in real time?

## Stimulus

An unmodified consumer/open-source **live face-swap** stack, default settings, one available swap model. Output was presented through the software-camera path.

Because the swap is applied to a live performer, blinks and head motion remain available to answer prompts (same liveness class as vector 4).

No device rooting. No custom model training is required for this vector as we ran it.

## Scoring

Five trials, fresh session, success = adult/verified outcome.

## What this artifact does not include

Software names as a cookbook, model files, stream URLs, or capture-tool configuration.
