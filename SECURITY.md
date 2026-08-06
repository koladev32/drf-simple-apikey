# Security Policy

For a detailed explanation of what this package protects against, what a leaked `FERNET_SECRET` exposes, and how to respond to a compromise, see the [Threat Model](https://drf-api-key.koladev.xyz/docs/threat-model) documentation.

## Supported Versions

Security fixes are released against the latest `2.x` minor version line only. If you're on an older minor version, upgrade to the latest `2.x` release before reporting an issue, to confirm it still reproduces.

| Version | Supported          |
| ------- | ------------------ |
| 2.4.x   | :white_check_mark: |
| 2.3.x   | :x:                |
| 2.2.x   | :x:                |
| < 2.2   | :x:                |
| 1.x     | :x:                |
| 0.x     | :x:                |

## Reporting a Vulnerability

If you believe you've found a security vulnerability in this project, please report it privately so it can be fixed before the details are public.

**Do not** open a public GitHub issue for a suspected vulnerability, as this can expose it to others before a fix is available.

### How to report

Email [koladev32@gmail.com](mailto:koladev32@gmail.com) with:

- A description of the vulnerability and its potential impact.
- Steps to reproduce it, including the package version and relevant configuration (`DRF_API_KEY` settings) — **never include real `FERNET_SECRET` values, API keys, or other live credentials in your report.**
- Any suggested fix or mitigation, if you have one.

### What to expect

We aim to acknowledge reports within 48 hours. Once confirmed, we'll work on a fix and coordinate a disclosure timeline with you, and credit you in the release notes unless you'd prefer otherwise.

Thank you for helping keep this project and its users secure.
