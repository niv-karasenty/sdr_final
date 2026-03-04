#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/Users/nivkarasenty/Desktop/niv/Delta/SDR_week/final_exercise/gr-modulator/python/modulator
export GR_CONF_CONTROLPORT_ON=False
export PATH="/Users/nivkarasenty/Desktop/niv/Delta/SDR_week/final_exercise/gr-modulator/build/python/modulator":"$PATH"
export DYLD_LIBRARY_PATH="":$DYLD_LIBRARY_PATH
export PYTHONPATH=/Users/nivkarasenty/Desktop/niv/Delta/SDR_week/final_exercise/gr-modulator/build/test_modules:$PYTHONPATH
/opt/homebrew/Cellar/gnuradio/3.10.12.0_10/libexec/venv/bin/python /Users/nivkarasenty/Desktop/niv/Delta/SDR_week/final_exercise/gr-modulator/python/modulator/qa_modulator.py 
