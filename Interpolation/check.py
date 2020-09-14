import re

probabilityRegex = re.compile(r'(\d\.\d+)\n')

file = open("testResults/output1000.txt")
data = file.read()
dataList = str(data).split("Probability: ")
finalData = []

for item in dataList:
    match = probabilityRegex.search(item)
    if match:
        print(match)
        finalData.append(match.group().split('\n')[0])

print(finalData)
