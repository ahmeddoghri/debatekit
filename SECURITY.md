# Security Policy

## Supported versions

This project is pre-1.0. Security fixes land on `main`; track the latest commit.

## Reporting a vulnerability

Please do not open a public issue for security problems. Use GitHub's
[private vulnerability reporting](https://github.com/ahmeddoghri/debatekit/security/advisories/new)
or email the maintainer. Include a description of the issue and its impact,
steps to reproduce (a minimal proof-of-concept helps), and any suggested fix.

You can expect an acknowledgement within a few days. Once a fix is out you will
be credited unless you would rather stay anonymous.

## Scope notes

debatekit is a pure-stdlib library with no runtime dependencies and makes no
network calls. It does not call any model; `Agent` is a simulated noisy
classifier for the benchmark. If you wire this pattern up to real models for
production debate, keep in mind that running N agents for R rounds costs
roughly N times R model calls per question, which is the real-world tradeoff
against the accuracy gain shown in the benchmark. Budget accordingly, and
consider pairing this with agentbudget to cap the cost of a debate that runs
long.
