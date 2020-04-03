import subprocess
M = 3 # on cycles
N = 7 # off cycles

output = ["Burst3Output0.txt", "Burst3Output1.txt", "Burst3Output2.txt", "Burst3Output3.txt", "Burst3Output4.txt", "Burst3Output5.txt", "Burst3Output6.txt", "Burst3Output7.txt"]

for x in range (0,7):
	subprocess.run(["/Users/Riley/Desktop/Modest/modest", "mcsta", "BurstyMode.modest", "-E", "DUR = 10000, Mvar = %s, Nvar = %s, Startvar = %s" % (str(M), str(N), str(x)), "--unsafe", "-O", str(output[x])])