import sys
import os
import random
from cipher_algorithm.baby_rijndael import babyr_enc, babyr_dec, print_b

sys.path.append(os.getcwd())


def convert_bytes_list_to_hex_integer(bytes_list: list) -> int:
    """
    Convert a list of bytes to a hexadecimal integer.

    Args:
    - bytes_list: The list of bytes to convert.

    Returns:
    An integer representing the hexadecimal value of the byte list.
    """
    hex_representation = ''.join([hex(x)[2:].zfill(2) for x in bytes_list])

    # Convert the concatenated hexadecimal string to an integer
    return int(hex_representation, 16)


def generate_cbc_dataset(size):
    """
    Generate a dataset for Cipher Block Chaining (CBC) mode.

    Args:
    - size: Number of pairs to generate.

    Returns:
    A list of tuples, each containing a ciphertext and key pair.
    """
    dataset = []
    for _ in range(size):
        # Generate a random 16-bit plaintext and key
        plaintext = random.randint(0, 0xFFFF)
        key = random.randint(0, 0xFFFF)

        # Generate a random 16-bit Initialization Vector (IV)
        initialization_vector = random.randint(0, 0xFFFF)

        # Encrypt the plaintext using CBC mode
        ciphertext = initialization_vector  # Initialization Vector for the first block
        for i in range(16):
            # XOR the plaintext with the previous ciphertext (or IV for the first block)
            plaintext ^= ciphertext
            # Encrypt the XORed result
            ciphertext = convert_bytes_list_to_hex_integer(babyr_enc(plaintext, key))

            # Append the encrypted block to the dataset
            dataset.append((ciphertext, key))

    return dataset


# Example: Generate a dataset with 10 random pairs of ciphertexts and keys in CBC mode
cbc_dataset = generate_cbc_dataset(10)

# Example of how to use your decryption function for CBC mode
for ciphertext, key in cbc_dataset:
    decrypted_block = babyr_dec(ciphertext, key)
    print("*" * 20)
    print(f"Original Ciphertext: {hex(ciphertext)}")
    print("-" * 30)
    print(f"Decrypted Block: {print_b(decrypted_block)}")
    print("*" * 20)
    print()


def frequency_test_within_block_cbc(dataset):
    bit_counts = [0] * 16

    for ciphertext, key in dataset:
        decrypted_block = babyr_dec(ciphertext, key)

        # Count the number of set bits for each position
        for bit_position in range(16):
            bit_counts[bit_position] += (decrypted_block[0] >> bit_position) & 1

    # Check if the bit distribution is approximately uniform
    threshold = len(dataset) // 2  # Assuming a balanced distribution
    for bit_position, count in enumerate(bit_counts):
        if count > threshold or count > len(dataset) - threshold:
            print(f"CBC Mode Frequency Test Failed")
        else:
            print(f"CBC Mode Frequency Test passed")


frequency_test_within_block_cbc(cbc_dataset)
