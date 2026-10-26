"""Cells' tests: the real record store, files and gate on this machine.

`cm quill test` runs them. Cells has no code: what is tested is that the
manifest installs, that everyone gets the first sheet, and that a sheet's
cells are kept exactly as typed in its .cell file and worked out by the
kit's rules.
"""

import pytest

from cloudmorrow.quill.cells import Sheet, file_text
from cloudmorrow.quill.testing import Harness


@pytest.fixture()
def q():
    with Harness(".") as harness:
        yield harness


IN_DOCUMENTS = {"share": "my-files", "within": "Documents", "suffix": ".cell"}


def test_everybody_gets_a_first_sheet_once(q):
    sheets = q.list("file", **IN_DOCUMENTS)
    assert [s["path"] for s in sheets] == ["Documents/Budget.cell"], "the budget is seeded the first time"
    assert [s["path"] for s in q.list("file", **IN_DOCUMENTS)] == ["Documents/Budget.cell"], "and only once"
    budget = Sheet.from_text(q.get("file", sheets[0].id)["text"])
    assert budget.shown("B5") == "1770" and budget.shown("B7") == "59"
    assert budget.raw("B5") == "=SUM(B1:B3)", "what was typed is what is kept"


def test_a_sheet_keeps_its_cells_as_typed(q):
    cells = {"A1": "Fuel", "B1": "80", "B2": "=B1*2", "C1": "'007"}
    sheet = q.seed("file", share="my-files", path="Documents/Trip.cell", text=file_text(cells))
    kept = q.get("file", sheet.id)["text"]
    assert kept == '{\n  "cells": {\n    "A1": "Fuel",\n    "B1": "80",\n    "C1": "\'007",\n    "B2": "=B1*2"\n  }\n}\n'
    worked = Sheet.from_text(kept)
    assert worked.shown("B2") == "160" and worked.shown("C1") == "007"


def test_what_goes_wrong_shows_in_the_cell(q):
    cells = {"A1": "=1/0", "A2": "=A3", "A3": "=A2", "A4": "=NOPE(1)", "A5": '="x"+1'}
    sheet = q.seed("file", share="my-files", path="Documents/Odd.cell", text=file_text(cells))
    worked = Sheet.from_text(q.get("file", sheet.id)["text"])
    assert [worked.shown(f"A{n}") for n in range(1, 6)] == ["#DIV/0!", "#CIRC!", "#CIRC!", "#NAME?", "#VALUE!"]
