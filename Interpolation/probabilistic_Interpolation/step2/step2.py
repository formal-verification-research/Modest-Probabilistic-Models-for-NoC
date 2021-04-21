import os

dataFolder = "./data/"
mathsat = "/mnt/home/benjaylew/tools/mathsat-5.6.0-linux-x86_64/bin/mathsat"

for val in range (0,3):
    if(val == 2):
        val0 = 3
    else:
        val0 = val
    for val1 in range (0,3):
        print(val0, ',', val1)
        command = mathsat + " step2_a2" + str(val0) +"_a3"+str(val1)+".smt2 > " + dataFolder + "output"+str(val0)+str(val1)+".txt"
        os.system(command)
