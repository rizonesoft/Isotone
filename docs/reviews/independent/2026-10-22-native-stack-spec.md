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

## Round 3: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-22T21:27:57Z
- Effort: xhigh
- Lines: 19
- Digest: f305f7b0613a7dc8

## adversarial: needs-attention

1. P1 `docs/specs/2026-10-22-native-stack-design.md:86`: New-file saves can overwrite an unconfirmed competing file without a backup. Demonstrate by starting a save to an absent pathname, pausing before the rename, creating a different file at that pathname from another process, then resuming. The specified `MOVEFILE_REPLACE_EXISTING` destroys that file, while the new-file branch takes no backup or protection snapshot. New-file commits must refuse an occupied destination atomically. Microsoft documents this replacement behavior in [MoveFileExW](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw).
2. P1 `docs/specs/2026-10-22-native-stack-design.md:90`: “Handling a recovered document” retires all its checkpoints without requiring a durable replacement. Accept recovery of an untitled document, retire its previous session’s checkpoints, then kill the app before its first new checkpoint completes. The next launch excludes the only durable copy. Accepting recovery must retain the original checkpoints until a replacement save or checkpoint completes, or the user explicitly discards the recovered work.

## consistency: approve

## integration: needs-attention

3. P1 `docs/specs/2026-10-22-native-stack-design.md:102`: The secondary-copy protection protocol covers checkpoints and dumps at line 88 but leaves the carried-over scratch-backed tile store unspecified. `todo/03-gesso/TODO-02-gesso-rendering.md:68` requires spilling document pixels into an app-data scratch file without an encryption contract. Open an EFS-protected raster document, force eviction with the planned 64 MB cache cap, then inspect the scratch data after terminating the process. Encrypting its checkpoint and dump does not protect this separate copy. Extend the protection protocol and its proofs to scratch and persisted undo data before their first write. Microsoft’s [EFS documentation](https://learn.microsoft.com/en-us/windows/win32/fileio/handling-encrypted-files-and-directories) describes encryption as belonging to the particular file or destination directory.

## source-defect: needs-attention

4. P2 `docs/specs/2026-10-22-native-stack-design.md:96`: Passing every first-chance exception back unhandled also passes through the breakpoint generated by debugger attachment. Attach the proposed watcher to an otherwise healthy app with no breakpoint handler: that initial breakpoint reaches last chance and is treated as a crash. Microsoft documents the attachment breakpoint in [DebugActiveProcess](https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-debugactiveprocess) and the unhandled-exception consequences in [ContinueDebugEvent](https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-continuedebugevent). Require handling the debugger’s attachment breakpoint separately, and add a healthy-start attachment proof.

## record: approve

HIGHEST: P1
OVERALL: needs-attention

## Response to round 3

This record's round 3 is the spec's fifth review round. Every finding was verified and is real.

1. P1, a new-file save can overwrite a competing file: verified against `MoveFileExW`'s documented replace behavior. A save to a name that did not exist commits without `MOVEFILE_REPLACE_EXISTING`, so an occupied destination fails the commit atomically and the user is asked; a save over an existing file also checks the target's file ID and last-write time just before the commit and asks when another program changed it. Proofs added for both.
2. P1, recovery retirement before a durable replacement: verified. A recovered document's earlier checkpoints are retired only after a save or a new-session checkpoint of it completes, or the user discards it. Proof added: recovery, a kill before the first new checkpoint, and recovery again.
3. P1, the tile store's scratch is an unprotected copy: verified against `todo/03-gesso/TODO-02-gesso-rendering.md:68`. Secondary copies now names every kind of document-content file an app writes (checkpoints, dumps, tile scratch, persisted undo, preview and thumbnail caches, and any later kind), all in user-only folders and encrypted before the first byte; process-only copies use a key held only in memory. Proofs added for each kind.
4. P2, the attach breakpoint read as a crash: verified against `DebugActiveProcess`. The attach breakpoint is continued as handled and every other first-chance exception passed back unhandled. Proof added: a healthy session with the watcher attached writes no dump.

## Round 4: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-22T21:35:27Z
- Effort: xhigh
- Lines: 18
- Digest: 0c9f61e827e22ed8

## adversarial: needs-attention

1. P1 `docs/specs/2026-10-22-native-stack-design.md:91`: Recovery can overwrite a file created after the interrupted save. Demonstrate by killing the app after its backup exists, replacing the target with unrelated content that fails its format check, then restarting. The specified recovery restores the old backup over that new file without checking its identity or preserving it. A failed format check does not establish ownership of the current target. Require conflict detection and preservation before restoration.

## consistency: approve

## integration: needs-attention

2. P2 `docs/specs/2026-10-22-native-stack-design.md:96`: Portable-mode dump storage cannot satisfy line 88’s mandatory user-only DACL on FAT32 or exFAT. Run the portable ZIP from an exFAT USB drive and trigger a crash: the required folder protection cannot be enforced, so the implementation must either violate the protection contract or fail the promised dump proof. Define a supported fallback or an explicit volume restriction. Microsoft’s [File System Functionality Comparison](https://learn.microsoft.com/en-us/windows/win32/fileio/filesystem-functionality-comparison) documents that these filesystems lack ACL support.

## source-defect: needs-attention

3. P1 `docs/specs/2026-10-22-native-stack-design.md:86`: The new identity check does not make existing-file replacement conditional. Pause immediately after the final `GetFileInformationByHandleEx` check, let another process replace the target with B, then resume. `MoveFileExW(MOVEFILE_REPLACE_EXISTING)` replaces B, while the backup contains A. B is destroyed without confirmation. Microsoft documents [pathname-based replacement](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw), with no expected-destination identity parameter. Separately, ID plus last-write time cannot establish unchanged contents: Microsoft’s [File Times](https://learn.microsoft.com/en-us/windows/win32/sysinfo/file-times) documentation says write timestamps need not be fully updated until writing handles close. Require a protocol that protects the checked revision through commit or preserves the actual displaced revision, with tests for both interleavings.

## record: approve

HIGHEST: P1
OVERALL: needs-attention

## Response to round 4

This record's round 4 is the spec's sixth review round. Every finding was verified and is real. Findings 1 and 3 share a cause: Windows has no rename that replaces a name only if it still holds an expected file (`MoveFileExW` replaces by pathname), so any check-then-replace leaves a race. Saving's ownership was re-thought from checking to holding.

1. P1, recovery can overwrite a file created after an interrupted save: verified. Recovery now decides by the file IDs the journal records, never by a format check, and never overwrites a file the record does not name: it restores the original only into a free name, and otherwise keeps both and tells the user. Proof added.
2. P2, portable-mode folders on FAT or exFAT cannot carry a DACL: verified against Microsoft's File System Functionality Comparison. Encryption at rest is the protection that always holds; the DACL is a second layer that such volumes cannot carry, which the log records; checkpoints from another machine or account are reported unreadable rather than offered.
3. P1, the identity check does not make the replacement conditional, and last-write time does not prove unchanged contents: verified against `MoveFileExW` and File Times. An open document's file is now held with read-only sharing for the whole session (as Microsoft Office does), so it cannot change under the app; the commit renames the original to the backup name through that held handle and installs the new file without replacing, so no step can destroy a file the app does not hold. Proofs added: refused foreign writes, a file created between the two renames, and a document opened read-only when another program holds it for writing.

## Round 5: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-22T21:42:33Z
- Effort: xhigh
- Lines: 22
- Digest: 45449dec9298470b

## adversarial: needs-attention

1. P1 `docs/specs/2026-10-22-native-stack-design.md:86`: Ownership is lost during installation of the new file. Pause after `MoveFileExW` returns but before the prescribed reopen; replace the target with unrelated file B, then resume and save again. No identity check is required when reacquiring the lock, so the app can adopt B and subsequently delete it as its backup without confirmation. Protecting the original does not protect this handoff. Microsoft describes [MoveFileEx’s separate open, rename, and close operations](https://devblogs.microsoft.com/oldnewthing/20211022-00/?p=105822/).

## consistency: needs-attention

2. P2 `docs/specs/2026-10-22-native-stack-design.md:86`: The journal must contain the temporary file’s ID before the next specified step creates that file with `CREATE_NEW`. That ID does not exist yet. Following the stated order cannot produce the required journal; creating the temporary file first introduces an unrecorded crash state. Specify an executable creation and journaling order, including recovery from interruption between them.

## integration: needs-attention

3. P2 `docs/specs/2026-10-22-native-stack-design.md:86`: The unconditional session-long write lock prevents Albumen’s planned external-editor workflow. Open an image in Albumen Viewer, launch its configured external editor with the current path, and save there: Albumen’s handle denies the write or replacement. `todo/04-albumen/TODO-04-albumen-viewer.md:316` requires that handoff. The spec needs a viewing and handoff ownership contract that preserves this commitment.

## source-defect: needs-attention

4. P2 `docs/specs/2026-10-22-native-stack-design.md:86`: The held handle cannot generally provide the promised interoperability with readers. Renaming through it requires `DELETE` access, so another reader opened with `GENERIC_READ` and `FILE_SHARE_READ` fails with `ERROR_SHARING_VIOLATION`; that reader must also share delete access. An existing such reader likewise prevents acquiring the required handle, although it holds no writing access. This follows Microsoft’s [rename access requirements](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntifs/ns-ntifs-_file_rename_information) and [bidirectional sharing checks](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew).

5. P2 `docs/specs/2026-10-22-native-stack-design.md:91`: Identity-based recovery assumes IDs survive the prescribed renames on FAT, where line 86 still requires the same protocol. Microsoft documents that [renaming a FAT file to a longer name can change its ID](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/ns-fileapi-by_handle_file_information). Record an original’s ID, rename it to a sufficiently longer backup name, kill the app, and compare during recovery: the recorded identity no longer identifies that backup. Logging a weaker guarantee supplies no recovery rule for this supported case.

## record: approve

HIGHEST: P1
OVERALL: needs-attention

## Response to round 5

This record's round 5 is the spec's seventh review round. Every finding was verified and is real (finding 3 against `todo/04-albumen/TODO-04-albumen-viewer.md:316`, finding 4 against `CreateFileW`'s sharing rules, finding 5 against `BY_HANDLE_FILE_INFORMATION`'s FAT note). Saving has now drawn findings in five rounds, each one a level deeper into a prescribed Win32 call sequence, so the unit was re-thought at its altitude: the spec now owns five invariants and the proofs, and the document safety foundation section owns the exact sequence, with a reference sequence as its default.

1. P1, ownership lost while re-acquiring the lock: verified. No lock is held any more, so there is no handoff; a displaced file is moved aside by a rename that never replaces, and deleted only when its content hash proves it is the app's own last version.
2. P2, the journal cannot hold the temporary file's ID before it exists: verified. The journal holds a fresh random temporary name created with `CREATE_NEW`, and identity is by content hash, not file ID.
3. P2, the session lock breaks Albumen's external-editor handoff: verified. No lock is held; the app watches the folder and offers to reload; a proof covers the external editor saving over an image Albumen shows.
4. P2, the held handle blocks ordinary readers: verified. Resolved by holding no handle.
5. P2, file IDs change on FAT renames: verified. Invariant 3 forbids deciding by file IDs, times, or timing; a FAT proof with long names is added.

## Round 6: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-22T21:50:00Z
- Effort: xhigh
- Lines: 22
- Digest: 872fdb088864e4e1

## adversarial: needs-attention

1. P1 `docs/specs/2026-10-22-native-stack-design.md:92`: Recovery deletes the temporary pathname without checking its content, violating invariant 3. Reproduce by killing the app after journaling, placing unrelated content at the recorded temporary name, then restarting. Recovery deletes that foreign file because its only stated condition is that the temporary file is not the target. Random names and `CREATE_NEW` do not establish ownership after a crash.

## consistency: needs-attention

2. P2 `docs/specs/2026-10-22-native-stack-design.md:86`: Invariants 1 and 5 conflict with invariant 3 and the reference sequence’s conflict handling. Move original A to the backup, let another program create B at the target, then fail the installation rename. Preserving B prevents leaving A at the target as invariant 5 requires; after a crash, preserving B also prevents satisfying invariant 1’s old-or-new requirement. Define an explicit conflict outcome and corresponding exceptions to those invariants and proofs.

## integration: needs-attention

3. P1 `docs/specs/2026-10-22-native-stack-design.md:88`: The protection comparison is no longer bound to the file actually displaced. Pause after the final comparison, tighten the target’s DACL from another process, then resume the two renames. The replacement retains the temporary file’s earlier, broader DACL, weakening protection despite a successful comparison. The reference sequence needs a protection contract tied to the displaced version and a regression scenario for concurrent security changes. Microsoft’s [File Security and Access Rights](https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights) documents that renaming does not assign a new security descriptor.

## source-defect: needs-attention

4. P2 `docs/specs/2026-10-22-native-stack-design.md:89`: User-scoped `CryptProtectData` does not guarantee that checkpoints are readable only on the originating machine. Microsoft explicitly permits decryption on another computer with a roaming profile. Reproduce with the same roaming user on two machines and transfer the checkpoint and wrapped key. Either specify additional machine binding or correct the restriction and recovery behavior. See [CryptProtectData, Remarks](https://learn.microsoft.com/en-us/windows/win32/api/dpapi/nf-dpapi-cryptprotectdata#remarks).

## record: needs-attention

5. P3 `docs/specs/2026-10-22-native-stack-design.md:3`: The status says “six independent review rounds” but enumerates seven. Commit `c8b327f` and the record’s `Response to round 5` confirm that the seventh review was answered. Update the count.

HIGHEST: P1
OVERALL: needs-attention

## Response to round 6

This record's round 6 is the spec's eighth review round. Every finding was verified and is real.

1. P1, recovery deletes the temporary name without proving it: verified. A file at the temporary name is deleted only when its hash equals the new data's recorded hash; a partial one is kept and listed in the recovery report. Proof added.
2. P2, invariants 1 and 5 conflict with invariant 3: verified. The invariants now state that 1 and 5 hold when no other program touches the target's name, and define the conflict outcome (every version kept under a named path, the save reported not completed, the user told), which the proofs check.
3. P1, protections compared before a concurrent change are not bound to the displaced file: verified against File Security and Access Rights. The temporary file is created narrower than any target could be (user and SYSTEM only, a no-read-up and no-write-up label, EFS with the target's key holders), and the full contract is applied after the commit from the displaced version itself, read from the backup name; invariant 2 is restated against the displaced version. Proof added for a DACL tightened and a key holder added during a save.
4. P2, DPAPI user scope roams: verified against `CryptProtectData`'s remarks. The claim is corrected to the user, not the machine; the recovery folder is local, non-roaming app data, so checkpoints reach another machine only in a portable copy.
5. P3, the status line's round count: verified and corrected.

## Round 7: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-22T21:56:16Z
- Effort: xhigh
- Lines: 18
- Digest: 3c48881e11ca5d53

## adversarial: needs-attention

1. P1 `docs/specs/2026-10-22-native-stack-design.md:92`: Recovery does not finish the newly deferred file identity transfer before deleting the backup. Save a target containing `Zone.Identifier` or another named data stream, then kill the app immediately after the installation rename, before that stream is copied. Recovery accepts the new document hash, deletes the matching old backup, and retires the journal without transferring the stream. This permanently loses data or protection required by line 88. Backup deletion must wait for verified completion of the identity contract, including during recovery.

## consistency: needs-attention

2. P2 `docs/specs/2026-10-22-native-stack-design.md:86`: The fixed conflict outcome covers more interleavings than the reference sequence can produce. Start saving N from original A, then let another program overwrite A with B before the first rename. Line 87 moves B to the backup and installs N at the target; it cannot produce the promised A-at-backup, B-at-target, N-at-temporary outcome. A may already have been destroyed by the external writer. Scope the guarantee to attainable preservation outcomes and make the reference sequence and proofs agree.

## integration: approve

## source-defect: needs-attention

3. P1 `docs/specs/2026-10-22-native-stack-design.md:87`: The changed-encryption fallback contradicts the claim that temporary protections are always narrower. Start with an unencrypted target and temporary file in an unencrypted NTFS folder. Pause the save, encrypt the target with `EncryptFileW`, then resume. The displaced version is now EFS protected, but the specified fallback permits leaving the replacement plaintext with a restrictive DACL and merely reporting the change. That violates invariant 2. Microsoft’s [File Security and Access Rights](https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights) distinguishes encryption’s protection on the storage media from ACL enforcement; [EncryptFileW](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-encryptfilew) documents the encryption operation. An ACL cannot substitute for preserving that encryption.

## record: approve

HIGHEST: P1
OVERALL: needs-attention

## Response to round 7

This record's round 7 is the spec's ninth review round. Every finding was verified and is real.

1. P1, recovery deletes the backup before the deferred contract is applied: verified. The backup is deleted only after every contract item has been applied from it and read back, in the save and in recovery, which finishes the transfer first. Proof added: a kill right after the commit with a named stream not yet applied.
2. P2, the conflict outcome promised versions another program may have destroyed: verified. The outcome now covers every file the save moves or finds, and states that a version another program overwrote in place before the save moved it was destroyed by that program.
3. P1, encryption added mid-save was only reported: verified against `EncryptFileW` and File Security and Access Rights. Invariant 2 now names protections another program adds mid-save, which are applied to the new file before the save is reported, encryption included (the new file is encrypted in place); the narrowness claim is limited to access control, and encryption follows the target as the save starts. Proof added: the target encrypted during a save.

## Round 8: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-22T22:02:27Z
- Effort: xhigh
- Lines: 22
- Digest: 32a3542030694734

## adversarial: needs-attention

1. P1 `docs/specs/2026-10-22-native-stack-design.md:87`: The deferred identity transfer has no durability boundary before backup deletion. The only specified flush precedes copying named streams; subsequent readback can read cached writes. Persist the backup deletion and journal retirement, then cut power before the copied stream reaches disk: document bytes can survive while a contracted stream is lost. Microsoft’s [File Caching](https://learn.microsoft.com/en-us/windows/win32/fileio/file-caching) documentation explicitly distinguishes readback from durable storage. Require durable completion of the transferred data and metadata before deleting the backup, and include them in the power-loss comparison.

## consistency: needs-attention

2. P2 `docs/specs/2026-10-22-native-stack-design.md:86`: Round 9’s conflict correction remains inconsistent with the reference sequence. Start saving N from A, let another program overwrite A with B, then resume without further interference. Line 87 moves B to the backup and successfully installs N at the target, discovering B’s different hash during cleanup. Line 86 instead requires N at the temporary name and the save reported as not completed. Distinguish a foreign displaced version from a file appearing between the renames, and specify attainable outcomes for both.

## integration: needs-attention

3. P2 `docs/specs/2026-10-22-native-stack-design.md:92`: The newly required recovery transfer is not replayable after successful backup deletion. Complete the contract transfer, delete the backup, then kill the process before journal retirement. On restart, the target matches the new hash, but recovery must apply and verify the contract from a backup that no longer exists. The recorded hashes cover document data, not proof that the transfer completed. Define a durable completion state and an explicit recovery branch for this ordinary interruption.

## source-defect: needs-attention

4. P1 `docs/specs/2026-10-22-native-stack-design.md:87`: The new `EncryptFileW` step retains an unsafe failure outcome. Encrypt the original mid-save, install the plaintext replacement, then have another process open the replacement before encryption runs. Microsoft documents that [EncryptFileW requires exclusive access](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-encryptfilew), so encryption fails. The specified fallback keeps the backup but leaves the replacement plaintext, still violating invariant 2. Define a safe failure transition instead of treating encryption as cleanup after commitment.

5. P1 `docs/specs/2026-10-22-native-stack-design.md:87`: Granting the saving user and SYSTEM is not necessarily narrower than the target’s DACL. For example, give the target a DACL allowing its current logon SID, then save while another logon session uses the same account. The temporary file’s account-SID grant permits that other session to read data before the deferred DACL transfer; equal integrity levels do not prevent it. Microsoft’s [Trustees](https://learn.microsoft.com/en-us/windows/win32/secauthz/trustees) documentation distinguishes account and logon-session trustees. Protection must derive from the target before writing, rather than assuming this fixed ACL is universally narrower.

## record: approve

HIGHEST: P1
OVERALL: needs-attention

## Response to round 8

This record's round 8 is the spec's tenth review round. Every finding was verified and is real (finding 1 against File Caching, finding 4 against `EncryptFileW`'s exclusive-access requirement, finding 5 against Trustees). The save sequence has drawn findings in eight consecutive rounds, each one a deeper concurrency or durability case of a prescribed Win32 sequence, so the sequence moved out of the spec: the spec keeps the invariants and the proofs, and the document safety foundation section designs the sequence and reviews it with its code and its kill and power-loss tests. The requirements rounds 3 to 10 established are kept in the spec as the inputs to that design, so nothing found here is dropped.

1. P1, no durability boundary before releasing the backup: verified. Invariant 6 requires every state a later step depends on, each applied contract item included, to be durable on the medium rather than readable from the cache, with the journal recording each durable state. Proof added: power loss after each durable state, with every contract item present.
2. P2, the conflict outcomes did not match the sequence: verified. Two conflicts now have separate fixed outcomes: a version at the target's name that is not the app's last one (the save completes, that version is kept, the user is told), and a file appearing while the new data is installed (the save does not complete, every version is kept).
3. P2, recovery not replayable after the backup's release: verified. Invariant 6's journal of durable states lets recovery resume from the last one and never need a released file. Proof added: a kill after the release and before the journal's retirement.
4. P1, encryption failure after the commit left the new file plaintext: verified. Invariant 7 rolls the save back when a step after the commit cannot complete safely. Proof added: encryption blocked by another program's open handle.
5. P1, a fixed user-and-SYSTEM DACL is not always narrower: verified. Invariant 2 requires the temporary file's protection to be derived from the target's own before any data is written. Proof added: a DACL granting only a logon session.
