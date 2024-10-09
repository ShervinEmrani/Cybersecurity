from cipher_algorithm.baby_rijndael import babyr_enc, babyr_dec


def perform_bitwise_test(encryption_function, test_type):
    """
    Perform a bitwise test on the given encryption function.

    Args:
    - encryption_function: The encryption function to test.
    - test_type: The type of bitwise test (e.g., 'Strict Avalanche', 'Avalanche', 'Completeness').
    """
    block_input = 0x5b69
    key_input = 0x87b2

    original_output = encryption_function(block_input, key_input)

    for i in range(16):
        modified_block = block_input ^ (1 << i)
        modified_output = encryption_function(modified_block, key_input)

        # Output the result of the bitwise test
        print(f"{test_type} Test - Bit {i + 1}: {'Pass' if modified_output != original_output else 'Fail'}")


# Run strict avalanche test on encryption
print("\nStrict Avalanche Test: ")
print("**On all 16 bits of output**")
perform_bitwise_test(babyr_enc, 'Strict Avalanche')


# Run avalanche test on encryption
print("\nAvalanche Test: ")
print("**On all 16 bits of output**")
perform_bitwise_test(babyr_enc, 'Avalanche')


def completeness_test(encryption_function):
    """
    Perform a completeness test on the given encryption function.

    Args:
    - encryption_function: The encryption function to test.
    """
    for i in range(16):
        block_input = 0x5b31
        key_input = 0x87b2

        original_output = encryption_function(block_input, key_input)

        modified_block = block_input ^ (1 << i)
        modified_output = encryption_function(modified_block, key_input)

        # Output the result of the completeness test
        print(f"Completeness Test - Bit {i + 1}: {'Pass' if modified_output != original_output else 'Fail'}")


# Run completeness test on encryption
print("\nCompleteness Test: ")
print("**On all 16 bits of output**")
completeness_test(babyr_enc)
