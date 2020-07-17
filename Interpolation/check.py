import os
import re

probabilityRegex = re.compile(r'(\d\.\d+|0)\n')

probabilityTable = {
        "0" : [(1/9), (4/27), (16/81), (20/81), (1/27), (1/9), (1/27), (1/81), (2/81), (2/81), (1/81), (1/81), (2/81)],
        "1" : [(1/9), (4/27), (8/27), (4/27), (1/27), (1/9), 0, (1/27), (1/27), 0, (1/27), 0, (1/27)],
        "2" : [(1/9), (4/27), (2/9), (2/9), (1/27), (1/9), (1/27), 0, (1/27), 0, 0, (1/27), (1/27)],
        "3" : [(1/9), (4/27), (2/27), (10/27), (1/27), (1/9), (2/27), 0, 0, (2/27), 0, 0, 0],
        "4" : [0, 0, (4/9), 0, 0, (1/3), 0, 0, (1/9), 0, 0, 0, (1/9)],
        "5" : [0, 0, 0, (4/9), 0, (1/3), (1/9), 0, 0, (1/9), 0, 0, 0],
        "6" : [(1/9), (2/9), (2/9), 0, (1/9), (1/9), 0, (1/9), (1/9), 0, 0, 0, 0],
        "7" : [(2/9), (1/9), (1/9), (4/9), 0, 0, (1/9), 0, 0, 0, 0, 0, 0],
        "8" : [(2/9), (1/9), (1/9), (4/9), 0, 0, (1/9), 0, 0, 0, 0, 0, 0],
        "9" : [(1/9), (1/9), (1/3), (2/9), 0, (1/9), 0, 0, 0, 0, 0, 0, (1/9)],
        "10" : [(1/9), (1/9), (1/3), (2/9), 0, (1/9), 0, 0, 0, 0, (1/9), 0, 0],
        "11" : [(1/9), (1/3), (1/9), (2/9), (1/9), 0, 0, 0, 0, 0, 0, (1/9), 0],
        "12" : [(1/9), (1/3), (1/9), (2/9), (1/9), 0, 0, 0, 0, (1/9), 0, 0, 0]
        }

stateTable = {
	"1000" : "4",
	"1030" : "1",
	"1210" : "2",
	"1300" : "1",
	"1330" : "3",
	"2010" : "1",
	"2200" : "8",
	"2230" : "2",
	"2310" : "0",
	"3000" : "4",
	"3030" : "9",
        "3210" : "0",
	"3300" : "9",
	"3330" : "5",
	"1001" : "7",
	"1031" : "2",
	"1211" : "5",
	"1301" : "2",
	"1331" : "10",
	"2011" : "2",
	"2201" : "2",
	"2231" : "2",
	"2311" : "2",
	"3001" : "1",
	"3031" : "3",
	"3211" : "2",
	"3301" : "3",
	"3331" : "5",
	"1002" : "1",
	"1032" : "0",
	"1212" : "12",
	"1302" : "0",
	"1332" : "3",
	"2012" : "3",
	"2202" : "5",
	"2232" : "5",
	"2312" : "3",
	"3002" : "1",
	"3032" : "3",
	"3212" : "3",
	"3302" : "3",
	"3332" : "5",
	"1010" : "8",
	"1200" : "1",
	"1230" : "0",
	"1310" : "2",
	"2000" : "4",
	"2030" : "1",
	"2210" : "2",
	"2300" : "1",
	"2330" : "3",
	"3010" : "1",
	"3200" : "1",
	"3230" : "0",
	"3310" : "3",
	"1011" : "5",
	"1201" : "2",
	"1231" : "2",
	"1311" : "5",
	"2001" : "1",
	"2031" : "0",
	"2211" : "12",
	"2301" : "0",
	"2331" : "3",
	"3011" : "2",
	"3201" : "0",
	"3231" : "3",
	"3311" : "6",
	"1012" : "2",
	"1202" : "3",
	"1232" : "3",
	"1312" : "2",
	"2002" : "11",
	"2032" : "3",
	"2212" : "5",
	"2302" : "3",
	"2332" : "6",
	"3012" : "0",
	"3202" : "3",
	"3232" : "6",
	"3312" : "3"
         }

for val0 in range (1,4):
	for i in range (1,4):
		val1 = (i + 1) % 4
		for j in range (1,4):
			val2 = (j + 2) % 4
			for val3 in range (0,3):
                            outputFile = "dataFiles/output" + str(val0) + str(val1) + str(val2) + str(val3)
                            command = "mono /home/benjaylew/Modest/mcsta.exe arbiterTest13state.modest -E \"val0=" + str(val0) + ", val1=" + str(val1) + ", val2=" + str(val2) + ", val3=" + str(val3) + "\" > " + str(outputFile)
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
                            probabilityList = probabilityList[1:13]
                            
                            state81 = str(val0) + str(val1) + str(val2) + str(val3)
                            state = stateTable.get(state81)
                            abstractProbability = probabilityTable.get(state)

                            probabilityFile = open("dataFiles/probabilities" + str(val0) + str(val1) + str(val2) + str(val3), "a")
                            probabilityFile.write(state81)
                            probabilityFile.write("\n")
                            for i in range(0, len(probabilityList)):
                                probabilityFile.write("Abstract probability: ")
                                probabilityFile.write(str(abstractProbability[i]))
                                probabilityFile.write("\t Concrete probability: ")
                                probabilityFile.write(probabilityList[i])
                                probabilityFile.write("\t Difference:")
                                probabilityFile.write(str(abstractProbability[i] - float(probabilityList[i])))
                                probabilityFile.write("\n")
                            
                            
                            #print(probabilityList)
                            #probabilityFile = open("dataFiles/probabilities" + str(val0) + str(val1) + str(val2) + str(val3), "a")
                            #for item in data:
                            #    probabilityFile.write(item)
                            #    probabilityFile.write("\n")
                            #probabilityFile.close()
