import subprocess
import pathlib
path = pathlib.Path(__file__).parent.absolute()

for val0 in range (1,3):
	for i in range (1,3):
		val1 = (i + 1) % 4
		for j in range (1,3):
			val2 = (j + 2) % 4
			for val3 int range (0,2):
				outputFile = "output" + str(val0) + str(val1) + str(val2) + str(val3)
				subprocess.run([path, "mcsta", "arbiterTest13state.modest", "-E", "val0 = %s, val1 = %s, val2 = %s, val3 = %s" % (str(val0), str(val1), str(val2), str(val3)), "--unsafe", "-O", str(outputFile)])

