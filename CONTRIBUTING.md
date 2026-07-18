# Contributing

Thanks for taking a look.

## Development setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

## Before opening a pull request

- Keep changes focused. One logical change per PR, not a drive-by rewrite.
- Add or update tests for any behaviour you change. CI runs `pytest` on
  Python 3.9, 3.11, and 3.13, plus the example and benchmark, so it will
  find you.
- Run `ruff check .` and `pytest -q` locally before you push.
- If you touch the revision logic in `agents.py`, run the benchmark and check
  that debate still beats a single agent by a healthy margin and does not
  regress below plain voting; the whole point is that both of those hold.
- New questions in `corpus.py` should include distractors that are plausible
  wrong answers, not random noise. Uniformly random distractors make voting
  trivially easy and hide the real dynamic.

## Reporting bugs

Open an issue with a minimal reproduction, the expected versus actual result,
and your Python version. For security issues see [SECURITY.md](SECURITY.md).
