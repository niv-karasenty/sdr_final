#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2026 gr-modulator author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr

class demodulate(gr.sync_block):
    """
    demodulating a block using our modulation scheme
    """
    def __init__(self, t, samp_rate, threshold, timeout):
        gr.sync_block.__init__(self,
            name="demodulator",
            in_sig=[np.float32, ],
            out_sig=None)
        self.t = t
        self.samp_rate = samp_rate
        self.threshold = threshold
        self.timeout = timeout
        self.sps = int(self.samp_rate * self.t * 3) # samples per symbol
        self.preamble = -1.0
        self.sample_queue = []
        self.string = ''

    def demodulate(self):
        symbol_0 = np.repeat([1,-1,-1], self.sps/3)
        symbol_1 = np.repeat([1,1,-1], self.sps/3)

        bit_array = []

        for i in range(0,len(self.sample_queue)-1,self.sps):
            symbol = self.sample_queue[i:i+self.sps-1]
            if symbol * symbol_0 > symbol * symbol_1:
                bit_array.append(0)
            else:
                bit_array.append(1)

        for i in range(0,len(bit_array)-1,8):
            char_bits = bit_array[i:i+7]
            char_bits = "".join(map(str,char_bits))
            char_bits = int(char_bits,2)
            print(chr(char_bits))
            self.string = self.string + chr(char_bits)
            

    def work(self, input_items, output_items):
        in0 = input_items[0]
        for i in range(len(in0)):
            if in0[i:i+len(self.preamble)] == self.preamble:
                self.sample_queue = in0[i+len(self.preamble)+1:]
                break

        self.demodulate()
        
        # <+signal processing here+>
        return len(input_items[0])
