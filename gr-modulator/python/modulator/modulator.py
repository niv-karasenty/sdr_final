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

# This function returns a vector of bits for the coresponding chars
# The bits order is big-endian, meaning the most significant bit of each character comes first in the output vector.
def str_to_bits(s):
    ords = (ord(c) for c in s)
    shifts = (7, 6, 5, 4, 3, 2, 1, 0)
    return [(o >> shift) & 1 for o in ords for shift in shifts]

class modulator(gr.sync_block):
    """
    Modulating some initial string to our modulation scheme. 
    """
    def __init__(self, t, samp_rate, input_str):
        gr.sync_block.__init__(self,
            name="modulator",
            in_sig=None,
            out_sig=[np.float32, ])
        self.t = t # Duration of one part (which is 1/3 of a symbol) in seconds
        self.samp_rate = samp_rate
        self.input_str = input_str
        self.sps = int(self.samp_rate * self.t * 3) # samples per symbol
        self.preamble = -1.0
        self.sample_queue = [self.preamble] # Start with preamble

        self.enqueue_from_string()

    def enqueue_from_string(self):
        bit_array = str_to_bits(self.input_str)
        for bit in bit_array:
            if bit == 0:
                self.sample_queue.append(1.0, -1.0, -1.0) # '0' is represented by [1.0, -1.0, -1.0]
            else:
                self.sample_queue.append(1.0, 1.0, -1.0) # '1' is represented by [1.0, 1.0, -1.0]

    def work(self, input_items, output_items):
        out = output_items[0]
        for i in range(0, len(out) - 1):
            if self.sample_queue:
                out[i] = self.sample_queue.pop(0)
            else:
                out[i] = 0.0 # Fill the rest with zeros if the queue is empty
        return len(output_items[0])