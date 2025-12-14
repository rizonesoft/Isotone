# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of Imago seriously. If you believe you have found a
security vulnerability, please report it to us as described below.

### How to Report

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please send an email to security@rizonesoft.com with:

- Type of issue (e.g., buffer overflow, privilege escalation, etc.)
- Full paths of source file(s) related to the issue
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Resolution Target**: Within 90 days (depending on complexity)

### Disclosure Policy

- We will confirm receipt of your report within 48 hours
- We will provide a more detailed response within 7 days
- We will work with you to understand and resolve the issue
- We will keep you informed of our progress
- We will credit you in the security advisory (unless you prefer anonymity)

## Security Best Practices

When contributing to Imago:

- Never commit secrets, API keys, or credentials
- Use parameterized queries to prevent injection attacks
- Validate all user input
- Follow the principle of least privilege
- Keep dependencies up to date

Thank you for helping keep Imago and our users safe!
