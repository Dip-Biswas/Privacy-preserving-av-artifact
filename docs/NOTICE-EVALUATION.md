# Notice: evaluation material

This repository’s evaluation documents (`docs/ATTACKS.md`, `docs/guides/`) describe **how the adversarial evaluation was designed and scored**, so reviewers can judge validity. They are **not** permission to bypass age gates.

## Who this is for

- Peer reviewers checking experimental protocol, apparatus, and success criteria
- Vendors assessing their own products on systems they operate or are authorized to test
- Researchers replicating the **measurement design** (trial counts, lighting, input paths, scoring)

## Who this is not for

Anyone seeking to access age-restricted services they are not allowed to use, including minors.

## What this repository includes

- Threat model and attacker-capability classes
- Apparatus, lighting, trial protocol, and scoring (`k/n`)
- Per-vector **method summaries**: what stimulus was presented, which liveness cues it can answer, how a trial was counted as a success or failure
- A privacy/network **checklist** (no live HAR dumps)

## What this repository does not include

- Exploit code, browser extensions, payloads, or token-forging scripts
- Vendor names, demo URLs, or consumer-platform integration lists
- Device-rooting, bootloader-unlock, or kernel-module install procedures
- Virtual-camera evasion pipelines (device naming, stream piping)
- Password-manager sharing or passkey-export playbooks
- Configuration guides for deepfake, 3D-model, or aging-filter software

Those omissions are intentional. Reviewers can still see **what was tested and under what conditions**. Reproduction of motivated toolchains is out of scope for a public artifact.

## Ethics and authorization

- Subjects were adult researchers. No minors took part.
- Trials used public demos, vendor free trials, or researcher-controlled accounts on consumer platforms.
- Identity-document and payment flows were out of scope.
- Findings were disclosed to the vendors that were tested.

## License vs. use restriction

Source code in this repository is MIT-licensed. That license does **not** authorize unlawful access to third-party services. Do not use these documents to circumvent age-assurance on production sites.
