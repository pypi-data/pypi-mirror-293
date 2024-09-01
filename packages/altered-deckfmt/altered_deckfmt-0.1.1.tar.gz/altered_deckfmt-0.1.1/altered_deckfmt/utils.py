import base64
from collections import defaultdict

from .exceptions import EncodeException


def parse_decklist(string: str, separator: str) -> dict[str, list[tuple[int, str]]]:
    """Function to parse a decklist and return a data structure that allows for easier
    access.

    It groups the data in a dictionary, which uses the set code as a key and the
    extracted cards in a list comprised of a tuple with the quantity of the card and
    the card reference. For example:

    {
        "COREKS": [(1, "ALT_COREKS_B_AX_03_C"), (2, "ALT_COREKS_B_AX_08_R1")],
        "CORE": [(1, "ALT_CORE_B_AX_14_C"), (2, "ALT_CORE_B_AX_11_R1")],
    }

    This structure is easy to generate, count its elements and iterate them.

    Args:
        string (str): The string containing the decklist.
        separator (str): The separator of the decklist.

    Returns:
        dict[str, list[tuple[int, str]]]: The data structure containing the decks data.
    """

    # Use a `defaultdict` to avoid controlling the first insertion of a set
    card_sets = defaultdict(list)

    # Iterate each card
    for line in string.split(separator):
        # Remove spaces at the beginning and at the end and ignore empty lines
        if content := line.strip():
            quantity, reference = content.split()
            card_set = reference.split("_")[1]
            card_sets[card_set].append((int(quantity), reference))

    return card_sets


def string_to_base64(binary_string: str) -> str:
    """Convert a string with 0s and 1s representing bits to base64.

    Args:
        binary_string (str): A string with binary values.

    Returns:
        str: The received string in base64.
    """

    # Calculate if any padding is necessary and add it
    num_bits = len(binary_string)
    padded_num_bits = num_bits if num_bits % 8 == 0 else num_bits + 8 - (num_bits % 8)
    binary_string = binary_string.ljust(padded_num_bits, "0")
    # Separate the string characters in chunks of 8, convert it from base2 to decimal
    # and to a bytes object which can be converted to base64
    binary_bytes = bytes(
        int(binary_string[i : i + 8], 2) for i in range(0, padded_num_bits, 8)
    )

    # Return the base64 string removing trailing characters (e.g. b'EBAgTSZQ')
    return str(base64.b64encode(binary_bytes))[2:-1]


def base64_to_string(encoded_string: str) -> str:
    """Convert a base64 string to a string with binary values.

    Args:
        encoded_string (str): A string with a base64 value.

    Returns:
        str: The received string converted to 0s and 1s.
    """
    decoded = base64.b64decode(encoded_string)
    binary_string = bin(int.from_bytes(decoded))[2:]
    num_bytes = (len(binary_string) + 7) // 8 * 8

    return binary_string.zfill(num_bytes)


def encode_chunk(value: int, size: int) -> str:
    """Function to receive a value, transform it to binary using `size` bits.
    If `value` does not fit in that amount of bits, EncodeException is raised.

    Args:
        value (int): The value to be encoded.
        size (int): The amount of bits used to encode it. If `value` uses less, it adds
                    0 on the left. If `value` uses more, EncodeException is raised.

    Raises:
        EncodeException: If `value` cannot be represented in `size` bits.

    Returns:
        str: The value in binary.
    """
    if value >= 2**size:
        raise EncodeException(f"Can't encode the number '{value}' in {size} bits")
    return format(value, f"0{size}b")


def decode_chunk(string: str, start: int, size: int) -> int:
    """Function that receives a string with binary values, extracts `size` values from
    the `start` index and converts it from binary to decimal.

    Args:
        string (str): String containing 0 and 1 values.
        start (int): The index where the number starts.
        size (int): The amount of characters needed to extract the number.

    Returns:
        int: The extracted number in decimal.
    """
    return int(string[start : (start + size)], 2)
