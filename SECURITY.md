# Security policy

## Reporting a vulnerability

Do not post credentials, private text, or exploit details in a public issue. Email
maintainer Shah Bakhsh at shahbakhshtech@gmail.com with subject “BalNLP security”.
Include the affected commit, component, impact, and a minimal sanitized reproduction.
Use GitHub private vulnerability reporting if the repository offers that option;
its availability is not assumed. Coordinate disclosure after a fix or mitigation.
No response-time or long-term support guarantee is currently offered.

## Supported code

The development branch is the current maintenance target. Version 0.1.0 is package
metadata, not evidence of a published supported release. Older snapshots have no
separate security maintenance commitment. Review fixes before deploying them.

## Trust boundaries

- Official model revisions are pinned in `balnlp/config.py`. Overrides and local
  paths are operator-controlled trust decisions; review both provenance and license.
- Transformers loading disables remote Python. POS/NER require safetensors;
  morphology/parser use PyTorch `weights_only=True` and strict state loading.
  These controls reduce risk; they do not make untrusted artifacts harmless.
- `BALMORPH_ADAPTER` imports local Python by module/class name. Treat this setting
  as executable configuration; never accept it from an API client.
- Keep `HF_TOKEN` server-side with minimum necessary permissions. Never commit
  `.env`, model weights, credentials, private examples, or frontend secrets.
  Rotate an exposed token first; deleting a file does not revoke it or erase history.
- Audit dependencies and container bases before releases. Pins improve repeatability
  but do not establish that a dependency is free of vulnerabilities.

## API operations and privacy

The API has no authentication. CORS restricts browser origins, not non-browser access.
Place authentication and network controls at an operator-managed gateway if needed.
Defaults: 32,768-byte bodies, 2,000 characters, 256 words/tokens, 80 parser words per
sentence, 10 POSTs per minute per observed client, and one inference job per process.
Settings can change these values. Rate limiting is in-process, not distributed.
Configure trusted proxies deliberately; users behind a proxy may otherwise share a limit.

Request timeouts do not stop native inference threads. The job retains its slot;
a permanently blocked call may require process restart. Use one worker unless memory
and concurrency behavior have been measured. Health is not proof of inference readiness.

Application logs contain request identifiers, fixed endpoint names, durations, status,
and task failure codes, not submitted text. Rate limits hold transient client IPs and
timestamps. Hosting logs, crash dumps, browser extensions, and monitoring are outside
this policy's guarantees. See [privacy](docs/PRIVACY.md). Do not submit sensitive text
to an operator whose infrastructure policy you have not reviewed.
