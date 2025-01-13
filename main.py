from concrete import fhe

# Function to scale frequency to 16-bit integer
def scale_frequency(value):
    """
    Scale frequency values into the 16-bit range.

    Parameters:
        value (float): The frequency value in Hz.

    Returns:
        int: Scaled 16-bit integer frequency value.
    """
    # Assume a frequency range of 0-100 Hz for scaling
    return int((value * 65535) // 100)

# Define the homomorphic function to classify the dominant frequency
def classify_brainwave_homomorphic(psd_values, frequencies):
    """
    Homomorphic function to classify the brainwave type.

    Parameters:
        psd_values (list of int): Power Spectral Density (scaled 16-bit integers).
        frequencies (list of int): Corresponding frequency values (scaled 16-bit integers).

    Returns:
        int: Classified brainwave type (0=Delta, 1=Theta, 2=Alpha, 3=Beta, 4=Gamma).
    """
    # Find the maximum PSD value and its corresponding frequency
    max_psd = 0
    weighted_frequencies = 0

    for i in range(len(psd_values)):
        # Update max_psd and accumulate weighted frequencies using element-wise multiplication
        is_new_max = psd_values[i] > max_psd
        max_psd = max_psd + is_new_max * (psd_values[i] - max_psd)
        weighted_frequencies = weighted_frequencies + is_new_max * (frequencies[i] - weighted_frequencies)

    # Use weighted_frequencies to classify the brainwave type
    delta = (weighted_frequencies < scale_frequency(4)) * 0
    theta = (weighted_frequencies >= scale_frequency(4)) * (weighted_frequencies < scale_frequency(8)) * 1
    alpha = (weighted_frequencies >= scale_frequency(8)) * (weighted_frequencies < scale_frequency(13)) * 2
    beta = (weighted_frequencies >= scale_frequency(13)) * (weighted_frequencies < scale_frequency(30)) * 3
    gamma = (weighted_frequencies >= scale_frequency(30)) * (weighted_frequencies < scale_frequency(100)) * 4

    # Sum up the results to get the brainwave type
    brainwave_type = delta + theta + alpha + beta + gamma

    return brainwave_type

# Compile the function for homomorphic execution
compiler = fhe.Compiler(
    classify_brainwave_homomorphic,
    {
        "psd_values": "encrypted",
        "frequencies": "encrypted",
    }
)

# Simulated input set for compilation (scaled to 16-bit range)
input_set = [
    ([scale_frequency(10), scale_frequency(6), scale_frequency(40)],  # PSD values
     [scale_frequency(2), scale_frequency(6), scale_frequency(40)]),  # Frequency values
    ([scale_frequency(20), scale_frequency(30), scale_frequency(50)],
     [scale_frequency(5), scale_frequency(10), scale_frequency(20)]),
]

print("Compilation...")
circuit = compiler.compile(input_set)

print("Key generation...")
circuit.keygen()

# Example data for homomorphic evaluation
psd_values = [scale_frequency(10), scale_frequency(25), scale_frequency(40)]  # Example PSD values
frequencies = [scale_frequency(2), scale_frequency(10), scale_frequency(40)]  # Example frequencies

# Encrypt the inputs
encrypted_psd, encrypted_freq = circuit.encrypt(psd_values, frequencies)

# Perform homomorphic classification
encrypted_result = circuit.run(encrypted_psd, encrypted_freq)

# Decrypt the result
brainwave_type = circuit.decrypt(encrypted_result)

# Map the brainwave type to its name
brainwave_names = ["Delta", "Theta", "Alpha", "Beta", "Gamma"]
if brainwave_type >= 0:
    print(f"Classified Brainwave: {brainwave_names[brainwave_type]}")
else:
    print("Brainwave Type: Unknown")
