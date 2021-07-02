import os
import re

probabilityRegex = re.compile(r'(\d\.\d+|0)\n')

probabilityTable = {
        "0" : [(1/9), (16/27), (4/27), (1/27), (1/27), (2/27)],
        "1" : [(1/9), (16/27), (4/27), (7/162), (5/162), (2/27)],
        "2" : [0, (4/9), (1/3), (1/12), (1/36), (1/9)],
        "3" : [(1/9), (2/3), (1/9), (1/9), 0, 0],
        "4" : [(1/9), (2/3), 0, 0, 0, (1/9)],
        "5" : [(1/6), (4/9), (2/9), 0, (2/9), 0]
        }

stateTable = {
	"1000" : "2",
	"1030" : "1",
	"1210" : "1",
	"1300" : "1",
	"1330" : "1",
	"2010" : "1",
	"2200" : "4",
	"2230" : "1",
	"2310" : "0",
	"3000" : "2",
	"3030" : "5",
        "3210" : "0",
	"3300" : "5",
	"3330" : "2",
	"1001" : "4",
	"1031" : "1",
	"1211" : "2",
	"1301" : "1",
	"1331" : "5",
	"2011" : "1",
	"2201" : "1",
	"2231" : "1",
	"2311" : "1",
	"3001" : "1",
	"3031" : "1",
	"3211" : "1",
	"3301" : "1",
	"3331" : "2",
	"1002" : "1",
	"1032" : "0",
	"1212" : "5",
	"1302" : "0",
	"1332" : "1",
	"2012" : "1",
	"2202" : "2",
	"2232" : "2",
	"2312" : "1",
	"3002" : "1",
	"3032" : "1",
	"3212" : "1",
	"3302" : "1",
	"3332" : "2",
	"1010" : "4",
	"1200" : "1",
	"1230" : "0",
	"1310" : "1",
	"2000" : "2",
	"2030" : "1",
	"2210" : "1",
	"2300" : "1",
	"2330" : "1",
	"3010" : "1",
	"3200" : "1",
	"3230" : "1",
	"3310" : "1",
	"1011" : "2",
	"1201" : "1",
	"1231" : "1",
	"1311" : "2",
	"2001" : "1",
	"2031" : "0",
	"2211" : "5",
	"2301" : "0",
	"2331" : "1",
	"3011" : "1",
	"3201" : "0",
	"3231" : "1",
	"3311" : "3",
	"1012" : "1",
	"1202" : "1",
	"1232" : "1",
	"1312" : "1",
	"2002" : "5",
	"2032" : "1",
	"2212" : "2",
	"2302" : "1",
	"2332" : "3",
	"3012" : "0",
	"3202" : "1",
	"3232" : "3",
	"3312" : "1"
         }

for val0 in range (1,4):
	for i in range (1,4):
		val1 = (i + 1) % 4
		for j in range (1,4):
			val2 = (j + 2) % 4
			for val3 in range (0,3):
                            outputFile = "dataFiles/output" + str(val0) + str(val1) + str(val2) + str(val3)
                            command = "mono /mnt/home/benjaylew/tools/Modest/mcsta.exe ./step1CounterExamples.modest -E \"val0=" + str(val0) + ", val1=" + str(val1) + ", val2=" + str(val2) + ", val3=" + str(val3) + "\" > " + str(outputFile)
                            #print("Running: " + command)
                            os.system(command)
                            dataFile = open(outputFile)
                            probabilityList = []
                            data = dataFile.read()
                            data = data.split("Probability:")
                            for item in data:
                                match = probabilityRegex.search(item)
                                if match:
                                    probabilityList.append(match.group().split('\n')[0])
                            dataFile.close()
                            probabilityList = probabilityList[1:14]
                            
                            state81 = str(val0) + str(val1) + str(val2) + str(val3)
                            state = stateTable.get(state81)
                            abstractProbability = probabilityTable.get(state)

                            probabilityFile = open("dataFiles/probabilities" + str(val0) + str(val1) + str(val2) + str(val3), "a")
                            probabilityFile.write(state81)
                            probabilityFile.write("\n")
                            for i in range(0, len(probabilityList)):
                                probabilityFile.write("Abstract probability: ")
                                probabilityFile.write(str(abstractProbability[i]))
                                #print("Abstract probability: " + str(abstractProbability[i]))
                                probabilityFile.write("\t Concrete probability: ")
                                probabilityFile.write(probabilityList[i])
                                #print("Concrete probability: " + str(probabilityList[i]))
                                probabilityFile.write("\t Difference: ")
                                
                                difference = abstractProbability[i] - float(probabilityList[i])
                                probabilityFile.write(str(difference))
                                #print("Difference: " + str(difference))
                                probabilityFile.write("\n")

                                if (difference > 0.00000001 or difference < -0.00000001):
                                    print(state81, end="")
                                    print("->", end="")
                                    print(i, end="")
                                    print("\tAbstract probability: ", end= "")
                                    print(str(abstractProbability[i]), end="")
                                    print("\tConcrete probability: ", end="")
                                    print(probabilityList[i], end="")
                                    print("\tDifference: ", end="")
                                    print(difference)


