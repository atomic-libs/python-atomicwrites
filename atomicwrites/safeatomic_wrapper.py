"""Internal adapter around the :mod:`safeatomic` package.

This module centralises imports from :mod:`safeatomic` and provides thin
wrappers so that :mod:`atomicwrites` continues to expose the historic API.
The wrappers keep the original function signatures while delegating all
implementation details to :mod:`safeatomic`.
"""

from __future__ import annotations

from typing import Any
import inspect

try:  # pragma: no cover - handled in tests
    import safeatomic as _safeatomic  # type: ignore
except Exception as exc:  # pragma: no cover - makes dependency explicit
    raise ImportError(
        "python-atomicwrites now depends on the 'safeatomic' package."
        " Please install safeatomic to use this compatibility wrapper."
    ) from exc

__all__ = ["atomic_write", "replace_atomic", "move_atomic", "AtomicWriter"]


def atomic_write(path: Any, writer_cls: type | None = None, **cls_kwargs: Any):
    """Proxy to :func:`safeatomic.atomic_write` keeping backward signature."""

    if writer_cls is None:
        writer_cls = AtomicWriter
    return _safeatomic.atomic_write(path, writer_cls=writer_cls, **cls_kwargs)


def replace_atomic(src: Any, dst: Any):
    """Proxy to :func:`safeatomic.replace_atomic`."""

    return _safeatomic.replace_atomic(src, dst)


def move_atomic(src: Any, dst: Any):
    """Proxy to :func:`safeatomic.move_atomic`."""

    return _safeatomic.move_atomic(src, dst)


class AtomicWriter(_safeatomic.AtomicWriter):
    """Compatibility wrapper around :class:`safeatomic.AtomicWriter`.

    The original :mod:`atomicwrites` exposed an ``AtomicWriter`` with the
    signature ``(path, mode="w", overwrite=False, **open_kwargs)``.  The
    underlying :mod:`safeatomic` implementation may use different parameter
    names (for example ``permit_overwrite`` instead of ``overwrite``).  This
    wrapper translates the historic arguments to whatever the wrapped class
    expects so that existing code keeps working.
    """

    def __init__(self, path: Any, mode: str = "w", overwrite: bool = False, **open_kwargs: Any) -> None:
        params = inspect.signature(_safeatomic.AtomicWriter.__init__).parameters
        kwargs = dict(open_kwargs)
        if "mode" in params:
            kwargs["mode"] = mode
        elif "file_mode" in params:
            kwargs["file_mode"] = mode
        else:
            kwargs["mode"] = mode

        if "overwrite" in params:
            kwargs["overwrite"] = overwrite
        elif "permit_overwrite" in params:
            kwargs["permit_overwrite"] = overwrite
        elif overwrite:
            raise TypeError("safeatomic.AtomicWriter does not support overwrite flag")

        if "dir" in kwargs and "dir" not in params and "tmp_dir" in params:
            kwargs["tmp_dir"] = kwargs.pop("dir")

        super().__init__(path, **kwargs)

