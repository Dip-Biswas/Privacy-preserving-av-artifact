# Vector 9 — Reusable passkey distribution

> [`NOTICE-EVALUATION.md`](../NOTICE-EVALUATION.md) · shared protocol: [`00-protocol.md`](00-protocol.md)

**Class:** motivated to **acquire**; trivial to **reuse**. **Property tested:** are ecosystem age passkeys non-transferable in practice, or can a consumer password manager share them without breaking FIDO2 cryptography?

## What we measured (not how to share credentials)

1. **Acquisition.** A passkey-backed age credential is created after a successful face-based flow (or an upstream flow that issues the same credential type). Acquisition may use another vector, or a legitimate adult verification. We classify that step as motivated.
2. **Storage.** The browser offered to save the credential as a platform passkey. With a consumer password manager set as the passkey provider, the item landed in that vault rather than only in the platform authenticator.
3. **Distribution.** Vault-sharing features (shared collection / shared vault), including a self-hosted password-manager deployment used only to test member-count limits, were used to give a **second account** read access. No raw key-material export and no FIDO2 protocol break.
4. **Reuse.** The second account, which never completed verification, presented the shared credential on accepting sites.

We also issued more than ten credentials in succession from one account and device to see whether **rate limits or cooldowns** existed.

## Scoring

Success for reuse: the receiving account satisfies the age gate **without** performing face verification. Success for the rate-limit check: additional credentials continue to issue.

## Dual-class note

One capable actor pays the acquisition cost once. Every downstream recipient only accepts a share and clicks through — trivial effort. That composition is the measurement, not a tutorial.

## What this artifact does not include

- Password-manager product steps, org/collection UI, or export playbooks
- Vendor or platform names that accept the credential
- Scripts that mint, clone, or replay credentials
