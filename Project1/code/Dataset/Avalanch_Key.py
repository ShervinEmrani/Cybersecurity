import sys
import os
import secrets
import random
from cipher_algorithm.baby_rijndael import babyr_enc

sys.path.append(os.getcwd())


def encrypt(plaintext, key):
    # Replace this function with the actual encryption function
    return babyr_enc(plaintext, key)


def generate_random_key(block_size=16):
    # Use the secrets module for secure random key generation
    return secrets.randbits(block_size)


def avalanche_key_dataset(encryption_function, num_samples=1000, block_size=16):
    """
    Generate a dataset for avalanche testing with varying keys.

    Args:
    - encryption_function: The encryption function to test.
    - num_samples: Number of samples to generate.
    - block_size: Size of the encryption block.

    Returns:
    A list of dictionaries, each containing information about a sample.
    """
    dataset = []

    for _ in range(num_samples):
        # Generate a random plaintext
        plaintext = random.randint(0, 2 ** block_size - 1)

        # Generate two slightly different keys
        original_key = generate_random_key(block_size)
        modified_key = original_key ^ (1 << random.randint(0, block_size - 1))

        # Encrypt with the original key
        original_ciphertext = encrypt(plaintext, original_key)

        # Encrypt with the modified key
        modified_ciphertext = encrypt(plaintext, modified_key)

        # Record the sample in the dataset
        dataset.append({
            'plaintext': plaintext,
            'original_key': original_key,
            'modified_key': modified_key,
            'original_ciphertext': original_ciphertext,
            'modified_ciphertext': modified_ciphertext,
        })

    return dataset


# Set a random seed for reproducibility
random.seed(42)
dataset = avalanche_key_dataset(babyr_enc, num_samples=1000)

# Print the details of the first 10 samples
for sample in dataset[:10]:
    print("*" * 20)
    print(f"Plaintext: {sample['plaintext']}\n"
          f"Original Key: {sample['original_key']}\n"
          f"Modified Key: {sample['modified_key']}\n"
          f"Original Ciphertext: {sample['original_ciphertext']}\n"
          f"Modified Ciphertext: {sample['modified_ciphertext']}\n"
          f"{'*' * 20}")
    print()


def frequency_test_within_block_avalanche_key(dataset):
    bit_counts = [0] * 16

    for sample in dataset:
        modified_ciphertext = sample['modified_ciphertext']

        # Count the number of set bits for each position
        for bit_position in range(16):
            bit_counts[bit_position] += (modified_ciphertext[0] >> bit_position) & 1

    # Check if the bit distribution is approximately uniform
    threshold = len(dataset) // 2  # Assuming a balanced distribution
    for bit_position, count in enumerate(bit_counts):
        if count < threshold or count > len(dataset) - threshold:
            print(f"Avalanche Key Frequency Test Failed")


frequency_test_within_block_avalanche_key(dataset)
