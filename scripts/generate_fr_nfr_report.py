#!/usr/bin/env python
"""Wrapper regenerating FR/NFR requirement verification summary reports."""

from __future__ import annotations

import sys
from app.evals.fr_nfr.run_fr_nfr_verification import run_checks

if __name__ == "__main__":
    print("Regenerating requirements verification reports...")
    sys.exit(run_checks())
