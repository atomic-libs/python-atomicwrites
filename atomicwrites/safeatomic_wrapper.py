"""Internal adapter around the :mod:`safeatomic` package."""

from __future__ import annotations

__all__ = ["AtomicWriter", "atomic_write", "move_atomic", "replace_atomic"]

try:  # pragma: no cover - handled in tests
    from safeatomic import (
        AtomicWriter,
        atomic_write,
        move_atomic,
        replace_atomic,
    )
except Exception as exc:  # pragma: no cover - makes dependency explicit
    raise ImportError(
        "python-atomicwrites now depends on the 'safeatomic' package."
        " Please install safeatomic to use this compatibility wrapper."
    ) from exc
