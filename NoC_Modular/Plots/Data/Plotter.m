close all

s1_i1 = fix_shape(readmatrix("Jonah/Journal/s1-i1.csv"));
s1_i5 = fix_shape(readmatrix("Jonah/Journal/s1-i5.csv"));
s1_i8 = fix_shape(readmatrix("Jonah/Journal/s1-i8.csv"));

fig = figure("Units", "inches", "Position",[5,5,3,2.5]);

hold on
plot(s1_i1(:,1), s1_i1(:,2));
plot(s1_i5(:,1), s1_i5(:,2));
plot(s1_i8(:,1), s1_i8(:,2));

xlabel("Clock Cycle");
ylabel("Probability");

grid on

legend(["$\ge 1$", "$\ge 5$", "$\ge 8$"], "Location","southeast", "Interpreter","latex");
xlim([0, 1000]);
hold off

exportgraphics(fig, "2x2_induct_final.png", "resolution", 300);

function data = fix_shape(raw_data)
    data = reshape(raw_data, [2, length(raw_data) / 2])';
end