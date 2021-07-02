import os
import re

probabilityRegex = re.compile(r'(\d\.\d+|0)\n')

probabilityTable = {
        "0" : [(1/9), (16/81), (20/81), (4/27), (1/9), (1/27), (1/27), (1/27), (1/27), (1/27)],
        "1" : [(1/9), (2/9), (2/9), (4/27), (1/9), (1/27), (1/27), (1/27), (2/27), 0],
        "2" : [(1/9), (2/27), (10/27), (4/27), (1/9), (1/27), (2/27), 0, 0, (2/27)],
        "3" : [(1/9), (8/27), (4/27), (4/27), (1/9), (1/27), 0, (2/27), (1/27), (1/27)],
        "4" : [0, 0, (4/9), 0,  (1/3), 0, (1/9), 0, 0, (1/9)],
        "5" : [0, (4/9), 0, 0, (1/3), 0, 0, (1/9), (1/9), 0],
        "6" : [(1/9), (2/9), 0, (2/9), (1/9), (1/9), 0, (2/9), 0, 0],
        "7" : [(2/9), (1/9), (4/9), (1/9), 0, 0, (1/9), 0, 0, 0],
        "8" : [(1/9), (2/9), (2/9), (2/9), (1/18), (1/18), 0, 0, (1/27), (2/27)],
        "9" : [(1/9), (1/3), (2/9), (1/9), (1/9), 0, 0, 0, (2/27), (1/27)]
        }

stateTable = {
	"1000" : "5",
	"1030" : "3",
	"1210" : "1",
	"1300" : "3",
	"1330" : "2",
	"2010" : "3",
	"2200" : "7",
	"2230" : "1",
	"2310" : "0",
	"3000" : "5",
	"3030" : "9",
        "3210" : "0",
	"3300" : "9",
	"3330" : "4",
	"1001" : "7",
	"1031" : "1",
	"1211" : "4",
	"1301" : "1",
	"1331" : "9",
	"2011" : "1",
	"2201" : "1",
	"2231" : "1",
	"2311" : "1",
	"3001" : "3",
	"3031" : "2",
	"3211" : "1",
	"3301" : "2",
	"3331" : "4",
	"1002" : "3",
	"1032" : "0",
	"1212" : "8",
	"1302" : "0",
	"1332" : "2",
	"2012" : "2",
	"2202" : "4",
	"2232" : "4",
	"2312" : "2",
	"3002" : "3",
	"3032" : "2",
	"3212" : "2",
	"3302" : "2",
	"3332" : "4",
	"1010" : "7",
	"1200" : "3",
	"1230" : "0",
	"1310" : "1",
	"2000" : "5",
	"2030" : "3",
	"2210" : "1",
	"2300" : "3",
	"2330" : "2",
	"3010" : "3",
	"3200" : "3",
	"3230" : "2",
	"3310" : "2",
	"1011" : "4",
	"1201" : "1",
	"1231" : "1",
	"1311" : "4",
	"2001" : "3",
	"2031" : "0",
	"2211" : "8",
	"2301" : "0",
	"2331" : "2",
	"3011" : "1",
	"3201" : "0",
	"3231" : "2",
	"3311" : "6",
	"1012" : "1",
	"1202" : "2",
	"1232" : "2",
	"1312" : "1",
	"2002" : "8",
	"2032" : "2",
	"2212" : "4",
	"2302" : "2",
	"2332" : "6",
	"3012" : "0",
	"3202" : "2",
	"3232" : "6",
	"3312" : "2"
         }

for val0 in range (1,4):
	for i in range (1,4):
		val1 = (i + 1) % 4
		for j in range (1,4):
			val2 = (j + 2) % 4
			for val3 in range (0,3):
                            outputFile = "dataFiles/output" + str(val0) + str(val1) + str(val2) + str(val3)
                            command = "mono /mnt/home/benjaylew/tools/Modest/mcsta.exe ./step3CounterExamples.modest -E \"val0=" + str(val0) + ", val1=" + str(val1) + ", val2=" + str(val2) + ", val3=" + str(val3) + "\" > " + str(outputFile)
                           # print("Running: " + command)
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


