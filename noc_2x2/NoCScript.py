import subprocess
M = 3 # on cycles
N = 7 # off cycles
Startvar = 0

output = ["Output0.txt", "Output1.txt", "Output2.txt", "Output3.txt", "Output4.txt", "Output5.txt", "Output6.txt", "Output7.txt", "Output8.txt", "Output9.txt", "Output10.txt",
            "Output11.txt", "Output12.txt", "Output13.txt", "Output14.txt", "Output15.txt", "Output20.txt", "Output25.txt", "Output30.txt"]

for x in range (0,15):
	subprocess.run(["~/ModestFiles/Modest/modest", "mcsta", "FinalBooleanQueue.modest", "-E", "DUR = %s, Mvar = %s, Nvar = %s, Startvar = %s" % (str(x), str(M), str(N), str(Startvar)), "--unsafe", "-O", str(output[x])])

subprocess.run(["~/ModestFiles/Modest/modest", "mcsta", "FinalBooleanQueue.modest", "-E", "DUR = 20, Mvar = %s, Nvar = %s, Startvar = %s" % (str(M), str(N), str(Startvar)), "--unsafe", "-O", str(output[16])])
subprocess.run(["~/ModestFiles/Modest/modest", "mcsta", "FinalBooleanQueue.modest", "-E", "DUR = 25, Mvar = %s, Nvar = %s, Startvar = %s" % (str(M), str(N), str(Startvar)), "--unsafe", "-O", str(output[17])])
subprocess.run(["~/ModestFiles/Modest/modest", "mcsta", "FinalBooleanQueue.modest", "-E", "DUR = 30, Mvar = %s, Nvar = %s, Startvar = %s" % (str(M), str(N), str(Startvar)), "--unsafe", "-O", str(output[18])])