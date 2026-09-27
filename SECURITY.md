# Security Policy

## Supported versions

The Isotone Graphics Suite is in pre-alpha and has no published release yet. Once releases begin, security fixes go into the latest release of each app:

| App | Supported |
| --- | --------- |
| Stilus, latest `stilus-v*` release | Yes |
| Pinxit, latest `pinxit-v*` release | Yes |
| Albumen, latest `albumen-v*` release | Yes |
| Isotone suite installer, latest `isotone-v*` release | Yes |
| Older releases and unreleased builds from `main` | Best effort |

## Reporting a vulnerability

**Please do not report security vulnerabilities through public issues, discussions, or pull requests.**

Report them privately through GitHub's private vulnerability reporting:

1. Open the [Security tab](https://github.com/rizonesoft/Isotone/security) of this repository.
2. Choose **Report a vulnerability** ([direct link](https://github.com/rizonesoft/Isotone/security/advisories/new)).
3. Fill in the advisory form.

Helpful details to include:

- The affected app (Stilus, Pinxit, Albumen, or the installer) and its version or commit
- The type of issue, for example a crash or memory corruption when opening a crafted file, or an installer privilege problem
- Steps to reproduce, and a sample file if the issue is triggered by opening one
- The impact as you understand it

Crafted input files are the most likely attack surface for graphics software. If your report involves a malicious SVG, image, or RAW file, attach it to the private advisory, not to a public issue.

## What to expect

- We aim to acknowledge a report within **7 days**.
- We will keep you updated in the advisory as we investigate and fix the issue.
- Once a fix ships, we publish the advisory and credit you, unless you prefer to stay anonymous.

This is a small open source project, so timelines are goals rather than guarantees. We appreciate coordinated disclosure: please give us a reasonable chance to release a fix before discussing the issue publicly.

## Code signing

Release binaries are not code-signed yet. Official builds are published only on [rizonesoft.com](https://www.rizonesoft.com/?utm_source=github&utm_medium=security), served from `download.rizonesoft.com`; GitHub releases carry no installers. Check a download against the SHA-256 table in the matching [GitHub release](https://github.com/rizonesoft/Isotone/releases) (or the `SHA256SUMS` file beside it) before you run it, and treat an Isotone installer offered anywhere else as untrusted.
