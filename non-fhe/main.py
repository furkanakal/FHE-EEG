import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch

# Function to identify brainwave type based on frequency
def classify_brainwave(frequency):
    if 0.5 <= frequency < 4:
        return "Delta"
    elif 4 <= frequency < 8:
        return "Theta"
    elif 8 <= frequency < 13:
        return "Alpha"
    elif 13 <= frequency < 30:
        return "Beta"
    elif 30 <= frequency < 100:
        return "Gamma"
    else:
        return "Unknown"

# Load the EEG data from the CSV file
file_path = "multi_channel_eeg_data.csv"  # Replace with your file path
eeg_data = pd.read_csv(file_path)

# Filter data for the first 2 seconds
eeg_data_2s = eeg_data[eeg_data["Time (s)"] <= 2]

# Sampling frequency (assumed based on data, modify if different)
fs = 250  # Hz

# Analyze and print frequency and brainwave type for each channel
print("Channel Analysis (First 2 Seconds):")
for column in eeg_data_2s.columns[1:]:  # Exclude the "Time (s)" column
    signal = eeg_data_2s[column]
    
    # Compute Power Spectral Density (PSD)
    frequencies, psd = welch(signal, fs, nperseg=fs)
    
    # Find dominant frequency
    dominant_frequency = frequencies[np.argmax(psd)]
    brainwave_type = classify_brainwave(dominant_frequency)
    
    print(f"Channel: {column}")
    print(f"  Dominant Frequency: {dominant_frequency:.2f} Hz")
    print(f"  Brainwave Type: {brainwave_type}")
    print()

# Plot each channel
plt.figure(figsize=(12, 8))
for column in eeg_data_2s.columns[1:]:  # Exclude the "Time (s)" column
    plt.plot(eeg_data_2s["Time (s)"], eeg_data_2s[column], label=column)

# Add plot details
plt.title("Multi-Channel EEG Data (First 2 Seconds)", fontsize=16)
plt.xlabel("Time (s)", fontsize=14)
plt.ylabel("Amplitude (µV)", fontsize=14)
plt.legend(title="Channels", loc="upper right")
plt.grid(True)
plt.tight_layout()

# Save the figure
plt.savefig("multi_channel_eeg_plot.png", dpi=300)

# Show the plot
plt.show()
