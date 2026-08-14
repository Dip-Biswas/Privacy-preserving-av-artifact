# Vector 1 — Printed photograph

> [`NOTICE-EVALUATION.md`](../NOTICE-EVALUATION.md) · shared protocol: [`00-protocol.md`](00-protocol.md)

**Class:** trivial. **Property tested:** does liveness / presentation-attack detection reject a static print of an adult face?

## Stimulus

Three colour photographs of adult males, printed at A4, 300 dpi, on a laser printer. The print was held about 30–40 cm from the camera (phone path or laptop webcam, depending on the service).

No software toolchain. No second device except the camera that already belongs to the verification flow.

## Liveness handling

If the service asked for a head turn or similar directional pose, the operator **tilted or repositioned the print**. No other countermeasure (no blinking overlay, no cut-out eyes).

## Scoring

Follow [`00-protocol.md`](00-protocol.md): five trials, fresh session, success = adult/verified outcome.

## What this artifact does not include

Print files, face images, or a targeting list of services.
