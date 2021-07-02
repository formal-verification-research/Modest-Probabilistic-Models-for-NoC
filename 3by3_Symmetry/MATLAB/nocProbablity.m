local = [
    0, 2/8, 6/8, 0;
    0, 2/8, 3/8, 3/8;
    0, 2/8, 0, 6/8;
    1/8, 1/8, 6/8, 0;
    1/8, 1/8, 3/8, 3/8;
    1/8, 1/8, 0, 6/8;
    2/8, 0, 6/8, 0;
    2/8, 0, 3/8, 3/8;
    2/8, 0, 0, 6/8;
    ];

DisplaceMessage = [
    0, 1, 2;    
    3, 4, 5;
    6, 7, 8;
    ];

a_local = [
    0, 2/8, 6/8, 0;
    0, 2/8, 3/8, 3/8;
    0, 2/8, 0, 6/8;
    1/8, 1/8, 6/8, 0;
    ];
b_local = [
    1/8, 1/8, 0, 6/8;
    2/8, 0, 6/8, 0;
    2/8, 0, 3/8, 3/8;
    2/8, 0, 0, 6/8;
    ];
inverseMatrix = [
    0, 0, 0, 1;
    0, 0, 1, 0;
    0, 1, 0, 0;
    1, 0, 0, 0;
    ];

mapFunction = [
    0, 1, 0, 0;
    1, 0, 0, 0;
    0, 0, 0, 1;
    0, 0, 1, 0;
    ];

disp(DisplaceMessage);

disp(">>>Starting Maping for the local direction<<<");

