"""Compatibility wrapper around the :mod:`safeatomic` package."""

from __future__ import annotations

from .safeatomic_wrapper import (
    AtomicWriter,
    atomic_write,
    move_atomic,
    replace_atomic,
)

__all__ = ["AtomicWriter", "atomic_write", "move_atomic", "replace_atomic"]

__version__ = "2.0.0"
