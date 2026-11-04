# Changelog

## 0.2.0

- `--min-overlap` sets the minimum overlap between the forward and the reverse read, from 12 to 20 nt (default 12, DADA2's default for `mergePairs`). It sets the shortest total length (the longest amplicon plus the overlap), is used in the merge tests, and appears as `minOverlap` in the report and in `summary.json`. Use the same value in your DADA2 `mergePairs` call. The validation was run at 12.
- `amplitrim.api.recommend()` is a programmatic entry point that returns the result, the path of the report and the parsed `summary.json`, and raises `PipelineError` or `RuntimeError` for bad input or a missing vsearch. The command line now calls it, so a script, a workflow wrapper and the command line give the same answer.
- Three optional arguments (`--its`, `--min-overlap`, `--verbose`).
- A comment in `config.py` no longer claims command-line options that did not exist.
- The run time and memory of a run were measured (34 to 54 seconds and at most 292 MB on three real datasets), and the default minimum overlap of 12 nt was tested against 10, 15, 20 and 25 nt on four mock communities (validation archive, register sections 27 and 28).

## 0.1.0

First release.

- Recommends DADA2 `truncLenF`, `truncLenR` and `maxEE` for paired-end amplicon reads. It measures amplicon lengths from the reads, replicates DADA2's quality filter exactly for every forward/reverse split, and tests real merges with vsearch.
- `maxEE` is recommended, not given: per read, the limit that covers three quarters of the reads at the recommended cut (never below 2, with no upper limit; the report notes a limit above 5); clean reads stay at 2.
- `--its` for amplicons that vary in length (no fixed truncation length; each read is still trimmed at its first base of quality 2 or below). Its report shows where the pairs go and what the forward reads alone would keep.
- Three required arguments and two optional ones (`--its`, `--verbose`).
- One runtime dependency, numpy. matplotlib is optional (`pip install "amplitrim[plot]"`) and only draws `summary.png`: without it the report and `summary.json` are written as usual.
- A command that makes a small simulated dataset for trying the tool (`tests/simulate.py`; see the README). The evidence for each recommendation is on the [validation page](https://github.com/paytonyau/amplitrim-validation/blob/main/docs/validation.md) of the validation archive.
- Report (`REPORT.md`, `summary.png`, `summary.json`) with copy-paste snippets for DADA2 and QIIME 2. `summary.json` is meant for scripts and workflow managers: it has a `schema_version`, always-numeric `maxEE_f` and `maxEE_r`, and a `maxEE_rule` that says whether `maxEE` was relaxed.
