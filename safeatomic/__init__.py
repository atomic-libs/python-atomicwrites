import contextlib
import io
import os
import tempfile

DEFAULT_MODE = "w"


def replace_atomic(src, dst):
    os.replace(src, dst)


def move_atomic(src, dst):
    os.link(src, dst)
    os.unlink(src)


class AtomicWriter:
    def __init__(self, path, mode=DEFAULT_MODE, permit_overwrite=False, **open_kwargs):
        if "a" in mode:
            raise ValueError("Appending is not supported")
        if "x" in mode:
            raise ValueError("Use permit_overwrite instead")
        if "w" not in mode:
            raise ValueError("AtomicWriter can only write")
        self._path = path
        self._mode = mode
        self._permit_overwrite = permit_overwrite
        self._open_kwargs = open_kwargs

    def open(self):
        return self._open(self.get_fileobject)

    @contextlib.contextmanager
    def _open(self, get_fileobject):
        f = None
        try:
            success = False
            with get_fileobject(**self._open_kwargs) as f:
                yield f
                self.sync(f)
            self.commit(f)
            success = True
        finally:
            if not success and f is not None:
                self.rollback(f)

    def get_fileobject(self, suffix="", prefix=tempfile.gettempprefix(), dir=None, **kwargs):
        if dir is None:
            dir = os.path.dirname(self._path) or None
        descriptor, name = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=dir)
        os.close(descriptor)
        kwargs.setdefault("mode", self._mode)
        kwargs["file"] = name
        return io.open(**kwargs)

    def sync(self, f):
        f.flush()
        os.fsync(f.fileno())

    def commit(self, f):
        if self._permit_overwrite:
            replace_atomic(f.name, self._path)
        else:
            move_atomic(f.name, self._path)

    def rollback(self, f):
        os.unlink(f.name)


def atomic_write(path, writer_cls=AtomicWriter, **cls_kwargs):
    return writer_cls(path, **cls_kwargs).open()
