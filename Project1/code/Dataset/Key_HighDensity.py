import random
import sys
import os
from cipher_algorithm.baby_rijndael import babyr_enc, print_b

sys.path.append(os.getcwd())


def generate_high_density_key_dataset(size, key_density=0.8):
    """
    Generate a dataset with random plaintexts and high-density keys.

    Args:
    - size: Number of pairs to generate.
    - key_density: Proportion of set bits in the key (0.0 to 1.0).

    Returns:
    A list of tuples, each containing a plaintext and a high-density key.
    """
    dataset = []
    for _ in range(size):
        # Generate a random 16-bit plaintext
        plaintext = random.randint(0, 0xFFFF)

        # Generate a random 16-bit key with high density
        key = 0
        for i in range(16):
            if random.random() < key_density:
                key |= 1 << i

        dataset.append((plaintext, key))
    return dataset


# Example: Generate a dataset with 10 random pairs of random plaintexts and high-density keys
high_density_key_dataset = generate_high_density_key_dataset(10, key_density=0.9)

# Example of how to use the encryption function
for plaintext, key in high_density_key_dataset:
    encrypted_block = babyr_enc(plaintext, key)
    print("*" * 20)
    print(f"Original Plaintext: {plaintext}")
    print("-" * 20)
    print(f"High-Density Key: {key}")
    print("-" * 20)
    print(f"Encrypted Block: {print_b(encrypted_block)}")
    print("*" * 20)
    print()


def frequency_test_within_block_high_density_key(dataset):
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
            print(f"High-Density with Key Frequency Test Failed")




frequency_test_within_block_high_density_key(high_density_key_dataset)
