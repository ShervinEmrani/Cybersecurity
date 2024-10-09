import sys
import os
import random
from cipher_algorithm.baby_rijndael import babyr_enc

sys.path.append(os.getcwd())


def encrypt(plaintext, key):
    """
    Encrypt the given plaintext using a provided key.

    Args:
    - plaintext: The original plaintext to be encrypted.
    - key: The encryption key.

    Returns:
    The resulting ciphertext after encrypting the plaintext with the key.
    """
    return babyr_enc(plaintext, key)


def plaintext_ciphertext_correlation_dataset(encryption_function, num_samples=1000, block_size=16):
    """
    Generate a dataset to analyze the correlation between plaintext and ciphertext.

    Args:
    - encryption_function: The encryption function to use.
    - num_samples: Number of samples to generate.
    - block_size: Size of the encryption block.

    Returns:
    A list of dictionaries, each containing information about a plaintext-ciphertext pair.
    """
    dataset = []
    for _ in range(num_samples):
        # Generate a random plaintext
        plaintext = random.randint(0, 2 ** block_size - 1)

        # Generate a random key
        key = random.randint(0, 2 ** block_size - 1)

        # Encrypt the plaintext with the key
        ciphertext = encrypt(plaintext, key)

        # Record the sample in the dataset
        dataset.append({
            'plaintext': plaintext,
            'key': key,
            'ciphertext': ciphertext,
        })

    return dataset


# Example usage
random.seed(42)  # For reproducibility
dataset = plaintext_ciphertext_correlation_dataset(babyr_enc, num_samples=1000)

# Print the first few samples
for sample in dataset[:5]:
    print("*" * 25)
    print(f"Original Plaintext: {sample['plaintext']}")
    print("-" * 25)
    print(f"Encryption Key: {sample['key']}")
    print("-" * 25)
    print(f"Generated Ciphertext: {sample['ciphertext']}")
    print("*" * 25)
    print()


def frequency_test_within_block_plaintext_ciphertext_correlation(dataset):
    bit_counts = [0] * 16

    for sample in dataset:
        ciphertext = sample['ciphertext']

        # Count the number of set bits for each position
        for bit_position in range(16):
            bit_counts[bit_position] += (ciphertext[0] >> bit_position) & 1

    # Check if the bit distribution is approximately uniform
    threshold = len(dataset) // 2  # Assuming a balanced distribution
    for bit_position, count in enumerate(bit_counts):
        if count < threshold or count > len(dataset) - threshold:
            print(f"Plaintext-Ciphertext Correlation Frequency Test Failed")


frequency_test_within_block_plaintext_ciphertext_correlation(dataset)
