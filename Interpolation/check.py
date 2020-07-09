import os

for val0 in range (1,3):
	for i in range (1,3):
		val1 = (i + 1) % 4
		for j in range (1,3):
			val2 = (j + 2) % 4
			for val3 int range (0,2):
				outputFile = "output" + str(val0) + str(val1) + str(val2) + str(val3)
				command = "mcsta arbiterTest13state.modest -E val0=" + str(val0) + " val1=" + str(val1) + " val2=" + str(val2) + " val3=" + str(val3) + " -O " + str(outputFile)
				os.system(command)