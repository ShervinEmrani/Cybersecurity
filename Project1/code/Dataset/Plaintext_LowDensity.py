import random
import sys
import os
from cipher_algorithm.baby_rijndael import babyr_enc, print_b

sys.path.append(os.getcwd())


def generate_low_density_dataset(size, density=0.2):
    """
    Generate a dataset with random low-density plaintexts and random keys.

    Args:
    - size: Number of pairs to generate.
    - density: Proportion of set bits in the plaintext (0.0 to 1.0).

    Returns:
    A list of tuples, each containing a low-density plaintext and a random key.
    """
    dataset = []
    for _ in range(size):
        # Generate a random 16-bit plaintext with low density
        plaintext = 0
        for _ in range(16):
            if random.random() < density:
                plaintext |= 1 << random.randint(0, 15)

        # Generate a random 16-bit key
        key = random.randint(0, 0xFFFF)

        dataset.append((plaintext, key))
    return dataset


# Example: Generate a dataset with 10 random pairs of low-density plaintexts and keys
low_density_dataset = generate_low_density_dataset(10, density=0.2)

# Example of how to use the encryption function
for plaintext, key in low_density_dataset:
    encrypted_block = babyr_enc(plaintext, key)
    print("*" * 20)
    print(f"Original Plaintext: {plaintext}")
    print("-" * 20)
    print(f"Encrypted Block: {print_b(encrypted_block)}")
    print("*" * 20)
    print()


def frequency_test_within_block_low_density_plaintext(dataset):
    bit_counts = [0] * 16

    for plaintext, key in dataset:
        encrypted_block = babyr_enc(plaintext, key)

        # Count the number of set bits for each position
        for bit_position in range(16):
            bit_counts[bit_position] += (encrypted_block[0] >> bit_position) & 1

    # Check if the bit distribution is approximately uniform
    threshold = len(dataset) // 2  # Assuming a balanced distribution
    for bit_position, count in enumerate(bit_counts):
        if count < threshold or count > len(dataset) - threshold:
            print(f"Low-Density with Plaintext Frequency Test Failed")


frequency_test_within_block_low_density_plaintext(low_density_dataset)
