#!/usr/bin/env python3
"""Check a completion review's reply before it counts (review-todo-section, step 5a).

    python scripts/completion_check.py --head <tip sha> < review.md     PASS (exit 0) or FAIL <reason> (exit 1)
    python scripts/completion_check.py --self-test

The panel's rounds pass through `review_prompt.py check-panel`; the completion review has its own reply format
(`docs/completion-review-prompt.md`), and a reply that is truncated, malformed, or about another candidate must never
be recorded as `complete`. A reply passes only when:

- its first non-empty line is `CANDIDATE: <sha>`, a prefix of at least 7 characters of `--head` (the receipt that the
  reviewer read this candidate);
- every other line before the closing lines is a finding `N. in-scope ...` or `N. out-of-scope ...`, numbered from 1
  without gaps, or an indented continuation of one;
- it closes with `HIGHEST: P1|P2|P3|none` and then `OVERALL: complete|incomplete` as its last non-empty line;
- the verdict agrees with the findings: `complete` with no finding and `HIGHEST: none`, `incomplete` with at least one.

A FAIL is handled as a round that returned no review: retried under the outage rule, never counted as a pass.
Stdlib only.
"""
import argparse
import re
import sys

CANDIDATE = re.compile(r"^CANDIDATE:\s*([0-9a-f]{7,40})\s*$")
FINDING = re.compile(r"^(\d+)\.\s+(in-scope|out-of-scope)\s+\S")
CONTINUATION = re.compile(r"^\s+\S")
HIGHEST = re.compile(r"^HIGHEST:\s*(P1|P2|P3|none)\s*$")
OVERALL = re.compile(r"^OVERALL:\s*(complete|incomplete)\s*$")


def check(text, head):
    """Return (True, reason) when the reply passes, else (False, reason)."""
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").split("\n")]
    while lines and not lines[-1].strip():
        lines.pop()
    body = [line for line in lines]
    while body and not body[0].strip():
        body.pop(0)
    if not body:
        return False, "empty reply"
    receipt = CANDIDATE.match(body[0].strip())
    if not receipt:
        return False, "first line is not CANDIDATE: <sha>"
    if not head or not head.lower().startswith(receipt.group(1).lower()):
        return False, f"the receipt names {receipt.group(1)}, not this candidate"
    if len(body) < 3:
        return False, "missing HIGHEST or OVERALL"
    overall = OVERALL.match(body[-1].strip())
    if not overall:
        return False, "last line is not OVERALL: complete|incomplete"
    closing = [i for i, line in enumerate(body[1:-1], 1) if line.strip()]
    if not closing or not HIGHEST.match(body[closing[-1]].strip()):
        return False, "the line before OVERALL is not HIGHEST: P1|P2|P3|none"
    highest = HIGHEST.match(body[closing[-1]].strip()).group(1)
    findings = 0
    in_finding = False
    for line in body[1:closing[-1]]:
        if not line.strip():
            continue
        found = FINDING.match(line)
        if found:
            if int(found.group(1)) != findings + 1:
                return False, f"finding {found.group(1)} is out of sequence"
            findings += 1
            in_finding = True
        elif in_finding and CONTINUATION.match(line):
            continue
        else:
            return False, f"unexpected line: {line.strip()[:60]!r}"
    if overall.group(1) == "complete" and (findings or highest != "none"):
        return False, "OVERALL: complete with findings or a severity"
    if overall.group(1) == "incomplete" and not findings:
        return False, "OVERALL: incomplete with no finding"
    return True, f"{findings} gap(s), highest {highest}, overall {overall.group(1)}"


def self_test():
    head = "0123456789abcdef0123456789abcdef01234567"
    good_complete = f"CANDIDATE: {head[:12]}\n\nHIGHEST: none\nOVERALL: complete\n"
    good_gaps = (f"CANDIDATE: {head[:7]}\n1. in-scope File > Open has no shortcut\n   it should be Ctrl+O per the map\n"
                 "2. out-of-scope Recent files list owned by nobody\nHIGHEST: P1\nOVERALL: incomplete\n")
    cases = [
        ("a complete reply passes", good_complete, True),
        ("a reply with gaps passes", good_gaps, True),
        ("OVERALL alone fails", "OVERALL: complete\n", False),
        ("a missing HIGHEST fails", f"CANDIDATE: {head[:12]}\nOVERALL: complete\n", False),
        ("another candidate fails", "CANDIDATE: fedcba9\nHIGHEST: none\nOVERALL: complete\n", False),
        ("complete with a gap fails", f"CANDIDATE: {head[:12]}\n1. in-scope x\nHIGHEST: P2\nOVERALL: complete\n", False),
        ("incomplete with no gap fails", f"CANDIDATE: {head[:12]}\nHIGHEST: none\nOVERALL: incomplete\n", False),
        ("an untagged finding fails", f"CANDIDATE: {head[:12]}\n1. x is missing\nHIGHEST: P1\nOVERALL: incomplete\n", False),
        ("a gap in numbering fails", f"CANDIDATE: {head[:12]}\n2. in-scope x\nHIGHEST: P1\nOVERALL: incomplete\n", False),
        ("a truncated reply fails", f"CANDIDATE: {head[:12]}\n1. in-scope x\n", False),
    ]
    failed = 0
    for name, text, want in cases:
        got, reason = check(text, head)
        if got != want:
            failed += 1
            print(f"FAIL {name}: got {got} ({reason})")
    print(f"completion_check self-test: {len(cases)} cases, {failed} failed")
    return 1 if failed else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--head", help="The candidate's tip sha")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.head:
        parser.error("--head is required")
    ok, reason = check(sys.stdin.read(), args.head)
    print(("PASS " if ok else "FAIL ") + reason)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
