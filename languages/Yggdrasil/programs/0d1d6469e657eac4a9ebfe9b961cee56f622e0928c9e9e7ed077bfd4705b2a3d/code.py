# Simple file system specification using Yggdrasil
# Yggdrasil: A Machine-Checked Construction of File Systems
# From: https://github.com/uw-unsat/yggdrasil

from z3 import *

# Disk model: array of blocks
BlockSize = 512
NumBlocks = 1024

def make_disk():
    return Array('disk', BitVecSort(32), BitVecSort(8 * BlockSize))

def disk_read(disk, blkno):
    return disk[blkno]

def disk_write(disk, blkno, data):
    return Store(disk, blkno, data)

# File system invariant: superblock is valid
def fs_invariant(disk):
    sb = disk_read(disk, BitVecVal(0, 32))  # superblock at block 0
    magic = Extract(31, 0, sb)  # first 4 bytes are magic number
    return magic == BitVecVal(0xDEADBEEF, 32)

# Verify that writes preserve the invariant
def verify_write_preserves_invariant():
    disk = make_disk()
    blkno = BitVec('blkno', 32)
    data = BitVec('data', 8 * BlockSize)

    s = Solver()
    # Assume invariant holds before write
    s.add(fs_invariant(disk))
    # Write to non-superblock location
    s.add(UGT(blkno, BitVecVal(0, 32)))
    new_disk = disk_write(disk, blkno, data)
    # Check invariant still holds
    s.add(Not(fs_invariant(new_disk)))

    result = s.check()
    if result == unsat:
        print("Verified: writes to non-superblock preserve fs invariant")
    else:
        print("Counterexample found:", s.model())

if __name__ == '__main__':
    verify_write_preserves_invariant()
