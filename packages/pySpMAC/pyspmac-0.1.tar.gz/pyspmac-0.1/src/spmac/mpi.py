# SPDX-License-Identifier: MPL-2.0
# Copyright (C) 2024- SpM-lab
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

MPI4PY = False

import numpy as np

try:
    from mpi4py import MPI
    MPI4PY = True
    def get_size():
        return MPI.COMM_WORLD.Get_size()
    def get_rank():
        return MPI.COMM_WORLD.Get_rank()
    def allreduce_sum(src):
        buf = np.zeros_like(src)
        MPI.COMM_WORLD.Allreduce(src, buf)
        return buf
    def bcast(src, root=0):
        return MPI.COMM_WORLD.bcast(src, root=root)
except ImportError:
    MPI4PY = False
    def get_size():
        return 1
    def get_rank():
        return 0
    def allreduce_sum(src):
        return src[:]
    def bcast(src, root=0):
        return src