disp("Key:    +y, -y, +x, -x");
temp = [0,1,2,3,4,5,6,7,8;];
disp(temp');

disp("Probablistic Matrix for the local channel: ");
disp(local);

Message = "This is maping nocs 0 - 3 to nocs 5- 8";
x = inverseMatrix * a_local * mapFunction;
y = inverseMatrix * b_local * mapFunction;
disp(Message);
disp(x);
disp("Equivalency check");
disp (x == b_local);

Message = "This is maping nocs 5 - 8 to nocs 0 - 3";
disp(Message);
disp(y);
disp(a_local);
disp (y == a_local);


Noc_0 =[0, 2/8, 6/8, 0;];
Noc_1 =[0, 2/8, 3/8, 3/8;];
Noc_2 =[0, 2/8, 0, 6/8;];
Noc_3 =[1/8, 1/8, 6/8, 0;];
u_local = [1/8, 1/8, 3/8, 3/8;];
Noc_5 =[1/8, 1/8, 0, 6/8;];
Noc_6 =[2/8, 0, 6/8, 0;];
Noc_7 =[2/8, 0, 3/8, 3/8;];
Noc_8 =[2/8, 0, 0, 6/8;];

mapFunction_Noc0 = [
    0, 0, 0, 0;
    0, 2, 0, 0;
    0, 0, 2, 0;
    0, 0, 0, 0;
    ];
mapFunction_Noc1 = [
    0, 0, 0, 0;
    0, 2, 0, 0;
    0, 0, 1, 0;
    0, 0, 0, 1;
    ];
mapFunction_Noc2 = [
    0, 0, 0, 0;
    0, 2, 0, 0;
    0, 0, 0, 0;
    0, 0, 0, 2;
    ];
mapFunction_Noc3 = [
    1, 0, 0, 0;
    0, 1, 0, 0;
    0, 0, 2, 0;
    0, 0, 0, 0;
    ];
mapFunction_Noc5 = [
    1, 0, 0, 0;
    0, 1, 0, 0;
    0, 0, 0, 0;
    0, 0, 0, 2;
    ];
mapFunction_Noc6 = [
    2, 0, 0, 0;
    0, 0, 0, 0;
    0, 0, 2, 0;
    0, 0, 0, 0;
    ];
mapFunction_Noc7 = [
    2, 0, 0, 0;
    0, 0, 0, 0;
    0, 0, 1, 0;
    0, 0, 0, 1;
    ];
mapFunction_Noc8 = [
    2, 0, 0, 0;
    0, 0, 0, 0;
    0, 0, 0, 0;
    0, 0, 0, 2;
    ];

disp("Maping the center Noc to Noc 0: ");
tempNoc0 = u_local * mapFunction_Noc0;
disp(Noc_0)
disp("Equivalency check");
disp(Noc_0 == tempNoc0)

disp("Maping the center Noc to Noc 1: ");
tempNoc1 = u_local * mapFunction_Noc1;
disp(Noc_1)
disp("Equivalency check");
disp(Noc_1 == tempNoc1)

disp("Maping the center Noc to Noc 2: ");
tempNoc2 = u_local * mapFunction_Noc2;
disp(Noc_2)
disp("Equivalency check");
disp(Noc_2 == tempNoc2)

disp("Maping the center Noc to Noc 3: ");
tempNoc3 = u_local * mapFunction_Noc3;
disp(Noc_3)
disp("Equivalency check");
disp(Noc_3 == tempNoc3)

disp("Maping the center Noc to Noc 5: ");
tempNoc5 = u_local * mapFunction_Noc5;
disp(Noc_5)
disp("Equivalency check");
disp(Noc_5 == tempNoc5)

disp("Maping the center Noc to Noc 6: ");
tempNoc6 = u_local * mapFunction_Noc6;
disp(Noc_6)
disp("Equivalency check");
disp(Noc_6 == tempNoc6)

disp("Maping the center Noc to Noc 7: ");
tempNoc7 = u_local * mapFunction_Noc7;
disp(Noc_7)
disp("Equivalency check");
disp(Noc_7 == tempNoc7)

disp("Maping the center Noc to Noc 8: ");
tempNoc8 = u_local * mapFunction_Noc8;
disp(Noc_8)
disp("Equivalency check");
disp(Noc_8 == tempNoc8);

disp(">>>Starting Maping for the y directions<<<");
disp("+y direction: ");
disp("Key:    +y, -x, +y, local");
temp = [0,1,2,3,4,5,6,7,8;];
disp(temp');

yPossitiveDricetion = [
    0, 0, 0, 1;
    0, 0, 0, 1;
    0, 0, 0, 1;
    0, 0, 1/2, 1/2;
    0, 0, 1/2, 1/2;
    0, 0, 1/2, 1/2;
    0, 0, 2/3, 1/3;
    0, 0, 2/3, 1/3;
    0, 0, 2/3, 1/3;    
    ];

disp("Probablistic Matrix for the +y direction channel: ");
disp(yPossitiveDricetion);



disp("-y direction: ");
disp("Key:    +x, -x, -y, local");
temp = [0,1,2,3,4,5,6,7,8;];
disp(temp');

yNegDricetion = [
    0, 0, 2/3, 1/3;
    0, 0, 2/3, 1/3;
    0, 0, 2/3, 1/3;
    0, 0, 1/2, 1/2;
    0, 0, 1/2, 1/2;
    0, 0, 1/2, 1/2;
    0, 0, 0, 1;
    0, 0, 0, 1;
    0, 0, 0, 1;
    ];

a_yPossitive = [
    0, 0, 0, 1;
    0, 0, 0, 1;
    0, 0, 0, 1;
    0, 0, 1/2, 1/2;
    ];

b_yPossitive = [
    0, 0, 1/2, 1/2;
    0, 0, 2/3, 1/3;
    0, 0, 2/3, 1/3;
    0, 0, 2/3, 1/3;
    ];

disp("Probablistic Matrix for the -y Negative channel: ");
disp(yNegDricetion);

a_yNeg = [
    0, 0, 2/3, 1/3;
    0, 0, 2/3, 1/3;
    0, 0, 2/3, 1/3;
    0, 0, 1/2, 1/2;
    ];
b_yNeg = [
    0, 0, 1/2, 1/2;
    0, 0, 0, 1;
    0, 0, 0, 1;
    0, 0, 0, 1;
    ];


disp("Mapping y possitive to y negative:");
disp("a y possitive mapps to b y negative:");
tempAY = inverseMatrix  * b_yNeg;
disp(tempAY);
disp("Equivalency check");
disp(tempAY == a_yPossitive);

disp("b y possitive mapps to a y negative:");
tempBY = inverseMatrix  * a_yNeg;
disp(tempBY);
disp("Equivalency check");
disp(tempBY == b_yPossitive);

disp("Starting Mapping of center noc to all other nocs");
yCenterNoc = [0, 0, 1/2, 1/2;];
yTopNoc = [0, 0, 2/3, 1/3;];
disp("Mapping to the 0,0,2/3,1/3: ");

MapFunctionYTop = [
    0, 0, 0, 0;
    0, 0, 0, 0;
    0, 0, 4/3, 0;
    0, 0, 0, 2/3;
    ];

tempNoc = yCenterNoc * MapFunctionYTop;

yBootomNoc = [0, 0, 0, 1;];
disp("Displaying mapping Function: ");
disp(tempNoc);
disp("Equivalency check");
disp(tempNoc == yTopNoc);

disp("Mapping to the 0,0,0,1: ");

MapFunctionYBottom = [
    0, 0, 0, 0;
    0, 0, 0, 0;
    0, 0, 0, 0;
    0, 0, 0, 2;
    ];

tempNoc = yCenterNoc * MapFunctionYBottom;

disp("Displaying mapping Function: ");
disp(tempNoc);
disp("Equivalency check");
disp(tempNoc == yBootomNoc);
disp("Therefore all the Nocs in the y direction can be mapped to from the center Noc.");

xPosDicTop = [
    0, 0, 2/3, 1/3;
    3/6, 0, 2/6, 1/6;
    0, 0, 0, 0;
    0, 1/3, 1/3, 1/3;
    ];
    
    xPosDicBottom = [
    0, 0, 0, 0;
    0, 2/3, 0, 1/3;
    3/6, 2/6, 0, 1/6;
    0, 0, 0, 0;                                                                                                                  
    ];                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                                                                     
XNegDicTop = [
    0,0,0,0;
    3/6,0,2/6,1/6;
    0,0,2/3,1/3;
    0,0,0,0;
    ];
XNegDicBottom = [
    0,1/3,1/3,1/3;
    0,0,0,0;
    3/6,2/6,0,1/6;
    0,2/3,0,1/3;
    ];

disp("Mapping the x Neg direction top to the x pos direction bottom");
mappingFuncXDirection = [
    1,0,0,0;
    0,0,1,0;
    0,1,0,0;
    0,0,0,1;
    ];
temp = inverseMatrix * xPosDicBottom * mappingFuncXDirection;
disp(temp);
disp("Equivalency check");
disp(temp == XNegDicTop);

disp("Mapping the x Neg direction bottom to the x pos direction Top");
temp = inverseMatrix * xPosDicTop * mappingFuncXDirection;
disp(temp);
disp("Equivalency check");
disp(temp == XNegDicBottom);

disp("Starting Mapping of center noc to all other nocs from the x poss direction");

cenNocXDir = [3/6, 1/6, 1/6, 1/6;];

xPosNoc0 = [0, 0, 2/3, 1/3;];
xPosNoc1 = [3/6, 0, 2/6, 1/6;];
xPosNoc2 = [0, 0, 0, 0;];
xPosNoc3 = [0, 1/3, 1/3, 1/3;];
xPosNoc5 = [0, 0, 0, 0;];
xPosNoc6 = [0, 2/3, 0, 1/3;];
xPosNoc7 = [3/6, 2/6, 0, 1/6;];
xPosNoc8 = [0, 0, 0, 0;];

xPosMap0 = [
    0, 0, 0, 0;
    0, 0, 0, 0;
    0, 0, 4, 0;
    0, 0, 0, 2;
    ];
xPosMap1 = [
    1, 0, 0, 0;
    0, 0, 0, 0;
    0, 0, 2, 0;
    0, 0, 0, 1;
    ];
xPosMap2 = [
    0, 0, 0, 0;
    0, 0, 0, 0;
    0, 0, 0, 0;
    0, 0, 0, 0;
    ];
xPosMap3 = [
    0, 0, 0, 0;
    0, 2, 0, 0;
    0, 0, 2, 0;
    0, 0, 0, 2;
    ];
xPosMap5 = [
    0, 0, 0, 0;
    0, 0, 0, 0;
    0, 0, 0, 0;
    0, 0, 0, 0;
    ];
xPosMap6 = [
    0, 0, 0, 0;
    0, 4, 0, 0;
    0, 0, 0, 0;
    0, 0, 0, 2;
    ];
xPosMap7 = [
    1, 0, 0, 0;
    0, 2, 0, 0;
    0, 0, 0, 0;
    0, 0, 0, 1;
    ];
xPosMap8 = [
    0, 0, 0, 0;
    0, 0, 0, 0;
    0, 0, 0, 0;
    0, 0, 0, 0;
    ];
tempXtop = cenNocXDir * xPosMap0;
disp("Mapping center to noc 0 in the x pos direction");
disp(tempXtop);
disp("Equivalency check");
disp(tempXtop == xPosNoc0);

tempXtop = cenNocXDir * xPosMap1;
disp("Mapping center to noc 1 in the x pos direction");
disp(tempXtop);
disp("Equivalency check");
disp(tempXtop == xPosNoc1);

tempXtop = cenNocXDir * xPosMap2;
disp("Mapping center to noc 2 in the x pos direction");
disp(tempXtop);
disp("Equivalency check");
disp(tempXtop == xPosNoc2);

tempXtop = cenNocXDir * xPosMap3;
disp("Mapping center to noc 3 in the x pos direction");
disp(tempXtop);
disp("Equivalency check");
disp(tempXtop == xPosNoc3);

tempXtop = cenNocXDir * xPosMap5;
disp("Mapping center to noc 5 in the x pos direction");
disp(tempXtop);
disp("Equivalency check");
disp(tempXtop == xPosNoc5);

tempXtop = cenNocXDir * xPosMap6;
disp("Mapping center to noc 6 in the x pos direction");
disp(tempXtop);
disp("Equivalency check");
disp(tempXtop == xPosNoc6);

tempXtop = cenNocXDir * xPosMap7;
disp("Mapping center to noc 7 in the x pos direction");
disp(tempXtop);
disp("Equivalency check");
disp(tempXtop == xPosNoc7);

tempXtop = cenNocXDir * xPosMap8;
disp("Mapping center to noc 8 in the x pos direction");
disp(tempXtop);
disp("Equivalency check");
disp(tempXtop == xPosNoc8);
   
disp("Starting Mapping of center noc to all other nocs from the x neg direction");
xNegNoc0 = [0,0,0,0;];
xNegNoc1 = [3/6,0,2/6,1/6;];
xNegNoc2 = [0,0,2/3,1/3;];
xNegNoc3 = [0,0,0,0;];
xNegNoc5 = [0,1/3,1/3,1/3;];
xNegNoc6 = [0,0,0,0;];
xNegNoc7 = [3/6,2/6,0,1/6;];
xNegNoc8 = [0,2/3,0,1/3;];

xNegMap0 = [
    0, 0, 0, 0;
    0, 0, 0, 0;
    0, 0, 0, 0;
    0, 0, 0, 0;
    ];
xNegMap1 = [
    1, 0, 0, 0;
    0, 0, 0, 0;
    0, 0, 2, 0;
    0, 0, 0, 1;
    ];
xNegMap2 = [
    0, 0, 0, 0;
    0, 0, 0, 0;
    0, 0, 4, 0;
    0, 0, 0, 2;
    ];
xNegMap3 = [
    0, 0, 0, 0;
    0, 0, 0, 0;
    0, 0, 0, 0;
    0, 0, 0, 0;
    ];
xNegMap5 = [
    0, 0, 0, 0;
    0, 2, 0, 0;
    0, 0, 2, 0;
    0, 0, 0, 2;
    ];
xNegMap6 = [
    0, 0, 0, 0;
    0, 0, 0, 0;
    0, 0, 0, 0;
    0, 0, 0, 0;
    ];
xNegMap7 = [
    1, 0, 0, 0;
    0, 2, 0, 0;
    0, 0, 0, 0;
    0, 0, 0, 1;
    ];
xNegMap8 = [
    0, 0, 0, 0;
    0, 0, 0, 0;
    0, 0, 0, 0;
    0, 0, 0, 0;
    ];

tempXbottom = cenNocXDir * xNegMap0;
disp("Mapping center to noc 0 in the x neg direction");
disp(tempXtop);
disp("Equivalency check");
disp(tempXtop == xNegNoc0);

tempXtop = cenNocXDir * xNegMap1;
disp("Mapping center to noc 1 in the x neg direction");
disp(tempXtop);
disp("Equivalency check");
disp(tempXtop == xNegNoc1);

tempXtop = cenNocXDir * xNegMap2;
disp("Mapping center to noc 2 in the x Neg direction");
disp(tempXtop);
disp("Equivalency check");
disp(tempXtop == xNegNoc2);

tempXtop = cenNocXDir * xNegMap3;
disp("Mapping center to noc 3 in the x Neg direction");
disp(tempXtop);
disp("Equivalency check");
disp(tempXtop == xNegNoc3);

tempXtop = cenNocXDir * xNegMap5;
disp("Mapping center to noc 5 in the x Neg direction");
disp(tempXtop);
disp("Equivalency check");
disp(tempXtop == xNegNoc5);

tempXtop = cenNocXDir * xNegMap6;
disp("Mapping center to noc 6 in the x Neg direction");
disp(tempXtop);
disp("Equivalency check");
disp(tempXtop == xNegNoc6);

tempXtop = cenNocXDir * xNegMap7;
disp("Mapping center to noc 7 in the x Neg direction");
disp(tempXtop);
disp("Equivalency check");
disp(tempXtop == xNegNoc7);

tempXtop = cenNocXDir * xNegMap8;
disp("Mapping center to noc 8 in the x Neg direction");
disp(tempXtop);
disp("Equivalency check");
disp(tempXtop == xNegNoc8);