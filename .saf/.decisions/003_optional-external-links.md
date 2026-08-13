# 003 · External links enter the scope, behind the --esterni option

- **Status:** accepted
- **Date:** 2026-08-09

The Senior disposes that external http and https links be verified, with a HEAD request and a timeout. Inclusion is optional: without --esterni the behavior stays as before, deterministic and network-free, so CI does not inherit the flakiness of the network. Verification uses urllib from the standard library: the decision on the absence of dependencies stays valid and shaped the how. This supersedes the decision that kept external links out of scope: the alternative that decision had deferred is now realized.

## Relations
- supersedes → [[decision:001]]
- delivered-by → [[iteration:002]]
