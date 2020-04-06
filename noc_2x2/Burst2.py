import subprocess
M = 2 # on cycles
N = 8 # off cycles

output = ["Burst2Output0.txt", "Burst2Output1.txt", "Burst2Output2.txt", "Burst2Output3.txt", "Burst2Output4.txt", "Burst2Output5.txt", "Burst2Output6.txt", "Burst2Output7.txt", "Burst2Output8.txt"]

for x in range (0,8):
	subprocess.run(["~/ModestFiles/Modest/modest", "mcsta", "BurstyMode.modest", "-E", "DUR = 100, Mvar = %s, Nvar = %s, Startvar = %s" % (str(M), str(N), str(x)), "--unsafe", "-O", str(output[x])])

