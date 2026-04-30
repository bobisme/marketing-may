"""
Make scripts/ importable as a package for tests.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Add project root to sys.path so `import scripts.foo` works without packaging.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
