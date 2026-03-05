# CMake generated Testfile for 
# Source directory: /Users/nivkarasenty/Desktop/niv/Delta/SDR_week/final_exercise/gr-modulator/python/modulator
# Build directory: /Users/nivkarasenty/Desktop/niv/Delta/SDR_week/final_exercise/gr-modulator/build/python/modulator
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(qa_modulator "/bin/sh" "qa_modulator_test.sh")
set_tests_properties(qa_modulator PROPERTIES  _BACKTRACE_TRIPLES "/opt/homebrew/lib/cmake/gnuradio/GrTest.cmake;119;add_test;/Users/nivkarasenty/Desktop/niv/Delta/SDR_week/final_exercise/gr-modulator/python/modulator/CMakeLists.txt;39;GR_ADD_TEST;/Users/nivkarasenty/Desktop/niv/Delta/SDR_week/final_exercise/gr-modulator/python/modulator/CMakeLists.txt;0;")
add_test(qa_demodulate "/bin/sh" "qa_demodulate_test.sh")
set_tests_properties(qa_demodulate PROPERTIES  _BACKTRACE_TRIPLES "/opt/homebrew/lib/cmake/gnuradio/GrTest.cmake;119;add_test;/Users/nivkarasenty/Desktop/niv/Delta/SDR_week/final_exercise/gr-modulator/python/modulator/CMakeLists.txt;40;GR_ADD_TEST;/Users/nivkarasenty/Desktop/niv/Delta/SDR_week/final_exercise/gr-modulator/python/modulator/CMakeLists.txt;0;")
subdirs("bindings")
