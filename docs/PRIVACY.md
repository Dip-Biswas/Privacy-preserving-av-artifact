# Privacy / network measurement

Inspect network traffic of age-verification services: what leaves the device (image, video, location), whether uploads are authenticated, and whether undisclosed analytics or subprocessors appear.

This repository does **not** include HAR dumps, vendor names, or capture scripts from live sessions (those traces contain tokens and biometric payloads). Use this page as a **measurement checklist**, then store traces privately.

## What to look for

| Question | Why it matters |
| --- | --- |
| Does a face image or video leave the device? | Client-side estimation vs server-side upload |
| If uploaded, is the URL unauthenticated or only time-limited? | Access-control failures affect *complying* users |
| Is a subprocessor named in the UI / privacy policy? | Some services delegated biometrics to unnamed vendors |
| Device fingerprinting / analytics SDKs | Common in inspected traffic |
| Location or other extra fields | Scope creep beyond a binary age check |

Attackers who never present a real face do not pay this cost; honest users do.

## How to capture (defensive / your own test account)

1. Use a demo or site **you are authorized to test**, or a site you operate.
2. Chrome DevTools → Network → preserve log → export HAR. For WebSockets, export frames separately.
3. Redact cookies, tokens, and image bytes before sharing.
4. Classify endpoints: first-party host vs CDN vs analytics vs unnamed biometric API.

Do not replay captured success tokens against production sites; that is out of scope for this artifact.

## Reading a HAR without extra tools

A HAR is JSON. After redaction you can list hostnames:

```bash
python -c "import json,sys; h=json.load(open(sys.argv[1]));
print(sorted({e['request']['url'].split('/')[2] for e in h['log']['entries']}))" capture.har
```

Ask: which hosts receive `multipart` image/video bodies, whether those URLs later fetch without `Authorization`, and whether analytics hosts appear that the UI never mentioned.
