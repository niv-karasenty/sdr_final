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
    def __init__(self, t, samp_rate, threshold, timeout):
        gr.sync_block.__init__(self,
            name="demodulate",
            in_sig=[<+numpy.float32+>, ],
            out_sig=None)


    def work(self, input_items, output_items):
        in0 = input_items[0]
        # <+signal processing here+>
        return len(input_items[0])
