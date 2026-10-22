## Round 1: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-22T21:06:38Z
- Effort: xhigh
- Lines: 26
- Digest: 170c18e7a418171b

## adversarial: needs-attention

1. P1 `docs/specs/2026-10-22-native-stack-design.md:86`: The save sequence is not atomic across its two renames. Kill the process after moving the original to the backup but before installing the temporary file: the saved pathname is absent, contradicting line 90’s old-or-new-file proof. Startup recovery only specifies scanning the app’s recovery folder, without a durable transaction record locating interrupted saves in arbitrary target folders.

2. P1 `docs/specs/2026-10-22-native-stack-design.md:88`: Retirement has no saved-revision cutoff. Start saving revision N, edit to N+1 and complete its checkpoint, then finish saving N. The retirement rule permits retiring the newer checkpoint, and recovery excludes retired checkpoints, losing work already protected by a completed checkpoint. Require retirement to identify the session and covered edit counters, and test this interleaving.

## consistency: needs-attention

3. P2 `docs/specs/2026-10-22-native-stack-design.md:72`: Requiring printing through `ID2D1PrintControl` conflicts with preserving the existing prepress scope. `todo/02-stilus/TODO-13-stilus-parity-print.md:391` requires printing the app’s own PostScript to a RIP, including in-RIP separations and trapping. Direct2D print control consumes drawing command lists, not the app’s PostScript stream. Specify a separate delivery path for those jobs; converting them through Direct2D cannot preserve that contract. See Microsoft’s [Printing and command lists](https://learn.microsoft.com/en-us/windows/win32/direct2d/printing-and-command-lists).

## integration: needs-attention

4. P2 `docs/specs/2026-10-22-native-stack-design.md:78`: Bounding individual dispatches does not bound GPU work already queued ahead of input. A filter can enqueue many sub-2-ms dispatches before the next pointer update, leaving its frame behind their accumulated execution time. Swap-chain frame latency limits queued frames, not arbitrary compute dispatches. Require a bound on outstanding engine work with completion tracking, and test that backlog case. Microsoft documents [asynchronous command submission](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11devicecontext-flush) and the narrower [frame-latency limit](https://learn.microsoft.com/en-us/windows/win32/api/dxgi1_3/nf-dxgi1_3-idxgiswapchain2-setmaximumframelatency).

## source-defect: needs-attention

5. P1 `docs/specs/2026-10-22-native-stack-design.md:86`: The replacement protocol omits preservation of file security and encryption. Save a file with a restrictive explicit DACL inside a directory whose inherited permissions allow broader reading: an ordinarily created temporary file inherits the directory’s permissions and retains them when renamed onto the target. Individually encrypted files can likewise become plaintext. Preserve protections before writing document data into temporary files. This follows Microsoft’s [file security rules](https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights); [ReplaceFileW](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-replacefilew) explicitly preserves protections that this replacement sequence omits.

6. P2 `docs/specs/2026-10-22-native-stack-design.md:65`: The reference-white policy incorrectly applies HDR luminance semantics to Advanced Color SDR. Microsoft states that reference-white adjustment applies only to HDR; on Advanced Color SDR, scRGB `(1,1,1)` already represents the display’s maximum white. Applying the prescribed HDR white scaling there can brighten and clip SDR content. Separate the two modes and test an ACM-enabled SDR display. See [Advanced Color luminance behavior and reference white](https://learn.microsoft.com/en-us/windows/win32/direct3darticles/high-dynamic-range#match-your-apps-reference-white-to-the-os-sdr-reference-white-level).

7. P2 `docs/specs/2026-10-22-native-stack-design.md:94`: The watcher cannot obtain the promised crash dump by waiting for unexpected exit: termination frees the process’s memory before its process object signals. A fail-fast crash also bypasses the exception handlers that could send the cooperative crash signal, while this design excludes WER. Require capture before termination and test fail-fast separately. Microsoft documents both [process termination](https://learn.microsoft.com/en-us/windows/win32/procthread/terminating-a-process) and [RaiseFailFastException](https://learn.microsoft.com/en-us/windows/win32/api/errhandlingapi/nf-errhandlingapi-raisefailfastexception).

## record: approve

HIGHEST: P1
OVERALL: needs-attention

## Response to round 1

This record's round 1 is the spec's third review round; rounds 1 and 2 ran before this record existed, and their findings and answers are in the commit messages of `8a04c8a` and `9832b83`. Every finding was verified and is real; each is answered in the spec at the commit that follows this record.

1. P1, saves not atomic across two renames: verified. The backup is now a hard link to the previous file (a flushed copy where the volume has no hard links) and the temporary file replaces the target in one `MoveFileExW` rename with `MOVEFILE_REPLACE_EXISTING` and `MOVEFILE_WRITE_THROUGH`, so the target's name always holds a complete file; a save journal record in the recovery folder names the target, temporary file, and backup, and recovery settles leftover records before scanning checkpoints. Proof added: a kill at each step of the save protocol.
2. P1, retirement with no saved-revision cutoff: verified. Retirement records name the document, the session, and the edit counter covered; a completed save retires only checkpoints at or below the counter it wrote. Proof added: save of N completing after N+1 was checkpointed, then a kill, recovering N+1.
3. P2, PostScript to a RIP cannot go through Direct2D print control: verified against `todo/02-stilus/TODO-13-stilus-parity-print.md` (`D02 T13 §10`). Printing now has a second path: app-written PostScript or PDF sent unchanged as a `RAW` spooler job to a queue whose driver or PPD accepts it.
4. P2, bounded dispatches do not bound queued work: verified. The render thread keeps at most a fixed number of engine dispatches unfinished on the GPU (default one), tracked with `D3D11_QUERY_EVENT`; a backlog test measures pen latency and cadence under a filter that would enqueue hundreds of dispatches.
5. P1, protections lost on save: verified. The temporary file is created with the target's security descriptor, attributes, EFS encryption, and compression before any document data is written, and the save fails if they cannot be applied; named streams such as the Mark of the Web are copied; read-only targets are refused. Proofs added for each.
6. P2, reference white applied to Advanced Color SDR: verified against Microsoft's Advanced Color guidance ("Reference white applies only to HDR displays"). The policy is now per mode: reference white scaling in HDR only, scRGB 1.0 as the display's white in Advanced Color SDR. Proof added on an Advanced Color SDR display.
7. P2, the watcher cannot dump after exit and misses fail-fast: verified against Microsoft's `__fastfail` and `RaiseFailFastException` documentation (no handlers run; an attached debugger is given the state). The watcher now attaches as the app's debugger with kill-on-exit off and dumps on last-chance and fail-fast exceptions while the app is suspended. Proofs added: access violation, `__fastfail`, `/GS` overrun, and stack overflow, plus a killed watcher leaving the app running.

## Round 2: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-22T21:17:07Z
- Effort: xhigh
- Lines: 22
- Digest: 91070c34d3588a86

## adversarial: needs-attention

1. P1 `docs/specs/2026-10-22-native-stack-design.md:86`: Save commits have no serialization or revision-order rule. Start saving N, edit and checkpoint N+1, then start saving N+1. Let N+1 finish and retire its checkpoints, then let N replace the target. A crash now leaves N on disk with N+1 excluded from recovery. The revised retirement cutoff does not prevent this interleaving. Require ordered commits per target and test reversed save completion.

2. P2 `docs/specs/2026-10-22-native-stack-design.md:86`: The failure guarantee contradicts the operation order. After the replacing rename succeeds, deleting the backup or retiring the journal can fail, but the previous file is already replaced. Inject either cleanup failure after the rename to disprove “if any step fails ... the previous file is untouched.” Define the commit point, distinguish committed saves from cleanup failures, and retain retryable cleanup records.

## consistency: approve

## integration: needs-attention

3. P1 `docs/specs/2026-10-22-native-stack-design.md:87`: Protected documents can leak through recovery files. Open an EFS-encrypted document while the recovery directory is unencrypted, edit it, and allow its first checkpoint. The “same write protocol” copies protections from the checkpoint target, which does not yet exist, rather than from the source document. Nothing requires encrypting that checkpoint; line 94 similarly permits plaintext dumps containing document data. Define and test protection before writing these secondary copies. EFS encryption is specific to files and their destination directory’s defaults. [Microsoft: Handling Encrypted Files and Directories](https://learn.microsoft.com/en-us/windows/win32/fileio/handling-encrypted-files-and-directories).

## source-defect: needs-attention

4. P1 `docs/specs/2026-10-22-native-stack-design.md:86`: Copying owner and DACL does not preserve mandatory integrity protection. Integrity labels and their policies reside in the SACL. Demonstrate with a file carrying an explicit medium-integrity `SYSTEM_MANDATORY_LABEL_NO_READ_UP` policy: the specified replacement omits that policy, allowing a low-integrity process with sufficient DACL access to read the saved contents. Preserve the label and policy before writing data, or refuse the save. [Microsoft: Mandatory Integrity Control](https://learn.microsoft.com/en-us/windows/win32/secauthz/mandatory-integrity-control).

5. P2 `docs/specs/2026-10-22-native-stack-design.md:86`: Preserving `FILE_ATTRIBUTE_ENCRYPTED` does not preserve the original EFS users’ keys. Give users A and B decrypting access to a file, then save it as A using the specified newly encrypted replacement. The protocol never transfers B’s encryption certificate, so B can lose access despite an unchanged DACL and a successful encryption-attribute check. Require preservation and verification of authorized decryptors, with a two-user regression test. Microsoft exposes separate APIs for querying and adding these keys. [Microsoft: Encrypted Files and User Keys](https://learn.microsoft.com/en-us/windows/win32/fileio/encrypted-files-and-user-keys).

## record: approve

HIGHEST: P1
OVERALL: needs-attention

## Response to round 2

This record's round 2 is the spec's fourth review round. Every finding was verified and is real. All five sit in the save protocol, the third round running to patch that unit, so under the loop's rule it was re-thought as a whole rather than patched again: saving now has one stated commit point and serialized commits; what a save preserves is one named list, the file identity contract, each item applied before data is written, read back before the commit, and the save refused when any item cannot be reproduced, with what lies outside the contract named; and every secondary copy of document data is encrypted at rest whatever the source's protection.

1. P1, reversed save completion: verified. Saves of one target are serialized and only the newest waiting request runs, so commits follow edit order. Proof added: a slow save of N with N+1 queued, killed at each point.
2. P2, failure guarantee contradicts the operation order: verified. The replacing rename is the commit point; failures before it fail the save with the previous file untouched, cleanup failures after it are not save failures and are finished from the journal at the next save or start. Proof added: an injected cleanup failure.
3. P1, protected documents leak through recovery files and dumps: verified. A Secondary copies rule: recovery and dump folders granted to the user and SYSTEM only, every checkpoint and dump encrypted at rest under a DPAPI-wrapped key, dumps encrypted through `MiniDumpWriteDump`'s I/O callbacks. Proof added: no plaintext of an EFS document in its checkpoint or dump.
4. P1, integrity label not preserved: verified against Microsoft's Mandatory Integrity Control documentation (labels live in the SACL). The label and its policy are in the contract, through `LABEL_SECURITY_INFORMATION`. Proof added.
5. P2, EFS key holders not preserved: verified. The contract carries every user able to decrypt the target (`QueryUsersOnEncryptedFile`, `AddUsersToEncryptedFile`) and refuses the save when a certificate is unavailable. Proofs added: a two-user file, and the refusal.

Also in this revision, outside the review: the language standard moved from C++20 to C++23 (`docs/dev/decisions.md`, 2026-10-22: The C++ language standard).
