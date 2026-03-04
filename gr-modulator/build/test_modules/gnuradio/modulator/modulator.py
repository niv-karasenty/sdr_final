#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2026 N.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr

class modulator(gr.sync_block):
    """
    docstring for block modulator
    """
    def __init__(self, t, samp_rate, input_str):
        gr.sync_block.__init__(self,
            name="modulator",
            in_sig=None,
            out_sig=[np.float32, ])


    def work(self, input_items, output_items):
        out = output_items[0]
        # <+signal processing here+>
        out[:] = whatever
        return len(output_items[0])
