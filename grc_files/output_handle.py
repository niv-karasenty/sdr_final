import numpy as np

file_name = '/Users/nivkarasenty/Desktop/niv/Delta/SDR_week/final_exercise/grc_files/output_file'
bin_array = np.fromfile(file_name, dtype=np.float32)

print('------------------------------')
print(bin_array)
print('------------------------------')