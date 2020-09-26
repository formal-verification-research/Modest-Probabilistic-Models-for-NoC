import os

for val0 in range (1,4):
	for i in range (1,4):
		val1 = (i + 1) % 4
		for j in range (1,4):
			val2 = (j + 2) % 4
			for val3 in range (0,3):
				outputFile = "testResults/output" + str(val0) + str(val1) + str(val2) + str(val3) + ".txt"
				command = "mono /mnt/home/benjaylew/tools/Modest/mcsta.exe arbiterTest13state.modest -E \"val0=" + str(val0) + ", val1=" + str(val1) + ", val2=" + str(val2) + ", val3=" + str(val3) + "\" -O " + str(outputFile)
				os.system(command)
