import pandas as pd
import matplotlib.pyplot as plt

# Read CSV file
def read_csv_file(file_path):
    df = pd.read_csv(file_path)
    return df

# Plot resistive noise
def plot_resistive_noise(df):
    plt.figure(figsize=(10, 6))
    for threshold in df['RESISTIVE_NOISE_THRESH'].unique():
        print(threshold)
        df_threshold = df[df['RESISTIVE_NOISE_THRESH'] == threshold]
        plt.plot(df_threshold['CLK_UPPER'], df_threshold['resistiveNoiseProbability'], label=f'Resistive Threshold {threshold}')
    plt.title('Resistive Noise Probability')
    plt.xlabel('Clock Cycles')
    plt.ylabel('Probability')
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot inductive noise
def plot_inductive_noise(df):
    plt.figure(figsize=(10, 6))
    for threshold in df['INDUCTIVE_NOISE_THRESH'].unique():
        print(threshold)
        df_threshold = df[df['INDUCTIVE_NOISE_THRESH'] == threshold]
        plt.plot(df_threshold['CLK_UPPER'], df_threshold['inductiveNoiseProbability'], label=f'Inductive Threshold {threshold}')

    plt.title('Inductive Noise Probability')
    plt.xlabel('Clock Cycles')
    plt.ylabel('Probability')
    plt.legend()
    plt.grid(True)
    plt.show()

# Main function
def main():
    file_path_1 = "../NoC_Modular/Plots/Data/Nick/noise_2x2_1.txt"
    file_path_5 = "../NoC_Modular/Plots/Data/Nick/noise_2x2_5.txt"
    file_path_10 = "../NoC_Modular/Plots/Data/Nick/noise_2x2_10.txt"
    file_path_20 = "../NoC_Modular/Plots/Data/Nick/noise_2x2_20.txt"

    df1 = read_csv_file(file_path_1)
    df5 = read_csv_file(file_path_5)
    df10 = read_csv_file(file_path_10)
    df20 = read_csv_file(file_path_20)

    df = pd.concat([df1, df5, df10, df20], axis=0)

    plot_resistive_noise(df)
    plot_inductive_noise(df)

if __name__ == "__main__":
    main()
