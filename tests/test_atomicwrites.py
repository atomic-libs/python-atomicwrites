import errno
import os
import sys

# Ensure local packages are importable when running tests directly
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest

safeatomic = pytest.importorskip("safeatomic")

from atomicwrites import AtomicWriter, atomic_write, move_atomic, replace_atomic


def test_atomic_write(tmpdir):
    fname = tmpdir.join('ha')
    for i in range(2):
        with atomic_write(str(fname), overwrite=True) as f:
            f.write('hoho')

    with pytest.raises(OSError) as excinfo:
        with atomic_write(str(fname), overwrite=False) as f:
            f.write('haha')

    assert excinfo.value.errno == errno.EEXIST

    assert fname.read() == 'hoho'
    assert len(tmpdir.listdir()) == 1


def test_teardown(tmpdir):
    fname = tmpdir.join('ha')
    with pytest.raises(AssertionError):
        with atomic_write(str(fname), overwrite=True):
            assert False

    assert not tmpdir.listdir()


def test_replace_simultaneously_created_file(tmpdir):
    fname = tmpdir.join('ha')
    with atomic_write(str(fname), overwrite=True) as f:
        f.write('hoho')
        fname.write('harhar')
        assert fname.read() == 'harhar'
    assert fname.read() == 'hoho'
    assert len(tmpdir.listdir()) == 1


def test_dont_remove_simultaneously_created_file(tmpdir):
    fname = tmpdir.join('ha')
    with pytest.raises(OSError) as excinfo:
        with atomic_write(str(fname), overwrite=False) as f:
            f.write('hoho')
            fname.write('harhar')
            assert fname.read() == 'harhar'

    assert excinfo.value.errno == errno.EEXIST
    assert fname.read() == 'harhar'
    assert len(tmpdir.listdir()) == 1


# Verify that nested exceptions during rollback do not overwrite the initial
# exception that triggered a rollback.
def test_open_reraise(tmpdir):
    fname = tmpdir.join('ha')
    with pytest.raises(AssertionError):
        aw = atomic_write(str(fname), overwrite=False)
        with aw:
            # Mess with internals, so commit will trigger a ValueError. We're
            # testing that the initial AssertionError triggered below is
            # propagated up the stack, not the second exception triggered
            # during commit.
            aw.rollback = lambda: 1 / 0
            # Now trigger our own exception.
            assert False, "Intentional failure for testing purposes"


def test_atomic_write_in_pwd(tmpdir):
    orig_curdir = os.getcwd()
    try:
        os.chdir(str(tmpdir))
        fname = 'ha'
        for i in range(2):
            with atomic_write(str(fname), overwrite=True) as f:
                f.write('hoho')

        with pytest.raises(OSError) as excinfo:
            with atomic_write(str(fname), overwrite=False) as f:
                f.write('haha')

        assert excinfo.value.errno == errno.EEXIST

        assert open(fname).read() == 'hoho'
        assert len(tmpdir.listdir()) == 1
    finally:
        os.chdir(orig_curdir)


def test_atomic_write_wrapper(monkeypatch):
    called = {}

    def fake_atomic_write(path, writer_cls=AtomicWriter, **kwargs):
        called["args"] = (path, writer_cls, kwargs)
        return "ok"

    monkeypatch.setattr(safeatomic, "atomic_write", fake_atomic_write)

    res = atomic_write("/tmp/foo", overwrite=True)

    assert res == "ok"
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

    move_atomic("a", "b")

    assert called["args"] == ("a", "b")


def test_atomicwriter_is_subclass():
    assert issubclass(AtomicWriter, safeatomic.AtomicWriter)


def test_atomicwriter_overwrite_mapping(tmpdir):
    aw = AtomicWriter(tmpdir.join("ha"), overwrite=True)
    assert getattr(aw, "_permit_overwrite", None) is True
