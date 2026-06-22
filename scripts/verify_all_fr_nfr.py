#!/usr/bin/env python
"""Wrapper executing Functional and Non-Functional requirements verification runner."""

from __future__ import annotations

import sys

from app.evals.fr_nfr.run_fr_nfr_verification import run_checks

if __name__ == "__main__":
    sys.exit(run_checks())
