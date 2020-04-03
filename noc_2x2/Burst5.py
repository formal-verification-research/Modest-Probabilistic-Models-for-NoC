import subprocess
M = 5 # on cycles
N = 10 # off cycles

output = ["Burst5Output0.txt", "Burst5Output1.txt", "Burst5Output2.txt", "Burst5Output3.txt", "Burst5Output4.txt", "Burst5Output5.txt", "Burst5Output6.txt", "Burst5Output7.txt", "Burst5Output8.txt", "Burst5Output9.txt", "Burst5Output10.txt"]

for x in range (0,10):
	subprocess.run(["/Users/Riley/Desktop/Modest/modest", "mcsta", "BurstyMode.modest", "-E", "DUR = 10000, Mvar = %s, Nvar = %s, Startvar = %s" % (str(M), str(N), str(x)), "--unsafe", "-O", str(output[x])])