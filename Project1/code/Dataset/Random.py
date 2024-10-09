import numpy as np
import sys
import os
import random
from cipher_algorithm.baby_rijndael import babyr_enc, babyr_dec, print_b

# Add the current working directory to the system path
sys.path.append(os.getcwd())

# Import necessary functions from the cipher_algorithm module


def generate_random_dataset(size):
    """
    Generate a random dataset of block-key pairs.

    Args:
    - size: Number of random pairs to generate.

    Returns:
    A list of tuples, each containing a random 16-bit block and key.
    """
    dataset = []
    for _ in range(size):
        # Generating random 16-bit block and key
        block = random.randint(0, 0xFFFF)
        key = random.randint(0, 0xFFFF)
        dataset.append((block, key))
    return dataset


# Example: Generate a dataset with 10 random pairs of blocks and keys
random_dataset = generate_random_dataset(10)

# Example of how to use encryption and decryption functions
for block, key in random_dataset:
    # Encrypt the block using the generated key
    encrypted_block = babyr_enc(block, key)

    # Convert the encrypted block to a hex string for display
    hex_string = ''.join([hex(b)[2:].zfill(2) for b in encrypted_block])

    # Decrypt the block using the original key
    decrypted_block = babyr_dec(int(hex_string, 16), key)

    # Display the original block, encrypted block, and decrypted block
    print("*" * 30)
    print(f"Original Block: {block}")
    print("-" * 30)
    print(f"Encrypted Block: {print_b(encrypted_block)}")
    print("-" * 30)
    print(f"Decrypted Block: {print_b(decrypted_block)}")
    print("*" * 30)
    print()


def frequency_test_within_block_random(dataset):
    # Initialize a list to store the count of set bits for each bit position
    bit_counts = [0] * 16

    # Iterate through each (block, key) pair in the dataset
    for block, key in dataset:
        # Encrypt the block using the provided key
        encrypted_block = babyr_enc(block, key)

        # Count the number of set bits for each bit position in the encrypted block
        for bit_position in range(16):
            bit_counts[bit_position] += (encrypted_block[0] >> bit_position) & 1

    # Check if the bit distribution is approximately uniform
    threshold = len(dataset) // 2  # Assuming a balanced distribution
    for bit_position, count in enumerate(bit_counts):
        if count < threshold or count > len(dataset) - threshold:
            print(f"Random Frequency Test Failed")
        else:
            print(f"Random Mode Frequency Test passed")


def binary_matrix_rank_test_random(dataset):
    for block, key in dataset:
        encrypted_block = babyr_enc(block, key)

        # Form binary matrix
        matrix = [[(block >> j) & 1 for j in range(16)]]

        # Add ciphertext row
        matrix.append([(encrypted_block[0] >> j) & 1 for j in range(16)])

        # Check binary matrix rank
        rank = np.linalg.matrix_rank(matrix)

        if rank != 2:
            print(f"Random Binary Matrix Rank Test Failed: Rank is {rank}, expected 2")


# Example usage: Perform the frequency test on the provided random dataset
print("*" * 25)
frequency_test_within_block_random(random_dataset)
print()
print("*" * 25)
binary_matrix_rank_test_random(random_dataset)

