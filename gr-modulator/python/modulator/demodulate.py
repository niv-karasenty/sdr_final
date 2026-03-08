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
        self.threshold = threshold # Threshold for deciding whether a bit is 0 or 1 based on correlation values
        self.timeout = timeout # Number of symbols up to we ignore no bits found
        self.sps = int(self.samp_rate * self.t * 3) # samples per symbol
        self.preamble = np.repeat(-1.0, self.sps/3)
        self.string = ''
        self.demodulating_flag = False
        self.time_out_counter = 0
        self.preamble_to_check = np.array([])
        self.byte_to_demod = np.array([]) # This array will hold the samples for one byte

    # This function demodulates one byte at a time
    # Must recieve 8 symbols of samples
    def demodulate_byte(self, ):
        symbol_0 = np.repeat([1,-1,-1], self.sps/3)
        symbol_1 = np.repeat([1,1,-1], self.sps/3)

        bit_array = []

        for i in range(0,8):
            symbol = self.byte_to_demod[i*self.sps:(i+1)*self.sps]
            if np.correlate(symbol, symbol_0)/(self.sps) > self.threshold or np.correlate(symbol, symbol_1)/(self.sps) > self.threshold:
                print('Correlation value for symbol ' + str(i) + ': ' + str(np.correlate(symbol, symbol_0)/(self.sps)) + ' for bit 0 and ' + str(np.correlate(symbol, symbol_1)/(self.sps)) + ' for bit 1')
                if np.correlate(symbol, symbol_0)/(self.sps) > np.correlate(symbol, symbol_1)/(self.sps):
                    bit_array.append(0)
                    print('Added bit 0')
                else:
                    bit_array.append(1)
                    print('Added bit 1')
                self.time_out_counter = 0 # Reset timeout counter if we found a bit
            else: # If no bit was detected, we assume the packet is corrupted and stop demodulating
                print('No bit detected')
                if np.correlate(symbol, symbol_0)/(self.sps/3) > np.correlate(symbol, symbol_1)/(self.sps/3):
                    bit_array.append(0)
                else:
                    bit_array.append(1)

                self.time_out_counter += 1
            
        # Bits to char
        char_bits = bit_array
        char_bits = "".join(map(str,char_bits))
        char_bits = int(char_bits,2)
        self.string = self.string + chr(char_bits)
            
    # Checking if check_pre_amble and pre amble are the same, if so we can start demodulating
    # Without noise we just need to check wether the pre amble is the same as the one we check.
    # For later versions must be adjusted
    def check_preamble(self):
        if np.correlate(self.preamble_to_check, self.preamble)/(self.sps/3) > self.threshold: # If the correlation is above the threshold, we assume we found the preamble
            print('Correlation value: ' + str(np.correlate(self.preamble_to_check, self.preamble)/(self.sps/3)))
            return True
        else:
            return False


    # Standard work function, this will be activated every time we have a packet comming in
    def work(self, input_items, output_items):
        in0 = input_items[0]
        sample_counter = 0

        # Countinue checking for preamble until we find it or run out of samples
        while (not self.demodulating_flag) and sample_counter < len(in0):
            if len(self.preamble_to_check) < len(self.preamble): # We need to fill the preamble_to_check array until it's the same length as the preamble
                if len(in0) > len(self.preamble) - len(self.preamble_to_check): # If we have more samples in packet than we need to fill preamble
                    sample_counter = len(self.preamble) - len(self.preamble_to_check)
                    self.preamble_to_check = np.append(self.preamble_to_check, in0[:(len(self.preamble) - len(self.preamble_to_check))])
                    
                else: # If we don't have enough samples in packet to fill preamble
                    self.preamble_to_check = np.append(self.preamble_to_check, in0)
                    sample_counter = len(in0)
            # Check for preamble only once we have enough samples to compare
            if len(self.preamble_to_check) == len(self.preamble):
                if self.check_preamble():
                    self.demodulating_flag = True
                    print('Preamble found, starting demodulation')
                    break
                else:
                    # If we haven't found the preamble yet, we need to keep checking the incoming samples
                    self.preamble_to_check = np.roll(self.preamble_to_check, -1)
                    self.preamble_to_check[-1] = in0[sample_counter]
                    sample_counter += 1

        # Check if timeout has been reached
        if self.time_out_counter > self.timeout: # If we have reached the timeout, we assume the packet is corrupted and stop demodulating
            self.demodulating_flag = False
            self.time_out_counter = 0
            self.preamble_to_check = np.array([]) # Clear the preamble_to_check array for the next packet

        if self.demodulating_flag:
            while sample_counter < len(in0):
                self.byte_to_demod = np.append(self.byte_to_demod, in0[sample_counter])
                if (len(self.byte_to_demod) == self.sps * 8): # Once we have enough samples for one byte, we can demodulate it
                    self.demodulate_byte()
                    self.byte_to_demod = np.array([]) # Clear the byte_to_demod array for the next byte
                sample_counter += 1
        else:
            if len(self.string) > 0:
                print('Demodulated string: ' + self.string)
                self.string = '' # Clear the string for the next packet
        return len(input_items[0])
