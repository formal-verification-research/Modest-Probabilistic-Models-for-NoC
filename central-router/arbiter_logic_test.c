#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

//#define debug
#define STATE "NESW"

/* priority - state
1-NESW	7-NEWS	13-NWES 19-WNES
2-ENSW	8-ENWS	14-EWNS	20-WENS
3-NSEW	9-NSWE	15-NWSE	21-WNSE
4-ESNW	10-ESWN	16-EWSN	22-WESN
5-SNEW	11-SNWE	17-SWNE	23-WSNE
6-SENW	12-SEWN	18-SWEN	24-WSEN
*/


/*
router channel positions
	0
3	-	1
	2

begin test
	open file to print to 
	make array of unserviced variable values
	make array of priority variables
	loop for each set of unserviced values
		check logic for each of the priority variables
		print to file
	endloop
end test
*/


int main()
{ //begin test
	

	bool unserviced [4][16]; //make array of unserviced values

	FILE* outfile;
	
	if ((outfile = fopen("test_result.txt", "w+")) == NULL){ 					//if attempt to open inputfile is unsuccessful
		printf("Error: attempt to create/modify output file was unsuccessful");		//print error message to console
		exit(EXIT_FAILURE); 														//terminate program
	}

	int j;	
	for(j = 0; j < 16; j++){

		unserviced[3][j] = (j / 8);
		unserviced[2][j] = (j - (unserviced[3][j] * 8)) / 4 ;
		unserviced[1][j] = (j - (unserviced[3][j] * 8) - (unserviced[2][j] * 4)) / 2 ;
		unserviced[0][j] = j % 2;
#ifdef debug
	printf("unserviced[3,2,1,0][%02d] :\t%d  %d  %d  %d \n", j, unserviced[3][j], unserviced[2][j], unserviced[1][j], unserviced[0][j]);
#endif
	}
	
	int priority [4] = {0,0,0,0}; //make array of priority variables
	
	fprintf(outfile, "Priority update table for condition %s\nUnserviced [3,2,1,0] | Priority (next state)\n________________________________________\n", STATE);
	for (j = 0; j < 16; j++) {
		/*
	//logic for priority[0]
		priority [0] = Logic0;
	//logic for priority[1]
		priority [1] = Logic1;	
	//logic for priority[0]
		priority [2] = Logic2;		
	//logic for priority[0]
		priority [3] = Logic3;
		*/
		fprintf(outfile, "\t     %d %d %d %d | %d %d %d %d \n", unserviced[3][j], unserviced[2][j], unserviced[1][j], unserviced[0][j], priority[3], priority[2], priority[1], priority[0]);
	}

	return 0;
} //end test
