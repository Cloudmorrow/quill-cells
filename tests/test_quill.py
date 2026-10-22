"""Cells' tests: the real record store and gate on this machine.

`cm quill test` runs them. Cells has no code: what is tested is that the
manifest installs, that everyone gets the first sheet, and that a sheet's
cells are kept exactly as typed and worked out by the kit's rules.
"""

import pytest

from cloudmorrow.quill.cells import Sheet
from cloudmorrow.quill.testing import Harness


@pytest.fixture()
def q():
    with Harness(".") as harness:
        yield harness


def test_everybody_gets_a_first_sheet_once(q):
    sheets = q.list("sheet")
    assert [s["name"] for s in sheets] == ["Budget"], "the budget is seeded the first time the sheets are listed"
    assert [s["name"] for s in q.list("sheet")] == ["Budget"], "and only once"
    budget = Sheet.from_field(sheets[0]["cells"])
    assert budget.shown("B5") == "1770" and budget.shown("B7") == "59"
    assert budget.raw("B5") == "=SUM(B1:B3)", "what was typed is what is kept"


def test_a_sheet_keeps_its_cells_as_typed(q):
    sheet = q.seed("sheet", name="Trip", cells={"A1": "Fuel", "B1": "80", "B2": "=B1*2", "C1": "'007"})
    kept = q.get("sheet", sheet.id)["cells"]
    assert kept == {"A1": "Fuel", "B1": "80", "B2": "=B1*2", "C1": "'007"}
    worked = Sheet.from_field(kept)
    assert worked.shown("B2") == "160" and worked.shown("C1") == "007"


def test_what_goes_wrong_shows_in_the_cell(q):
    sheet = q.seed("sheet", name="Odd", cells={"A1": "=1/0", "A2": "=A3", "A3": "=A2", "A4": "=NOPE(1)", "A5": "=\"x\"+1"})
    worked = Sheet.from_field(q.get("sheet", sheet.id)["cells"])
    assert [worked.shown(f"A{n}") for n in range(1, 6)] == ["#DIV/0!", "#CIRC!", "#CIRC!", "#NAME?", "#VALUE!"]
