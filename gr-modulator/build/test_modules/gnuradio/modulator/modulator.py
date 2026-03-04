#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2026 N.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr
import bitarray

# This function returns 
def str_to_bits(s):
    ords = (ord(c) for c in s)
    shifts = (7, 6, 5, 4, 3, 2, 1, 0)
    return [(o >> shift) & 1 for o in ords for shift in shifts]

class modulator(gr.sync_block):
    """
    docstring for block modulator
    """
    def __init__(self, t, samp_rate, input_str):
        gr.sync_block.__init__(self,
            name="modulator",
            in_sig=None,
            out_sig=[np.float32, ])
        self.t = t
        self.samp_rate = sampe_rate
        self.input_str = input_str
        self.queue = []

        self.enqueue_from_string()

    def enqueue_from_string(self):
        bit_array = str_to_bits(self.input_str)
        

    def work(self, input_items, output_items):
        out = output_items[0]
        # <+signal processing here+>
        out[:] = whatever
        return len(output_items[0])