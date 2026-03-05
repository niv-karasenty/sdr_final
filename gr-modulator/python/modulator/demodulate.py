#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2026 gr-modulator author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr

class demodulate(gr.sync_block):
    """
    docstring for block demodulate
    """
    def __init__(self, t, samp_rate):
        gr.sync_block.__init__(self,
            name="demodulator",
            in_sig=[np.float32, ],
            out_sig=None)
        self.t = t
        self.samp_rate = samp_rate
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
        self.sample_queue = in0
        for sample in self.sample_queue:
            self.sample_queue.pop(0)
            if sample == self.preamble:
                break

        self.demodulate()
        
        # <+signal processing here+>
        return len(input_items[0])
