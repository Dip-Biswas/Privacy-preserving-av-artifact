# Vector 5 — 3D head model

> [`NOTICE-EVALUATION.md`](../NOTICE-EVALUATION.md) · shared protocol: [`00-protocol.md`](00-protocol.md)

**Class:** technical. **Property tested:** does the service accept a synthetic rigged head that an operator can pose in response to prompts?

## Stimulus

A rigged 3D adult male head, rendered on the desktop and presented through the software-camera path. The operator moved the model in real time (turn, nod, expression) when the service prompted.

The model had enough controls to answer blink and smile challenges as well as head pose. No rooted device.

## Liveness handling

Operator-driven: whatever the rig exposed. This is stronger than a still and weaker than a live human only insofar as the rig looks synthetic to a detector.

## Scoring

Five trials, fresh session, success = adult/verified outcome.

## What this artifact does not include

Model files, renderer HTML, animation-control modifications, or capture-tool configuration.
