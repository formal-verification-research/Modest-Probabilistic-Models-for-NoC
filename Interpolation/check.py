import os
import re

probabilityTable = {
        "0" : [(1/9), (4/27), (16/81), (20/81), (1/27), (1/9), (1/27), (1/81), (2/81), (2/81), (1/81), (1/81), (2/81)],
        "1" : [(1/9), (4/27), (8/27), (4/27), (1/27), (1/9), 0, (1/27), (1/27), 0, (1/27), 0, (1/27)],
        "2" : [(1/9), (4/27), (16/81), (20/81), (1/27), (1/9), (1/27), (1/81), (2/81), (2/81), (1/81), (1/81), (2/81)],
        "3" : [(1/9), (4/27), (16/81), (20/81), (1/27), (1/9), (1/27), (1/81), (2/81), (2/81), (1/81), (1/81), (2/81)],
        "4" : [(1/9), (4/27), (16/81), (20/81), (1/27), (1/9), (1/27), (1/81), (2/81), (2/81), (1/81), (1/81), (2/81)],
        "5" : [(1/9), (4/27), (16/81), (20/81), (1/27), (1/9), (1/27), (1/81), (2/81), (2/81), (1/81), (1/81), (2/81)],
        "6" : [(1/9), (4/27), (16/81), (20/81), (1/27), (1/9), (1/27), (1/81), (2/81), (2/81), (1/81), (1/81), (2/81)],
        "7" : [(1/9), (4/27), (16/81), (20/81), (1/27), (1/9), (1/27), (1/81), (2/81), (2/81), (1/81), (1/81), (2/81)],
        "8" : [(1/9), (4/27), (16/81), (20/81), (1/27), (1/9), (1/27), (1/81), (2/81), (2/81), (1/81), (1/81), (2/81)],
        "9" : [(1/9), (4/27), (16/81), (20/81), (1/27), (1/9), (1/27), (1/81), (2/81), (2/81), (1/81), (1/81), (2/81)],
        "10" : [(1/9), (4/27), (16/81), (20/81), (1/27), (1/9), (1/27), (1/81), (2/81), (2/81), (1/81), (1/81), (2/81)],
        "11" : [(1/9), (4/27), (16/81), (20/81), (1/27), (1/9), (1/27), (1/81), (2/81), (2/81), (1/81), (1/81), (2/81)],
        "12" : [(1/9), (4/27), (16/81), (20/81), (1/27), (1/9), (1/27), (1/81), (2/81), (2/81), (1/81), (1/81), (2/81)]
        }

for val0 in range (1,4):
	for i in range (1,4):
		val1 = (i + 1) % 4
		for j in range (1,4):
			val2 = (j + 2) % 4
			for val3 in range (0,3):
				outputFile = "dataFiles/output" + str(val0) + str(val1) + str(val2) + str(val3)
				command = "mono /home/benjaylew/Modest/mcsta.exe arbiterTest13state.modest -E \"val0=" + str(val0) + ", val1=" + str(val1) + ", val2=" + str(val2) + ", val3=" + str(val3) + "\" -O " + str(outputFile)
				os.system(command)

