# Cells

A Quill for [Cloudmorrow](https://github.com/Cloudmorrow/cloudmorrow): small
spreadsheets — cells, numbers and formulas — on the phone, the web app, the
terminal and the command line.

- A sheet is cells in rows and columns. Type text, a number, or a formula
  starting with `=`: `=SUM(B1:B3)`, `=IF(B5>1000, "over", "under")`,
  `=ROUND(B5/30, 2)`. The useful part of Excel's formulas, and nothing of
  the rest of Excel: no pivots, no charts, no macros.
- What a formula comes to is worked out as you type, by the same rules on
  every surface, so a sheet never says one thing on the phone and another
  in the terminal. What goes wrong shows in the cell: `#DIV/0!`, `#REF!`,
  `#NAME?`, `#VALUE!`, `#CIRC!`.
- A sheet is a record of the foundational `sheet` datamodel: a name, and its
  cells kept exactly as typed, in one field — open to any other Quill, to
  `cm`, and to your assistant. Removing this Quill takes the tab away, never
  a sheet.
- It saves as you type. A sheet changed somewhere else since you opened it
  is never written over.

The formulas, and what each surface does, are
[docs/CELLS.md](https://github.com/Cloudmorrow/cloudmorrow/blob/main/docs/CELLS.md)
in the Cloudmorrow repository.

Install it from the Quill Catalog, or from this repository with
`cm quill add --source https://github.com/Cloudmorrow/quill-cells --ref v1.0.0`.

## What it adds to your Cloudmorrow

`cm quill check` prints this for you; keep it here for the catalog page.

| | |
| --- | --- |
| Datamodels | uses `sheet` |
| Screens | Cells: the sheets, and one open as a grid — on the phone, the web app, the terminal, `cm cells`, and to your assistant |
| Datasets | a first sheet, Budget, for everyone once |
| Code | none |

## On the command line

```
cm cells list                          # every sheet, newest first
cm cells add "Trip"                    # a new, empty sheet
cm cells show Budget                   # the sheet, worked out, as a table
cm cells show Budget --raw             # as typed: the formulas
cm cells get Budget B5                 # one cell, worked out
cm cells set Budget B3 150             # one cell; set Budget B3 "" clears it
cm cells set Budget B5 "=SUM(B1:B3)"
cm cells set Budget name=Costs         # the sheet's own fields
cm cells show Budget --plain           # the cells as JSON, for scripts
```

## Working on it

```
uv sync                  # .venv with Cloudmorrow and pytest
cm quill check           # the manifest, as a server would install it
cm quill test            # tests/, against the real record store and gate
cm quill dev --local     # a throwaway server here, reinstalled as you save
```
