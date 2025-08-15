# atomicwrites/__init__.py

"""Compatibility wrapper around the :mod:`safeatomic` package.

This module exposes the historic :mod:`atomicwrites` API but delegates all
work to :mod:`safeatomic`.
"""

from __future__ import annotations

from .safeatomic_wrapper import AtomicWriter, atomic_write, move_atomic, replace_atomic

__all__ = ["atomic_write", "replace_atomic", "move_atomic", "AtomicWriter"]

__version__ = "1.5.0"
