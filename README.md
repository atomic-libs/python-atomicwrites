# python-atomicwrites

Compatibility layer for legacy [`atomicwrites`](https://github.com/untitaker/python-atomicwrites) users, powered by [`safeatomic`](https://github.com/atomic-libs/safeatomic).

The original [`atomicwrites`](https://pypi.org/project/atomicwrites/) project by [Markus Unterwaditzer](https://github.com/untitaker) is no longer maintained after PyPI's 2FA enforcement.  
This repository is a **from-scratch rewrite** that preserves the historic `atomicwrites` API while delegating all file operations to the actively maintained [`safeatomic`](https://github.com/atomic-libs/safeatomic) package.

## Purpose

- Preserve drop-in compatibility with existing `atomicwrites`-based code.
- Allow seamless migration to `safeatomic` without changing existing imports.
- Maintain API stability for projects that cannot refactor immediately.

---

## Requirements

### Core dependencies
- [safeatomic](https://github.com/atomic-libs/safeatomic) (installed from GitHub)
- [click](https://pypi.org/project/click/) >= 8.2.1

### Development dependencies (`[dev]` extra)
- [build](https://pypi.org/project/build/)
- [twine](https://pypi.org/project/twine/)
- [pytest](https://pypi.org/project/pytest/)

---

## Installation

### Using pip

For development (includes dev dependencies):

```bash
pip install -e .[dev] git+https://github.com/atomic-libs/safeatomic.git
````

For runtime only:

```bash
pip install git+https://github.com/atomic-libs/safeatomic.git
pip install python-atomicwrites
```

---

### Using uv

For development:

```bash
uv pip install -e .[dev]
```

> **Note:** `safeatomic` is pulled directly from GitHub via `[tool.uv.sources]` in `pyproject.toml`.

For runtime only:

```bash
uv pip install python-atomicwrites
```

---

## Usage

The API matches the original `atomicwrites` module:

```python
from atomicwrites import atomic_write, replace_atomic, move_atomic, AtomicWriter

# Write atomically to a file
with atomic_write("example.txt", overwrite=True) as f:
    f.write("Hello, world!")

# Replace a file atomically
replace_atomic("temp.txt", "target.txt")

# Move a file atomically
move_atomic("source.txt", "destination.txt")
```

---

## Upstream Reference

* Original unmaintained repo: [untitaker/python-atomicwrites](https://github.com/untitaker/python-atomicwrites)
* PyPI page: [atomicwrites](https://pypi.org/project/atomicwrites/)

```

If you want, I can also prepare a matching **`requirements.txt`** so that both `pip install -r requirements.txt` and `uv pip install -r requirements.txt` work out-of-the-box.  
Do you want me to generate that file too?
```
