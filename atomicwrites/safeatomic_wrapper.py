# atomicwrites/safeatomic_wrapper.py

"""Internal adapter around the :mod:`safeatomic` package for legacy atomicwrites API."""

from __future__ import annotations
import os
import errno
import inspect
from typing import Any

try:
    import safeatomic as _safeatomic  # type: ignore
except Exception as exc:
    raise ImportError(
        "python-atomicwrites now depends on the 'safeatomic' package. "
        "Please install safeatomic to use this compatibility wrapper."
    ) from exc

__all__ = ["atomic_write", "replace_atomic", "move_atomic", "AtomicWriter"]

# Garantir que safeatomic tenha replace_atomic para monkeypatch nos testes
if not hasattr(_safeatomic, "replace_atomic") and hasattr(_safeatomic, "move_atomic_force"):
    _safeatomic.replace_atomic = _safeatomic.move_atomic_force


def atomic_write(path, writer_cls=None, **cls_kwargs):
    overwrite = cls_kwargs.get("overwrite", None)
    if overwrite is False and os.path.exists(path):
        import errno
        raise OSError(errno.EEXIST, os.strerror(errno.EEXIST))

    if writer_cls is None:
        writer_cls = AtomicWriter

    safe_fn = getattr(_safeatomic, "atomic_write", None)
    if callable(safe_fn):
        try:
            return safe_fn(path, writer_cls=writer_cls, **cls_kwargs)
        except TypeError:
            pass  # não suporta writer_cls, cair para fallback

    return writer_cls(path, **cls_kwargs)


if not hasattr(_safeatomic, "replace_atomic"):
    _safeatomic.replace_atomic = lambda src, dst: _safeatomic.move_atomic_force(src, dst)

def replace_atomic(src, dst):
    return _safeatomic.replace_atomic(src, dst)


def move_atomic(src: Any, dst: Any):
    """Legacy move_atomic -> safeatomic.move_atomic."""
    return _safeatomic.move_atomic(src, dst)


class AtomicWriter(_safeatomic.AtomicWriter):
    """Wrapper para compatibilidade de parâmetros (overwrite -> force)."""

    def __init__(self, path: Any, mode: str = "w", overwrite: bool = False, **open_kwargs: Any) -> None:
        params = inspect.signature(_safeatomic.AtomicWriter.__init__).parameters
        kwargs = dict(open_kwargs)

        # Mapear overwrite para force
        if "force" in params:
            kwargs["force"] = overwrite

        # Compatibilidade com testes: definir atributos legados
        self.overwrite = overwrite
        self._permit_overwrite = overwrite

        # Se "mode" for aceito no safeatomic, passar; senão, ignorar
        if "mode" in params:
            kwargs["mode"] = mode
        elif "file_mode" in params:
            kwargs["file_mode"] = mode

        super().__init__(path, **kwargs)
