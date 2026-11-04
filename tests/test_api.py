"""The programmatic entry point gives what the command line gives, and fails the same way."""
import json

import pytest

from amplitrim import cli
from amplitrim.api import PipelineError, recommend
from conftest import need_vsearch


@need_vsearch
def test_recommend_returns_the_summary_that_the_command_line_writes(reads, tmp_path, capsys):
    result, report, summary = recommend(reads, tmp_path / "w_api", tmp_path / "o_api")
    assert report.name == "REPORT.md" and report.exists()
    assert cli.main(["--input-dir", str(reads), "--work-dir", str(tmp_path / "w_cli"), "--out-dir", str(tmp_path / "o_cli")]) == 0
    capsys.readouterr()
    from_cli = json.loads((tmp_path / "o_cli" / "summary.json").read_text())
    assert summary["recommended"] == from_cli["recommended"]
    assert result.recommendation is not None


@need_vsearch
def test_recommend_its_mode_gives_no_fixed_truncation(reads, tmp_path):
    _result, _report, summary = recommend(reads, tmp_path / "w", tmp_path / "o", its=True)
    assert (summary["recommended"]["truncLenF"], summary["recommended"]["truncLenR"]) == (0, 0)


def test_recommend_raises_for_a_folder_without_pairs(tmp_path):
    (tmp_path / "in").mkdir()
    with pytest.raises((PipelineError, RuntimeError)):
        recommend(tmp_path / "in", tmp_path / "w", tmp_path / "o")
