"""--min-overlap: from 12 to 20, carried through to the recommendation and the report; anything else is refused."""
import pytest

from amplitrim import cli
from amplitrim.api import recommend
from conftest import need_vsearch


@need_vsearch
def test_a_larger_minimum_overlap_gives_a_longer_total_and_is_reported(reads, tmp_path):
    _r, _p, base = recommend(reads, tmp_path / "w12", tmp_path / "o12")
    _r, _p, wide = recommend(reads, tmp_path / "w20", tmp_path / "o20", min_overlap=20)
    total = lambda s: s["recommended"]["truncLenF"] + s["recommended"]["truncLenR"]
    assert base["recommended"]["minOverlap"] == 12 and wide["recommended"]["minOverlap"] == 20
    assert total(wide) > total(base)                      # the amplicon plus a longer overlap needs more bases


@pytest.mark.parametrize("value", ["11", "21", "30", "x"])
def test_the_command_line_refuses_values_outside_12_to_20(reads, tmp_path, value, capsys):
    with pytest.raises(SystemExit) as stop:
        cli.main(["--input-dir", str(reads), "--work-dir", str(tmp_path / "w"), "--out-dir", str(tmp_path / "o"), "--min-overlap", value])
    assert stop.value.code == 2
    err = capsys.readouterr().err
    assert "minimum overlap must be between 12 and 20" in err or "is not a whole number" in err
