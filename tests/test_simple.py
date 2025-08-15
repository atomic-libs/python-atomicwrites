# tests/test_simple.py

import os
from atomicwrites import atomic_write, replace_atomic, move_atomic, AtomicWriter

# Create temp.txt for testing replace_atomic
with open("temp.txt", "w") as f:
    f.write("temporary file")

# First replace_atomic
replace_atomic("temp.txt", "target.txt")
assert os.path.exists("target.txt")

# Write atomically to a file
with atomic_write("example.txt", overwrite=True) as f:
    f.write("Hello, world!")

# Prepare files again for replace_atomic
with open("temp.txt", "w") as f:
    f.write("temporary file again")

replace_atomic("temp.txt", "target.txt")
assert os.path.exists("target.txt")

# Prepare files for move_atomic
with open("source.txt", "w") as f:
    f.write("moving file")

move_atomic("source.txt", "destination.txt")
assert os.path.exists("destination.txt")

print("✅ All tests passed")
