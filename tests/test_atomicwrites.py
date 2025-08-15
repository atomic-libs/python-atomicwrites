# tests/test_atomicwrites.py

import os
import sys
import errno
import pytest

# Garantir que o pacote local seja usado ao rodar direto
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import safeatomic
from atomicwrites import AtomicWriter, atomic_write, replace_atomic, move_atomic


def test_atomic_write_creates_file(tmpdir):
    fname = tmpdir.join("file.txt")
    with atomic_write(str(fname), overwrite=True) as f:
        f.write("hello")

    assert fname.read() == "hello"
    assert len(tmpdir.listdir()) == 1


def test_atomic_write_overwrite_false(tmpdir):
    fname = tmpdir.join("file.txt")
    with atomic_write(str(fname), overwrite=True) as f:
        f.write("data")

    with pytest.raises(OSError) as excinfo:
        with atomic_write(str(fname), overwrite=False) as f:
            f.write("new data")

    assert excinfo.value.errno == errno.EEXIST
    assert fname.read() == "data"


def test_atomic_write_wrapper(monkeypatch):
    called = {}

    def fake_atomic_write(path, writer_cls=AtomicWriter, **kwargs):
        called["args"] = (path, writer_cls, kwargs)
        return "ok"

    monkeypatch.setattr(safeatomic, "atomic_write", fake_atomic_write)

    result = atomic_write("/tmp/foo", overwrite=True)

    assert result == "ok"
    assert called["args"][0] == "/tmp/foo"
    assert called["args"][1] is AtomicWriter
    assert called["args"][2] == {"overwrite": True}


def test_replace_atomic_wrapper(monkeypatch):
    called = {}

    def fake_replace(src, dst):
        called["args"] = (src, dst)

    monkeypatch.setattr(safeatomic, "replace_atomic", fake_replace)

    replace_atomic("a", "b")
    assert called["args"] == ("a", "b")


def test_move_atomic_wrapper(monkeypatch):
    called = {}

    def fake_move(src, dst):
        called["args"] = (src, dst)

    monkeypatch.setattr(safeatomic, "move_atomic", fake_move)

    move_atomic("src.txt", "dst.txt")
    assert called["args"] == ("src.txt", "dst.txt")


def test_atomicwriter_is_subclass():
    assert issubclass(AtomicWriter, safeatomic.AtomicWriter)


def test_atomicwriter_overwrite_mapping(tmpdir):
    # Apenas verifica se a flag overwrite é propagada corretamente
    aw = AtomicWriter(tmpdir.join("file.txt"), overwrite=True)
    assert getattr(aw, "_permit_overwrite", None) is True or \
           getattr(aw, "overwrite", None) is True


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
