import random
import sys
import numpy as np
import os
from cipher_algorithm.baby_rijndael import babyr_enc, print_b

sys.path.append(os.getcwd())


def generate_high_density_plaintext_dataset(size, plaintext_density=0.8, key_density=0.8):
    """
    Generate a dataset with random high-density plaintexts and keys.

    Args:
    - size: Number of pairs to generate.
    - plaintext_density: Proportion of set bits in the plaintext (0.0 to 1.0).
    - key_density: Proportion of set bits in the key (0.0 to 1.0).

    Returns:
    A list of tuples, each containing a high-density plaintext and a high-density key.
    """
    dataset = []
    for _ in range(size):
        # Generate a random 16-bit plaintext with high density
        plaintext = 0
        for i in range(16):
            if random.random() < plaintext_density:
                plaintext |= 1 << i

        # Generate a random 16-bit key with high density
        key = 0
        for i in range(16):
            if random.random() < key_density:
                key |= 1 << i

        dataset.append((plaintext, key))
    return dataset


# Example: Generate a dataset with 10 random pairs of high-density plaintexts and keys
high_density_plaintext_dataset = generate_high_density_plaintext_dataset(10, plaintext_density=0.8, key_density=0.8)

# Example of how to use the encryption function
for plaintext, key in high_density_plaintext_dataset:
    encrypted_block = babyr_enc(plaintext, key)
    print("*" * 25)
    print(f"Original Plaintext: {plaintext}")
    print("-" * 25)
    print(f"Original Key: {key}")
    print("-" * 25)
    print(f"Encrypted Block: {print_b(encrypted_block)}")
    print("*" * 25)
    print()


def frequency_test_within_block_high_density_plaintext(dataset):
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
            print(f"High density with plaintext Frequency Test Failed")


def binary_matrix_rank_test_high_density_plaintext(dataset):
    for plaintext, key in dataset:
        encrypted_block = babyr_enc(plaintext, key)

        # Form binary matrix
        matrix = [[(plaintext >> j) & 1 for j in range(16)]]

        # Add ciphertext row
        matrix.append([(encrypted_block[0] >> j) & 1 for j in range(16)])

        # Check binary matrix rank
        rank = np.linalg.matrix_rank(matrix)

        if rank != 2:
            print(f"High-Density with Plaintext Binary Matrix Rank Test Failed: Rank is {rank}, expected 2")


print("*" * 25)
frequency_test_within_block_high_density_plaintext(high_density_plaintext_dataset)
print()
print("*" * 25)
binary_matrix_rank_test_high_density_plaintext(high_density_plaintext_dataset)
