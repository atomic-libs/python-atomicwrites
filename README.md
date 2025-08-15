# python-atomicwrites

Compatibility layer for legacy [`atomicwrites`](https://github.com/untitaker/python-atomicwrites) users, powered by [`safeatomic`](https://github.com/atomic-libs/safeatomic).

The original [`atomicwrites`](https://pypi.org/project/atomicwrites/) project by [Markus Unterwaditzer](https://github.com/untitaker) is no longer maintained after PyPI's 2FA enforcement.  
This repository is a **from-scratch rewrite** that keeps the historic `atomicwrites` API but delegates all file operations to the actively maintained [`safeatomic`](https://github.com/atomic-libs/safeatomic) package.

## Purpose

- Preserve drop-in compatibility with existing `atomicwrites`-based code.
- Allow seamless migration to `safeatomic` without changing existing imports.
- Maintain API stability for projects that cannot refactor immediately.

## Installation

```bash
pip install https://github.com/atomic-libs/safeatomic
pip install https://github.com/atomic-libs/python-atomicwrites
````

> **Note**: The `python-atomicwrites` package is just a thin wrapper and requires `safeatomic` to be installed.

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

## Upstream Reference

* Original unmaintained repo: [untitaker/python-atomicwrites](https://github.com/untitaker/python-atomicwrites)
* PyPI page: [atomicwrites](https://pypi.org/project/atomicwrites/)
