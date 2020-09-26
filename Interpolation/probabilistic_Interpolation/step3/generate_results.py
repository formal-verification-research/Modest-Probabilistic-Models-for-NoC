import os

for val in range (0,3):
    if(val == 2):
        val0 = 3
    else:
        val0 = val
    for val1 in range(0,3):
        command = "/home/benjaylew/mathsat-5.6.3-linux-x86_64/bin/mathsat step2_a2" + str(val0) + "_a3" + str(val1) + " > data/data" + str(val0) + "_" + str(val1) + ".txt"
        print(command)
        os.system(command)
