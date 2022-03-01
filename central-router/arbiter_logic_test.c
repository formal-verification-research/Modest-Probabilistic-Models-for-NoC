#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

//#define debug

/* priority - state
0-NESW	6-NEWS	12-NWES 18-WNES
1-ENSW	7-ENWS	13-EWNS	19-WENS
2-NSEW	8-NSWE	14-NWSE	20-WNSE
3-ESNW	9-ESWN	15-EWSN	21-WESN
4-SNEW	10-SNWE	16-SWNE	22-WSNE
5-SENW	11-SEWN	17-SWEN	23-WSEN
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
	loop for each set of us values
		check logic for each of the priority variables
		print to file
	endloop
end test
*/
int run_tests (int us[4][16], FILE* outfile);
int test_0 (int us[4][16], FILE* outfile);
int test_1 (int us[4][16], FILE* outfile);
int test_2 (int us[4][16], FILE* outfile);
int test_3 (int us[4][16], FILE* outfile);
int test_4 (int us[4][16], FILE* outfile);
int test_5 (int us[4][16], FILE* outfile);
int test_6 (int us[4][16], FILE* outfile);
int test_7 (int us[4][16], FILE* outfile);
int test_8 (int us[4][16], FILE* outfile);
int test_9 (int us[4][16], FILE* outfile);
int test_10 (int us[4][16], FILE* outfile);
int test_11 (int us[4][16], FILE* outfile);
int test_12 (int us[4][16], FILE* outfile);
int test_13 (int us[4][16], FILE* outfile);
int test_14 (int us[4][16], FILE* outfile);
int test_15 (int us[4][16], FILE* outfile);
int test_16 (int us[4][16], FILE* outfile);
int test_17 (int us[4][16], FILE* outfile);
int test_18 (int us[4][16], FILE* outfile);
int test_19 (int us[4][16], FILE* outfile);
int test_20 (int us[4][16], FILE* outfile);
int test_21 (int us[4][16], FILE* outfile);
int test_22 (int us[4][16], FILE* outfile);
int test_23 (int us[4][16], FILE* outfile);



