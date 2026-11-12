# Text box

Single-line text entry: names, paths, search. Numeric values use NumberBox.

## Anatomy

| Part | Size | Tokens |
| --- | --- | --- |
| Field | `control-h-compact` 24px (dialogs 28px, Comfortable 30px), 8px side padding, `radius-sm` | `surface-field`, 1px `border-control` |
| Text | `body` | `text-primary`; placeholder `text-placeholder` |
| Leading icon | 14px (search) | `icon` |
| Helper or error line | `caption`, 4px below | `text-secondary`; error `status-error` with the `error` icon |

## States

- Rest; hover: border `border-control-hover`.
- Focus: border `focus-ring` plus a 1px inner `focus-ring` line (2px total, inside, so fields do not grow). Text selection uses `state` with `state-on` text.
- Disabled: no fill, `divider-strong` border, `text-disabled` text.
- Read-only: no fill, `divider-strong` border, `text-primary` text, still focusable and selectable.
- Error: `status-error` border and inner line, a message that says what is allowed ("Names can't contain / or \\"), never color alone.
- Placeholder: shown only while empty; not a label.

## Keyboard

Standard edit keys; Enter commits (in the options bar and panels also returns focus to the canvas); Escape reverts to the value at focus; Ctrl+A selects all. Single-letter tool shortcuts never fire while a field has focus.

## Native

One text box element over the shared text editing model of `isotone::ui` (grapheme-aware caret, bidirectional selection, undo grouping, input methods through the Text Services Framework, layout with DirectWrite): its chrome, a scrolling content area, and a placeholder shown when the text is empty. The selection is drawn with `state` and its text with `state-on`; the caret is `text-primary`. A validation error shows the helper line. UI Automation: Edit with the Value and Text patterns.
