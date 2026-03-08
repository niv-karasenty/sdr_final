#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: nivkarasenty
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import modulator
import numpy as np
import threading



class noised(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "noised")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.SNR_dB = SNR_dB = 1
        self.timeout = timeout = 8
        self.threshold = threshold = 0.15
        self.t = t = 0.01
        self.samp_rate = samp_rate = 32000
        self.input_str = input_str = 'AAAA'
        self.f_delta = f_delta = 75000
        self.SNR_lin = SNR_lin = np.pow(10,(SNR_dB/10))

        ##################################################
        # Blocks
        ##################################################

        self.modulator_modulator_0 = modulator.modulator(t, int(samp_rate), input_str)
        self.modulator_demodulate_0 = modulator.demodulate(t, int(samp_rate), threshold, timeout)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_float*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, (1/(SNR_lin*samp_rate)), 0)
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc((2*np.pi*f_delta/samp_rate))
        self.analog_fm_demod_cf_0 = analog.fm_demod_cf(
        	channel_rate=samp_rate,
        	audio_decim=1,
        	deviation=f_delta,
        	audio_pass=15000,
        	audio_stop=16000,
        	gain=1.0,
        	tau=(75e-6),
        )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fm_demod_cf_0, 0), (self.modulator_demodulate_0, 0))
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.analog_fm_demod_cf_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.analog_frequency_modulator_fc_0, 0))
        self.connect((self.modulator_modulator_0, 0), (self.blocks_throttle2_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "noised")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_SNR_dB(self):
        return self.SNR_dB

    def set_SNR_dB(self, SNR_dB):
        self.SNR_dB = SNR_dB
        self.set_SNR_lin(np.pow(10,(self.SNR_dB/10)))

    def get_timeout(self):
        return self.timeout

    def set_timeout(self, timeout):
        self.timeout = timeout

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold

    def get_t(self):
        return self.t

    def set_t(self, t):
        self.t = t

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_frequency_modulator_fc_0.set_sensitivity((2*np.pi*self.f_delta/self.samp_rate))
        self.analog_noise_source_x_0.set_amplitude((1/(self.SNR_lin*self.samp_rate)))
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)

    def get_input_str(self):
        return self.input_str

    def set_input_str(self, input_str):
        self.input_str = input_str

    def get_f_delta(self):
        return self.f_delta

    def set_f_delta(self, f_delta):
        self.f_delta = f_delta
        self.analog_frequency_modulator_fc_0.set_sensitivity((2*np.pi*self.f_delta/self.samp_rate))

    def get_SNR_lin(self):
        return self.SNR_lin

    def set_SNR_lin(self, SNR_lin):
        self.SNR_lin = SNR_lin
        self.analog_noise_source_x_0.set_amplitude((1/(self.SNR_lin*self.samp_rate)))




def main(top_block_cls=noised, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
