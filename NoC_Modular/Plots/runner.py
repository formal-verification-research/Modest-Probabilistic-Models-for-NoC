'''
Run this program using:
python3 runner.py <InputFileName> <OutputFileName> <LineToIterate> <StartInt:Interval:StopInt>

LineToIterate must be in the format "const int <name> = "
'''

import sys
import os
from subprocess import Popen, PIPE

if __name__ == "__main__":
    # Parse the arguments
    fin = sys.argv[1]
    fout = sys.argv[2]
    critical = int(sys.argv[3])
    loop = sys.argv[4].split(':')
    for i in range(3):
        loop[i] = int(loop[i])
    
    # Print the arguments
    print('Input: ' + fin)
    print('Output: ' + fout)
    print('Edit line: ' + str(critical))
    print('For:' + str(loop))

    # Make some 0 indexing changes
    critical = critical - 1
    loop[2] = loop[2] + loop[1]
        
    # Load the input file as a list
    with open(fin, 'r') as f:
        lines = f.readlines()
        f.close()
    
    # Edit the critical line and verify continuation
    lines[critical] = lines[critical].split('\n')[0]
    print('Editing: ' + '"' + lines[critical] + '"')
    validate = None
    while validate != 'y':
        validate = input("Continue? (y/n): ")
        if validate == 'n':
            sys.exit("User quit program!");
        if validate != 'y':
            print("Not a valid input!")

    # Clear the old output file
    if os.path.exists(fout):
        os.remove(fout)
    
    for i in range(loop[0], loop[2], loop[1]):
        # Print the current iteration
        print("Clk = " + str(i))

        # Update the clock variable
        lines[critical] = lines[critical].split('=')[0] + "= " + str(i) + ";\n"

        # Save the updated version
        with open('run.modest', 'w') as f:
            for line in lines:
                f.write(line)
            f.close()

        # Run the updated program
        process = Popen(['modest', 'simulate', '--max-run-length', '0', 'run.modest'], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()

        # Get the probability
        output = str(output).split('\\n')
        for out in output:
            if "Estimated probability: " in out:
                index = output.index(out)
        prob = float(output[index].split(' ')[4])
        print("Probability = " + str(prob))

        #print(output)
        with open(fout, 'a') as f:
            f.write(str(i) + ',' + str(prob))
            if i != loop[2] - loop[1]:
                f.write(',')
            f.close()

        # If 100% probability was reached, there is no need to continue
        if prob == 1.0:
            sys.exit("100% probability reached!")

    print()


    
    
