# Vector 4 — Consumer aging filter

> [`NOTICE-EVALUATION.md`](../NOTICE-EVALUATION.md) · shared protocol: [`00-protocol.md`](00-protocol.md)

**Class:** technical. **Property tested:** does liveness still pass when a live face is age-morphed by an unmodified consumer app?

## Stimulus

A live adult face, with a widely available **old-age / age-morph** lens applied on a stock phone. The filtered selfie view was the verification input, via either:

- phone recapture (filtered preview on a display, second phone as camera), or
- software-camera capture of that preview on the desktop

The point of the vector is **live motion under a consumer age lens**, not a particular brand. Any app that applies a real-time age morph on a live camera is the same class.

## Liveness handling

Because the filter rides on a live face, blinks, head turns, and mouth motion are preserved and can answer dynamic prompts.

## Scoring

Five trials, fresh session, success = adult/verified outcome.

## What this artifact does not include

App names as a targeting list, mirror/crop settings, or capture-tool configuration.
