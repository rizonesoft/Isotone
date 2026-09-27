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

## WPF

`TextBox` style `Photon.TextBox` (implicit): `Border PART_Chrome`, `ScrollViewer PART_ContentHost`, `TextBlock PART_Placeholder` (visible when `Text` is empty), `SelectionBrush="{DynamicResource state}"`, `SelectionTextBrush="{DynamicResource state-on}"`, `CaretBrush="{DynamicResource text-primary}"`. Errors come from `INotifyDataErrorInfo`; `Validation.ErrorTemplate` is replaced by the helper line.
