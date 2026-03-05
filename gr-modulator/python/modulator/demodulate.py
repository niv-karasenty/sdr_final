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
        self.preamble_to_check = []
        self.pre_amble_valid_flag = False

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
            
    # Checking if check_pre_amble and pre amble are the same, if so we can start demodulating
    # Without noise we just need to check wether the pre amble is the same as the one we check.
    # For later versions must be adjusted
    def check_preamble(self):
        if self.check_preamble == self.preamble:
            self.pre_amble_valid_flag = True
        else:
            self.pre_amble_valid_flag = False


    def work(self, input_items, output_items):
        in0 = input_items[0]
        if self.pre_amble_left > 0:
            self.preamble_to_check = np.append(self.preamble_to_check, in0[:self.pre_amble_left])
        else:
            for i in range(len(in0)):
                if len(in0[i:]) < len(self.preamble):
                    self.preamble_to_check = in0[i:]
                    self.pre_amble_left = len(self.preamble) - i
                    check_preamble()
                    break
                else:
                    self.preamble_to_check = in0[i:i+len(self.preamble)]
        
        if self.pre_amble_valid_flag: # Checking if we have found preamble
            demodulate()
        return len(input_items[0])
