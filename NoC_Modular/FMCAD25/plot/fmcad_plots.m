results_directories = dir("results/");

close all

mkdir("plot")

for i = 1:size(results_directories, 1)
    if results_directories(i).isdir && ...
        (results_directories(i).name ~= "." && results_directories(i).name ~= "..")
        plot_noise(results_directories(i))
    end
end

%% Functions
function plot_noise(directory)
    % get the directory name
    noc_size = directory.name;

    % get all the csv files
    files = dir(fullfile(directory.folder, noc_size));

    % plot inductive noise first
    fig = figure("Units", "inches", "Position",[5,5,3.3,2.7]);
    hold on
    leg = strings(0);
    thresholds = [];
    for j = 1:size(files,1)
        if files(j).name == ".." || files(j).name == "."
            continue
        end

        is_inductive = contains(files(j).name, "inductive", ...
            "IgnoreCase",true);
        [~, ~, ext] = fileparts(files(j).name);
        is_csv = ext == ".csv";

        if is_inductive && is_csv 
            threshold = get_threshold(files(j).name);
            thresholds = [thresholds, threshold];
            label = sprintf("$$\\ge %d$$", threshold);
            leg = [leg, label];

            data = readtable(fullfile(files(j).folder, files(j).name), "VariableNamingRule","modify");
            if ~exist("line", "var")
                line = plot(data{:,"ClockCycle"}, data{:,"Probability"}, "LineWidth",1.0);
            else
                line = [line, plot(data{:,"ClockCycle"}, data{:,"Probability"}, "LineWidth",1.0)];
            end
        end
    end
    hold off
    grid on

    [~, i] = sort(thresholds);
    if exist("line", "var")
        set(gca,'Children',fliplr(line(i)));
    end
    leg = leg(i);

    legend(leg, "Interpreter","latex", "Location","southeast");
    xlabel("Clock cycles");
    ylabel("Probability");
    xlim tight
    ylim tight
    png_filename = sprintf("%s_inductive.png", noc_size);
    exportgraphics(fig, fullfile("plot", png_filename), "Resolution",600);

    % Save small version of plot
    set(fig, "Position", [5,5,3.3*(30/44),2.7*(30/44)])
    xlabel("Clock cycles", "FontSize", 8);
    ylabel("Probability", "FontSize", 8);
    xlim tight
    ylim tight
    png_filename = sprintf("%s_inductive_small.png", noc_size);
    exportgraphics(fig, fullfile("plot", png_filename), "Resolution",600);

    close all

    % plot resistive noise second
    fig = figure("Units", "inches", "Position",[5,5,3.3,2.7]);
    hold on
    leg = strings(0);
    thresholds = [];
    clear line
    for j = 1:size(files,1)
        is_inductive = contains(files(j).name, "resistive", ...
            "IgnoreCase",true);
        [~, ~, ext] = fileparts(files(j).name);
        is_csv = ext == ".csv";

        if is_inductive && is_csv 
            threshold = get_threshold(files(j).name);
            thresholds = [thresholds, threshold];
            label = sprintf("$$\\ge %d$$", threshold);
            leg = [leg, label];

            data = readtable(fullfile(files(j).folder, files(j).name), "VariableNamingRule","modify");
            if ~exist("line", "var")
                line = plot(data{:,"ClockCycle"}, data{:,"Probability"}, "LineWidth",1.0);
            else
                line = [line, plot(data{:,"ClockCycle"}, data{:,"Probability"}, "LineWidth",1.0)];
            end
        end
    end
    hold off
    grid on

    [~, i] = sort(thresholds);
    if exist("line", "var")
        set(gca,'Children',fliplr(line(i)));
    end
    leg = leg(i);

    legend(leg, "Interpreter","latex", "Location","southeast");
    xlabel("Clock cycles");
    ylabel("Probability");
    xlim tight
    ylim tight
    png_filename = sprintf("%s_resistive.png", noc_size);
    exportgraphics(fig, fullfile("plot", png_filename), "Resolution",600);
    
    % Save small version of plot
    set(fig, "Position", [5,5,3.3*(30/44),2.7*(30/44)])
    xlabel("Clock cycles", "FontSize", 8);
    ylabel("Probability", "FontSize", 8);
    xlim tight
    ylim tight
    png_filename = sprintf("%s_resistive_small.png", noc_size);
    exportgraphics(fig, fullfile("plot", png_filename), "Resolution",600);

    close all
end

function t = get_threshold(filename)
    expression = 'threshold_(\d+)_';
    [tokens, matches] = regexp(filename, expression, 'tokens', 'match');
    
    if size(matches, 1) ~= 0
        t = str2double(tokens{1}{1});
    else
        error("Didn't find threshold");
    end
end