int main()
{ //begin test
	

	int us [4][16]; //make array of us values

	FILE* outfile;
	
	if ((outfile = fopen("test_result.txt", "w+")) == NULL){ 					//if attempt to open inputfile is unsuccessful
		printf("Error: attempt to create/modify output file was unsuccessful");		//print error message to console
		exit(EXIT_FAILURE); 														//terminate program
	}

	for(int j = 0; j < 16; j++){

		us[3][j] = (j / 8);
		us[2][j] = (j - (us[3][j] * 8)) / 4 ;
		us[1][j] = (j - (us[3][j] * 8) - (us[2][j] * 4)) / 2 ;
		us[0][j] = j % 2;
#ifdef debug
	printf("us[3,2,1,0][%02d] :\t%d  %d  %d  %d \n", j, us[3][j], us[2][j], us[1][j], us[0][j]);
#endif
	}
	
	run_tests (us, outfile);
	
	fclose(outfile);
	
	return 0;
} //end test
int run_tests (int us[4][16], FILE* outfile)
{
	test_0 (us, outfile);
	test_1 (us, outfile);
	test_2 (us, outfile);
	test_3 (us, outfile);
	test_4 (us, outfile);
	test_5 (us, outfile);
	test_6 (us, outfile);
	test_7 (us, outfile);
	test_8 (us, outfile);
	test_9 (us, outfile);
	test_10 (us, outfile);
	test_11 (us, outfile);
	
	return 0;	
}
int test_0 (int us[4][16], FILE* outfile) //correct
{
	char STATE [5] = "NESW";
	int priority [5]; //make array of priority variables
	int priority_int;
	
	fprintf(outfile, "Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	printf("Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	for (int j = 0, priority_int; j < 16; j++) {
		priority[0] = us[1][j] || !us[0][j];
	
		priority[1] = (!us[3][j]&&!us[1][j]&&!us[0][j]&&us[2][j]) ||
		(us[3][j]&&!us[1][j]&&us[0][j]&&!us[2][j]) ||
		(!us[3][j]&&us[1][j]&&us[0][j]&&us[2][j]) ||
		(us[3][j]&&us[1][j]&&!us[0][j]&&!us[2][j]);	
	
		priority[2] = (us[1][j]&&us[3][j]&&!us[2][j]) ||
		(!us[0][j]&&us[3][j]&&!us[2][j]) ||
		(!us[1][j]&&us[0][j]&&!us[3][j]&&us[2][j]);		
	
		priority[3] = (!us[0][j]&&!us[3][j]) || (us[1][j]&&us[3][j]);

		priority[4] = us[3][j]&&!us[1][j];
		
		priority_int = priority[4]*16 + priority[3]*8 + priority[2]*4 + priority[1]*2 + priority[0];
	
		printf("\t   %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
		fprintf(outfile, "\t     %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
	}
	
	return 0;
}
int test_1 (int us[4][16], FILE* outfile) //correct
{
	char STATE [5] = "ENSW";
	int priority [5]; //make array of priority variables
	int priority_int;
	
	fprintf(outfile, "Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	printf("Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	for (int j = 0, priority_int; j < 16; j++) {
		priority[0] = !us[0][j] && us[1][j];

		priority[1] = (!us[0][j] && !us[1][j] && us[2][j] && !us[3][j]) || (us[0][j] && us[1][j] && us[2][j] && !us[3][j]) ||
			(us[0][j] && !us[1][j] && !us[2][j] && us[3][j]) || (!us[0][j] && us[1][j] && !us[2][j] && us[3][j]);

		priority[2] = (!us[0][j] && us[1][j] && us[2][j] && !us[3][j]) || (!us[1][j] && !us[2][j] && us[3][j]) || (us[0][j] && !us[2][j] && us[3][j]);

		priority[3] = (!us[1][j] && !us[3][j]) || (us[0][j] && us[3][j]);

		priority[4] = !us[0][j] && us[3][j];
		
		priority_int = priority[4]*16 + priority[3]*8 + priority[2]*4 + priority[1]*2 + priority[0];
	
		printf("\t   %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
		fprintf(outfile, "\t     %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
	}
	return 0;
}
int test_2 (int us[4][16], FILE* outfile) //correct
{
	char STATE [5] = "NSEW";
	int priority [5]; //make array of priority variables
	int priority_int;
	
	fprintf(outfile, "Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	printf("Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	for (int j = 0, priority_int; j < 16; j++) {
			priority[0] = !us[0][j] || us[1][j];
	
		priority[1] = (!us[1][j] && !us[2][j] && !us[3][j]) || (!us[0][j] && us[2][j] && !us[3][j]) ||
			(us[1][j] && us[2][j] && us[3][j]) || (!us[0][j] && !us[2][j] && us[3][j]);

		priority[2] = (!us[2][j] && us[3][j]) || (us[0][j] && us[2][j] && !us[3][j]);

		priority[3] = (!us[0][j] && !us[3][j]) || (us[1][j] && us[3][j]);

		priority[4] = !us[1][j] && us[3][j];
		
		priority_int = priority[4]*16 + priority[3]*8 + priority[2]*4 + priority[1]*2 + priority[0];
	
		printf("\t   %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
		fprintf(outfile, "\t     %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
	}
	
	return 0;
}
int test_3 (int us[4][16], FILE* outfile) //correct
{
	char STATE [5] = "ESNW";
	int priority [5]; //make array of priority variables
	int priority_int;
	
	fprintf(outfile, "Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	printf("Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	for (int j = 0, priority_int; j < 16; j++) {
		priority[0] = !us[0][j] && us[1][j];

		priority[1] = (!us[0][j] && !us[2][j] && !us[3][j]) || (!us[1][j] && us[2][j] && !us[3][j]) || (us[0][j] && us[2][j] && us[3][j]) || (!us[1][j] && !us[2][j] && us[3][j]);

		priority[2] = (us[1][j] && us[2][j] && !us[3][j]) || (!us[2][j] && us[3][j]);

		priority[3] = (!us[1][j] && !us[3][j]) || (us[0][j] && us[3][j]);

		priority[4] = !us[0][j] && us[3][j];
		
		priority_int = priority[4]*16 + priority[3]*8 + priority[2]*4 + priority[1]*2 + priority[0];
	
		printf("\t   %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
		fprintf(outfile, "\t     %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
	}
	return 0;
}
int test_4 (int us[4][16], FILE* outfile) //correct
{
	char STATE [5] = "SNEW";
	int priority [5]; //make array of priority variables
	int priority_int;
	
	fprintf(outfile, "Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	printf("Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	for (int j = 0, priority_int; j < 16; j++) {
		priority[0] = !us[0][j] && us[1][j];

		priority[1] = (!us[0][j] && !us[1][j] && !us[2][j]) || (us[0][j] && !us[1][j] && !us[3][j]) || (us[0][j] && us[1][j] && !us[2][j]) || 
			(!us[0][j] && us[1][j] && us[2][j]) || (us[2][j] && us[3][j]);
		
		priority[2] = (!us[2][j] && !us[3][j]) || (us[0][j] && us[3][j]) || (us[1][j] && us[3][j]) || (!us[0][j] && !us[1][j] && us[2][j]);

		priority[3] = (us[0][j] && !us[1][j] && us[3][j]) || (!us[0][j] && us[1][j] && us[3][j]);

		priority[4] = !us[0][j] && !us[1][j] && us[3][j];
		
		priority_int = priority[4]*16 + priority[3]*8 + priority[2]*4 + priority[1]*2 + priority[0];
	
		printf("\t   %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
		fprintf(outfile, "\t     %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
	}
	return 0;
}
int test_5 (int us[4][16], FILE* outfile) //correct
{
	char STATE [5] = "SENW";
	int priority [5]; //make array of priority variables
	int priority_int;
	
	fprintf(outfile, "Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	printf("Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	for (int j = 0, priority_int; j < 16; j++) {
		priority[0] = us[1][j] || (!us[0][j] && !us[2][j]) || (!us[0][j] && !us[3][j]);

		priority[1] = (!us[2][j] && !us[3][j]) || (!us[0][j] && !us[1][j] && us[3][j]) || (us[0][j] && us[1][j] && us[3][j]) || (us[0][j] && !us[1][j] && us[2][j]) || (!us[0][j] && us[1][j] && us[2][j]);

		priority[2] = (!us[2][j] && !us[3][j]) || (us[2][j] && us[3][j]) || (us[0][j] && us[3][j]) || (us[1][j] && us[3][j]) || (!us[0][j] && !us[1][j] && us[2][j]);

		priority[3] = (us[0][j] && !us[1][j] && us[3][j]) || (!us[0][j] && us[1][j] && us[3][j]);

		priority[4] = (!us[0][j] && !us[1][j] && us[3][j]);
		
		priority_int = priority[4]*16 + priority[3]*8 + priority[2]*4 + priority[1]*2 + priority[0];
	
		printf("\t   %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
		fprintf(outfile, "\t     %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
	}
	return 0;
}
int test_6 (int us[4][16], FILE* outfile) //correct
{
	char STATE [5] = "NEWS";
	int priority [5]; //make array of priority variables
	int priority_int;
	
	fprintf(outfile, "Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	printf("Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	for (int j = 0, priority_int; j < 16; j++) {
		priority[0] = !us[0][j] || us[1][j];

		priority[1] = (!us[3][j] && !us[2][j]) || (!us[0][j] && !us[1][j] && us[2][j]) || (us[0][j] && us[1][j] && us[2][j]) || (us[0][j] && !us[1][j] && us[3][j]) || (!us[0][j] && us[1][j] && us[3][j]);

		priority[2] = (!us[2][j] && !us[3][j]) || (!us[0][j] && us[3][j]) || (us[1][j] && us[3][j]) || (us[0][j] && !us[1][j] && us[2][j]);

		priority[3] = (!us[0][j] && !us[3][j]) || (us[1][j] && us[3][j]);

		priority[4] = (!us[1][j] && us[3][j]);
		
		priority_int = priority[4]*16 + priority[3]*8 + priority[2]*4 + priority[1]*2 + priority[0];
	
		printf("\t   %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
		fprintf(outfile, "\t     %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
	}
	return 0;
}
int test_7 (int us[4][16], FILE* outfile) //correct
{
	char STATE [5] = "ENWS";
	int priority [5]; //make array of priority variables
	int priority_int;
	
	fprintf(outfile, "Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	printf("Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	for (int j = 0, priority_int; j < 16; j++) {
		priority[0] = (!us[0][j] && us[1][j]);

		priority[1] = (!us[3][j] && !us[2][j]) || (!us[0][j] && !us[1][j] && us[2][j]) || (us[0][j] && !us[1][j] && us[3][j]) || (!us[0][j] && us[1][j] && us[3][j]) || (us[2][j] && us[3][j]);

		priority[2] = (!us[2][j] && !us[3][j]) || (!us[1][j] && us[3][j]) || (us[0][j] && us[3][j]) || (us[1][j] && us[2][j]);

		priority[3] = (!us[1][j] && !us[3][j]) || (us[0][j] && us[3][j]);

		priority[4] = (!us[0][j] && us[3][j]);
	
		priority_int = priority[4]*16 + priority[3]*8 + priority[2]*4 + priority[1]*2 + priority[0];
	
		printf("\t   %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
		fprintf(outfile, "\t     %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
	}
	return 0;
}
int test_8 (int us[4][16], FILE* outfile) //correct
{
	char STATE [5] = "NSWE";
	int priority [5]; //make array of priority variables
	int priority_int;
	
	fprintf(outfile, "Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	printf("Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	for (int j = 0, priority_int; j < 16; j++) {
		priority[0] = (!us[0][j] || us[1][j]) || (us[1][j] && us[2][j] && !us[3][j]);

		priority[1] = (!us[0][j] && !us[1][j] && !us[2][j] && us[3][j]) || (us[0][j] && us[1][j] && !us[2][j] && us[3][j]) || (us[0][j] && !us[1][j] && us[2][j] && !us[3][j]) || (!us[0][j] && us[1][j] && us[2][j] && !us[3][j]);

		priority[2] = (!us[1][j] && !us[2][j] && us[3][j]) || (!us[0][j] && !us[2][j] && us[3][j]) || (us[0][j] && us[1][j] && us[2][j] && !us[3][j]);

		priority[3] = (us[0][j] && !us[1][j] && !us[3][j]) || (!us[0][j] && us[1][j] && !us[3][j]);

		priority[4] = us[3][j] || (!us[0][j] && !us[1][j]);
		
		priority_int = priority[4]*16 + priority[3]*8 + priority[2]*4 + priority[1]*2 + priority[0];
	
		printf("\t   %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
		fprintf(outfile, "\t     %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
	}
	return 0;
}
int test_9 (int us[4][16], FILE* outfile) //correct
{
	char STATE [5] = "ESWN";
	int priority [5]; //make array of priority variables
	int priority_int;
	
	fprintf(outfile, "Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	printf("Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	for (int j = 0, priority_int; j < 16; j++) {
		priority[0] = (!us[0][j] && us[1][j]);

		priority[1] = (!us[0][j] && !us[1][j] && !us[2][j] && us[3][j]) || (us[0][j] && us[1][j] && !us[2][j] && us[3][j]) || (us[0][j] && !us[1][j] && us[2][j] && !us[3][j]) || (!us[0][j] && us[1][j] && !us[3][j]);

		priority[2] = (!us[1][j] && !us[2][j] && us[3][j]) || (!us[0][j] && !us[2][j] && us[3][j]) || (us[0][j] && us[1][j] && us[2][j] && !us[3][j]);

		priority[3] = (us[0][j] && !us[1][j] && !us[3][j]) || (!us[0][j] && us[1][j] && us[2][j] && !us[3][j]);

		priority[4] = (!us[0][j] && !us[1][j]) || us[3][j];
		
		priority_int = priority[4]*16 + priority[3]*8 + priority[2]*4 + priority[1]*2 + priority[0];
	
		printf("\t   %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
		fprintf(outfile, "\t     %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
	}
	return 0;
}
int test_10 (int us[4][16], FILE* outfile) //correct
{
	char STATE [5] = "SNWE";
	int priority [5]; //make array of priority variables
	int priority_int;
	
	fprintf(outfile, "Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	printf("Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	for (int j = 0, priority_int; j < 16; j++) {
		priority[0] = !us[0][j] && us[1][j];

		priority[1] = (us[1][j] && !us[2][j] && !us[3][j]) || (!us[0][j] && us[2][j] && !us[3][j]) || (!us[1][j] && us[2][j] && us[3][j]) || (!us[0][j] && !us[2][j] && us[3][j]);

		priority[2] = (!us[2][j] && !us[3][j]) || (us[2][j] && us[3][j]) || (us[0][j] && us[3][j]);

		priority[3] = (!us[1][j] && !us[3][j]) || (us[0][j] && us[3][j]);

		priority[4] = !us[0][j] && us[3][j];
		
		priority_int = priority[4]*16 + priority[3]*8 + priority[2]*4 + priority[1]*2 + priority[0];
	
		printf("\t   %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
		fprintf(outfile, "\t     %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
	}
	return 0;
}
int test_11 (int us[4][16], FILE* outfile) //correct
{
	char STATE [5] = "SEWN";
	int priority [5]; //make array of priority variables
	int priority_int;
	
	fprintf(outfile, "Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	printf("Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	for (int j = 0, priority_int; j < 16; j++) {
		priority[0] = !us[0][j] || us[1][j];

		priority[1] = (us[0][j] && !us[2][j] && !us[3][j]) || (!us[1][j] && us[2][j] && !us[3][j]) || (!us[0][j] && us[2][j] && us[3][j]) || (!us[1][j] && !us[2][j] && us[3][j]);

		priority[2] = (!us[2][j] && !us[3][j]) || (us[2][j] && us[3][j]) || (us[1][j] && us[3][j]);

		priority[3] = (!us[0][j] && !us[3][j]) || (us[1][j] && us[3][j]);

		priority[4] = !us[1][j] && us[3][j];
		
		priority_int = priority[4]*16 + priority[3]*8 + priority[2]*4 + priority[1]*2 + priority[0];
	
		printf("\t   %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
		fprintf(outfile, "\t     %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
	}
	return 0;
}
int test_12 (int us[4][16], FILE* outfile)
{
	char STATE [5] = "ENSW";
	int priority [5]; //make array of priority variables
	int priority_int;
	
	fprintf(outfile, "Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	printf("Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	for (int j = 0, priority_int; j < 16; j++) {
		priority[0] = !us[0][j] && us[1][j];

		priority[1] = (!us[0][j] && !us[1][j] && us[2][j] && !us[3][j]) || (us[0][j] && us[1][j] && us[2][j] && !us[3][j]) ||
			(us[0][j] && !us[1][j] && !us[2][j] && us[3][j]) || (!us[0][j] && us[1][j] && !us[2][j] && us[3][j]);

		priority[2] = (!us[0][j] && us[1][j] && us[2][j] && !us[3][j]) || (!us[1][j] && !us[2][j] && us[3][j]) || (us[0][j] && !us[2][j] && us[3][j]);

		priority[3] = (!us[1][j] && !us[3][j]) || (us[0][j] && us[3][j]);

		priority[4] = !us[0][j] && us[3][j];
		
		priority_int = priority[4]*16 + priority[3]*8 + priority[2]*4 + priority[1]*2 + priority[0];
	
		printf("\t   %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
		fprintf(outfile, "\t     %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
	}
	return 0;
}
int test_13 (int us[4][16], FILE* outfile)
{
	char STATE [5] = "ENSW";
	int priority [5]; //make array of priority variables
	int priority_int;
	
	fprintf(outfile, "Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	printf("Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	for (int j = 0, priority_int; j < 16; j++) {
		priority[0] = !us[0][j] && us[1][j];

		priority[1] = (!us[0][j] && !us[1][j] && us[2][j] && !us[3][j]) || (us[0][j] && us[1][j] && us[2][j] && !us[3][j]) ||
			(us[0][j] && !us[1][j] && !us[2][j] && us[3][j]) || (!us[0][j] && us[1][j] && !us[2][j] && us[3][j]);

		priority[2] = (!us[0][j] && us[1][j] && us[2][j] && !us[3][j]) || (!us[1][j] && !us[2][j] && us[3][j]) || (us[0][j] && !us[2][j] && us[3][j]);

		priority[3] = (!us[1][j] && !us[3][j]) || (us[0][j] && us[3][j]);

		priority[4] = !us[0][j] && us[3][j];
		
		priority_int = priority[4]*16 + priority[3]*8 + priority[2]*4 + priority[1]*2 + priority[0];
	
		printf("\t   %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
		fprintf(outfile, "\t     %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
	}
	return 0;
}
int test_14 (int us[4][16], FILE* outfile)
{
	char STATE [5] = "ENSW";
	int priority [5]; //make array of priority variables
	int priority_int;
	
	fprintf(outfile, "Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	printf("Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	for (int j = 0, priority_int; j < 16; j++) {
		priority[0] = !us[0][j] && us[1][j];

		priority[1] = (!us[0][j] && !us[1][j] && us[2][j] && !us[3][j]) || (us[0][j] && us[1][j] && us[2][j] && !us[3][j]) ||
			(us[0][j] && !us[1][j] && !us[2][j] && us[3][j]) || (!us[0][j] && us[1][j] && !us[2][j] && us[3][j]);

		priority[2] = (!us[0][j] && us[1][j] && us[2][j] && !us[3][j]) || (!us[1][j] && !us[2][j] && us[3][j]) || (us[0][j] && !us[2][j] && us[3][j]);

		priority[3] = (!us[1][j] && !us[3][j]) || (us[0][j] && us[3][j]);

		priority[4] = !us[0][j] && us[3][j];
		
		priority_int = priority[4]*16 + priority[3]*8 + priority[2]*4 + priority[1]*2 + priority[0];
	
		printf("\t   %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
		fprintf(outfile, "\t     %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
	}
	return 0;
}
int test_15 (int us[4][16], FILE* outfile)
{
	char STATE [5] = "ENSW";
	int priority [5]; //make array of priority variables
	int priority_int;
	
	fprintf(outfile, "Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	printf("Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	for (int j = 0, priority_int; j < 16; j++) {
		priority[0] = !us[0][j] && us[1][j];

		priority[1] = (!us[0][j] && !us[1][j] && us[2][j] && !us[3][j]) || (us[0][j] && us[1][j] && us[2][j] && !us[3][j]) ||
			(us[0][j] && !us[1][j] && !us[2][j] && us[3][j]) || (!us[0][j] && us[1][j] && !us[2][j] && us[3][j]);

		priority[2] = (!us[0][j] && us[1][j] && us[2][j] && !us[3][j]) || (!us[1][j] && !us[2][j] && us[3][j]) || (us[0][j] && !us[2][j] && us[3][j]);

		priority[3] = (!us[1][j] && !us[3][j]) || (us[0][j] && us[3][j]);

		priority[4] = !us[0][j] && us[3][j];
		
		priority_int = priority[4]*16 + priority[3]*8 + priority[2]*4 + priority[1]*2 + priority[0];
	
		printf("\t   %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
		fprintf(outfile, "\t     %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
	}
	return 0;
}
int test_16 (int us[4][16], FILE* outfile)
{
	char STATE [5] = "ENSW";
	int priority [5]; //make array of priority variables
	
	fprintf(outfile, "Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	printf("Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	for (int j = 0, priority_int; j < 16; j++) {
		priority[0] = !us[0][j] && us[1][j];

		priority[1] = (!us[0][j] && !us[1][j] && us[2][j] && !us[3][j]) || (us[0][j] && us[1][j] && us[2][j] && !us[3][j]) ||
			(us[0][j] && !us[1][j] && !us[2][j] && us[3][j]) || (!us[0][j] && us[1][j] && !us[2][j] && us[3][j]);

		priority[2] = (!us[0][j] && us[1][j] && us[2][j] && !us[3][j]) || (!us[1][j] && !us[2][j] && us[3][j]) || (us[0][j] && !us[2][j] && us[3][j]);

		priority[3] = (!us[1][j] && !us[3][j]) || (us[0][j] && us[3][j]);

		priority[4] = !us[0][j] && us[3][j];
		
		priority_int = priority[4]*16 + priority[3]*8 + priority[2]*4 + priority[1]*2 + priority[0];
	
		printf("\t   %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
		fprintf(outfile, "\t     %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
	}
	return 0;
}
int test_17 (int us[4][16], FILE* outfile)
{
	char STATE [5] = "ENSW";
	int priority [5]; //make array of priority variables
	int priority_int;
	
	fprintf(outfile, "Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	printf("Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	for (int j = 0, priority_int; j < 16; j++) {
		priority[0] = !us[0][j] && us[1][j];

		priority[1] = (!us[0][j] && !us[1][j] && us[2][j] && !us[3][j]) || (us[0][j] && us[1][j] && us[2][j] && !us[3][j]) ||
			(us[0][j] && !us[1][j] && !us[2][j] && us[3][j]) || (!us[0][j] && us[1][j] && !us[2][j] && us[3][j]);

		priority[2] = (!us[0][j] && us[1][j] && us[2][j] && !us[3][j]) || (!us[1][j] && !us[2][j] && us[3][j]) || (us[0][j] && !us[2][j] && us[3][j]);

		priority[3] = (!us[1][j] && !us[3][j]) || (us[0][j] && us[3][j]);

		priority[4] = !us[0][j] && us[3][j];
		
		priority_int = priority[4]*16 + priority[3]*8 + priority[2]*4 + priority[1]*2 + priority[0];
	
		printf("\t   %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
		fprintf(outfile, "\t     %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
	}
	return 0;
}
int test_18 (int us[4][16], FILE* outfile)
{
	char STATE [5] = "ENSW";
	int priority [5]; //make array of priority variables
	int priority_int;
	
	fprintf(outfile, "Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	printf("Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	for (int j = 0, priority_int; j < 16; j++) {
		priority[0] = !us[0][j] && us[1][j];

		priority[1] = (!us[0][j] && !us[1][j] && us[2][j] && !us[3][j]) || (us[0][j] && us[1][j] && us[2][j] && !us[3][j]) ||
			(us[0][j] && !us[1][j] && !us[2][j] && us[3][j]) || (!us[0][j] && us[1][j] && !us[2][j] && us[3][j]);

		priority[2] = (!us[0][j] && us[1][j] && us[2][j] && !us[3][j]) || (!us[1][j] && !us[2][j] && us[3][j]) || (us[0][j] && !us[2][j] && us[3][j]);

		priority[3] = (!us[1][j] && !us[3][j]) || (us[0][j] && us[3][j]);

		priority[4] = !us[0][j] && us[3][j];
		
		priority_int = priority[4]*16 + priority[3]*8 + priority[2]*4 + priority[1]*2 + priority[0];
	
		printf("\t   %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
		fprintf(outfile, "\t     %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
	}
	return 0;
}
int test_19 (int us[4][16], FILE* outfile)
{
	char STATE [5] = "ENSW";
	int priority [5]; //make array of priority variables
	int priority_int;
	
	fprintf(outfile, "Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	printf("Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	for (int j = 0, priority_int; j < 16; j++) {
		priority[0] = !us[0][j] && us[1][j];

		priority[1] = (!us[0][j] && !us[1][j] && us[2][j] && !us[3][j]) || (us[0][j] && us[1][j] && us[2][j] && !us[3][j]) ||
			(us[0][j] && !us[1][j] && !us[2][j] && us[3][j]) || (!us[0][j] && us[1][j] && !us[2][j] && us[3][j]);

		priority[2] = (!us[0][j] && us[1][j] && us[2][j] && !us[3][j]) || (!us[1][j] && !us[2][j] && us[3][j]) || (us[0][j] && !us[2][j] && us[3][j]);

		priority[3] = (!us[1][j] && !us[3][j]) || (us[0][j] && us[3][j]);

		priority[4] = !us[0][j] && us[3][j];
		
		priority_int = priority[4]*16 + priority[3]*8 + priority[2]*4 + priority[1]*2 + priority[0];
	
		printf("\t   %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
		fprintf(outfile, "\t     %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
	}
	return 0;
}
int test_20 (int us[4][16], FILE* outfile)
{
	char STATE [5] = "ENSW";
	int priority [5]; //make array of priority variables
	int priority_int;
	
	fprintf(outfile, "Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	printf("Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	for (int j = 0, priority_int; j < 16; j++) {
		priority[0] = !us[0][j] && us[1][j];

		priority[1] = (!us[0][j] && !us[1][j] && us[2][j] && !us[3][j]) || (us[0][j] && us[1][j] && us[2][j] && !us[3][j]) ||
			(us[0][j] && !us[1][j] && !us[2][j] && us[3][j]) || (!us[0][j] && us[1][j] && !us[2][j] && us[3][j]);

		priority[2] = (!us[0][j] && us[1][j] && us[2][j] && !us[3][j]) || (!us[1][j] && !us[2][j] && us[3][j]) || (us[0][j] && !us[2][j] && us[3][j]);

		priority[3] = (!us[1][j] && !us[3][j]) || (us[0][j] && us[3][j]);

		priority[4] = !us[0][j] && us[3][j];
		
		priority_int = priority[4]*16 + priority[3]*8 + priority[2]*4 + priority[1]*2 + priority[0];
	
		printf("\t   %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
		fprintf(outfile, "\t     %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
	}
	return 0;
}
int test_21 (int us[4][16], FILE* outfile)
{
	char STATE [5] = "ENSW";
	int priority [5]; //make array of priority variables
	int priority_int;
	
	fprintf(outfile, "Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	printf("Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	for (int j = 0, priority_int; j < 16; j++) {
		priority[0] = !us[0][j] && us[1][j];

		priority[1] = (!us[0][j] && !us[1][j] && us[2][j] && !us[3][j]) || (us[0][j] && us[1][j] && us[2][j] && !us[3][j]) ||
			(us[0][j] && !us[1][j] && !us[2][j] && us[3][j]) || (!us[0][j] && us[1][j] && !us[2][j] && us[3][j]);

		priority[2] = (!us[0][j] && us[1][j] && us[2][j] && !us[3][j]) || (!us[1][j] && !us[2][j] && us[3][j]) || (us[0][j] && !us[2][j] && us[3][j]);

		priority[3] = (!us[1][j] && !us[3][j]) || (us[0][j] && us[3][j]);

		priority[4] = !us[0][j] && us[3][j];
		
		priority_int = priority[4]*16 + priority[3]*8 + priority[2]*4 + priority[1]*2 + priority[0];
	
		printf("\t   %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
		fprintf(outfile, "\t     %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
	}
	return 0;
}
int test_22 (int us[4][16], FILE* outfile)
{
	char STATE [5] = "ENSW";
	int priority [5]; //make array of priority variables
	int priority_int;
	
	fprintf(outfile, "Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	printf("Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	for (int j = 0, priority_int; j < 16; j++) {
		priority[0] = !us[0][j] && us[1][j];

		priority[1] = (!us[0][j] && !us[1][j] && us[2][j] && !us[3][j]) || (us[0][j] && us[1][j] && us[2][j] && !us[3][j]) ||
			(us[0][j] && !us[1][j] && !us[2][j] && us[3][j]) || (!us[0][j] && us[1][j] && !us[2][j] && us[3][j]);

		priority[2] = (!us[0][j] && us[1][j] && us[2][j] && !us[3][j]) || (!us[1][j] && !us[2][j] && us[3][j]) || (us[0][j] && !us[2][j] && us[3][j]);

		priority[3] = (!us[1][j] && !us[3][j]) || (us[0][j] && us[3][j]);

		priority[4] = !us[0][j] && us[3][j];
		
		priority_int = priority[4]*16 + priority[3]*8 + priority[2]*4 + priority[1]*2 + priority[0];
	
		printf("\t   %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
		fprintf(outfile, "\t     %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
	}
	return 0;
}
int test_23 (int us[4][16], FILE* outfile)
{
	char STATE [5] = "ENSW";
	int priority [5]; //make array of priority variables
	int priority_int;
	
	fprintf(outfile, "Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	printf("Priority update table for condition %s\nunsigned [3,2,1,0] || Priority (next state)\n________________________________________\n", STATE);
	for (int j = 0, priority_int; j < 16; j++) {
		priority[0] = !us[0][j] && us[1][j];

		priority[1] = (!us[0][j] && !us[1][j] && us[2][j] && !us[3][j]) || (us[0][j] && us[1][j] && us[2][j] && !us[3][j]) ||
			(us[0][j] && !us[1][j] && !us[2][j] && us[3][j]) || (!us[0][j] && us[1][j] && !us[2][j] && us[3][j]);

		priority[2] = (!us[0][j] && us[1][j] && us[2][j] && !us[3][j]) || (!us[1][j] && !us[2][j] && us[3][j]) || (us[0][j] && !us[2][j] && us[3][j]);

		priority[3] = (!us[1][j] && !us[3][j]) || (us[0][j] && us[3][j]);

		priority[4] = !us[0][j] && us[3][j];
		
		priority_int = priority[4]*16 + priority[3]*8 + priority[2]*4 + priority[1]*2 + priority[0];
	
		printf("\t   %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
		fprintf(outfile, "\t     %d %d %d %d || %d %d %d %d %d -- %d\n", us[3][j], us[2][j], us[1][j], us[0][j], priority[4], priority[3], priority[2], priority[1], priority[0], priority_int);
	}
	return 0;
}
