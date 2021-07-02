import os
import re

files = os.listdir('.')

#print(files)

data_files = []

i_1_arguments = []

for f in files:
    if re.match('data*', f):
        data_files.append(f)

#print(data_files)

for f in data_files:
    current_file = open(f)
    i_1_argument_clause = []
    for line in current_file:
        for word in line.split('('):
            word = word.replace(' ', '')
            word = word.replace('and', '')
            word = word.replace(')', '')
            word = word.replace('not', '!')
            word = word.replace('_1', '')
            word = word.replace('\n', '')
            #print(word) 
            if(re.match('a[0-9][0-9]', word) or re.match('!a[0-9][0-9]', word)):
                word = word.replace('a', '')
                i_1_argument_clause.append(word)
    current_file.close()
    i_1_arguments.append(i_1_argument_clause)

#print(i_1_arguments)

clauses_to_remove = []
for i in range(0, len(i_1_arguments)):
    #print(i_1_arguments[i])
    for j in range(i+1, len(i_1_arguments)):
        if i_1_arguments[i] == i_1_arguments[j]:
            clauses_to_remove.append(j)
clauses_to_remove = list(set(clauses_to_remove))
#print(clauses_to_remove)

offset = 0
for j in clauses_to_remove:
    del i_1_arguments[j - offset]
    offset = offset + 1

for clause in i_1_arguments:
    if not clause:
        i_1_arguments.remove(clause)

#print(i_1_arguments)

open('interpolate_1', 'w').close()
result_file = open("interpolate_1", "a")
for clause in i_1_arguments:
    for element in clause:
        result_file.write(element)
        if not(element == clause[-1]):
            result_file.write(" && ")
    if not(clause == i_1_arguments[-1]):
        result_file.write(" ||\n")
    else:
        result_file.write("\n")
        
result_file.close()

