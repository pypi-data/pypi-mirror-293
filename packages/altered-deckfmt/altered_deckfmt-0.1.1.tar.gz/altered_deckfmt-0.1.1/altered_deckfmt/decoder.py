import logging

from .exceptions import DecodeException
from .models import CardSet, DeckFMT, Faction, Product, Rarity
from .utils import base64_to_string, decode_chunk

logger = logging.getLogger(__name__)


def decode(string: str) -> str:
    """Method to receive an encoded decklist and decode it into the regular notation.

    The basic idea that uses is:
    * Extract the version and the quantity of sets
    * Iterate each set by extracting the current set and how many cards it contains
    * Iterate each card and extract its quantity and the card reference

    While doing this, the variable `index` will be used to extract the information and
    keep track of the current position within the string with binary values. Once a
    chunk of data has been extracted, the index needs to be moved to the beginning of
    the next information.

    Args:
        string (str): The encoded decklist.

    Returns:
        str: The decoded decklist.
    """

    # Transform the string from base64 to a string with 0s and 1s
    string = base64_to_string(string.strip())
    result = []

    # Retrieve the version and the count of groups
    _, group_count = _decode_header(string)

    # Start the index right after the header. The start index will always be the same
    index = DeckFMT.SET_GROUP_START_INDEX

    # Iterate each set group
    for _ in range(group_count):
        # Extract the current set group id and how many cards it contains
        index, set_code, card_count = _decode_set_group(string, index)

        # Iterate each card of the set
        for _ in range(card_count):

            # Extract the amount of copies of the card
            index, quantity = _decode_card_ref_quantity(string, index)

            # Extract the card's data
            index, *card_data = _decode_card(string, index)
            
            # Build the card reference with the extracted information
            reference = _build_card_referece(set_code, *card_data)

            logger.debug(f"Parsed {quantity} units of '{reference}'")

            # Create the line for this decoded card
            result.append(f"{quantity} {reference}")

    return "\n".join(result)


def _decode_header(string: str) -> tuple[int, int]:
    """Extract the header frame from the encoded decklist.

    Args:
        string (str): The encoded decklist.

    Raises:
        DecodeError: If the encoded string is using an unknown version of DeckFMT.
        DecodeError: If the frame contains 0 set groups.

    Returns:
        tuple[int, int]: The version and the amount of set groups
    """

    # Extract the version and assert that it's valid
    version = decode_chunk(string, 0, DeckFMT.VERSION_BITS)
    if version != DeckFMT.VERSION_NUMBER:
        raise DecodeException(f"Unknown version: {version}")
    logger.debug(f"Detected version {version} of DeckFMT")

    # Extract the group count and assert that it's valid
    group_count = decode_chunk(string, DeckFMT.VERSION_BITS, DeckFMT.GROUPS_COUNT_BITS)
    if group_count == 0:
        raise DecodeException(f"Invalid number of groups: {group_count}")
    logger.debug(f"Found {group_count} set groups")

    return version, group_count


def _decode_set_group(string: str, index: int) -> tuple[int, str, int]:
    """Extract the frame information of a set group.
    Move the index to the beginning of the next data chunk.

    Args:
        string (str): The encoded decklist.
        index (int): The start position of the set group.

    Returns:
        tuple[int, str, int]: The index of the next field, the set's code and the
                              amount of cards it contains.
    """

    # Extract the set's id (int) and convert it to its string representation
    # (e.g. 1 => COREKS)
    set_num = decode_chunk(string, index, DeckFMT.SET_COUNT_BITS)
    set_code = CardSet(set_num).name
    index += DeckFMT.SET_COUNT_BITS

    # Extract the amount of cards belonging to this set
    card_count = decode_chunk(string, index, DeckFMT.REFS_COUNT_BITS)
    index += DeckFMT.REFS_COUNT_BITS

    logger.debug(f"Encountered {card_count} cards of set '{set_code}'")

    return index, set_code, card_count


def _decode_card_ref_quantity(string: str, index: int) -> tuple[int, int]:
    """Extract the amount of copies of a card.
    Move the index to the beginning of the next data chunk.

    Args:
        string (str): The encoded decklist.
        index (int): The start position of the card quantity value.

    Returns:
        tuple[int, int]: The index of the next field and the amount of copies.
    """

    # Extract the base quantity of the card
    quantity = decode_chunk(string, index, DeckFMT.CARD_QUANTITY_BITS)
    index += DeckFMT.CARD_QUANTITY_BITS

    # If the quantity is 0, extract the next 6 bits as they will contain the actual
    # quantity minus 3
    if quantity == 0:
        extended_quantity = decode_chunk(
            string, index, DeckFMT.CARD_EXTENDED_QUANTITY_BITS
        )
        quantity = extended_quantity + 3
        index += DeckFMT.CARD_EXTENDED_QUANTITY_BITS

    return index, quantity


def _decode_card(string: str, index: int) -> tuple[int, str, str, int, str, int]:
    """Extract the card's information.

    Args:
        string (str): The encoded decklist.
        index (int): The start position of the card's data.

    Returns:
        tuple[int, str, str, int, str, int]: The index, the product code, the faction
                                             code, the number within the faction, the
                                             rarity code and the unique id if any.
    """

    # Extract if the default product (B) is being used
    default_product = decode_chunk(string, index, DeckFMT.CARD_BOOSTER_BITS)
    index += DeckFMT.CARD_BOOSTER_BITS
    if default_product:
        product_code = DeckFMT.DEFAULT_PRODUCT
    else:
        # If the default product is not used, extract the product from the next bits
        product_num = decode_chunk(string, index, DeckFMT.CARD_PRODUCT_BITS)
        index += DeckFMT.CARD_PRODUCT_BITS
        product_code = Product(product_num).name

    # Extract the faction id and convert it into its string representation
    # (e.g. 1 => AX)
    faction_num = decode_chunk(string, index, DeckFMT.CARD_FACTION_BITS)
    faction_code = Faction(faction_num).name
    index += DeckFMT.CARD_FACTION_BITS

    # Extract the number of the card within its own faction
    number_in_faction = decode_chunk(string, index, DeckFMT.CARD_NUMBER_BITS)
    index += DeckFMT.CARD_NUMBER_BITS

    # Extract the rarity id and convert it into its string representation
    # (e.g. 1 => R1)
    rarity_num = decode_chunk(string, index, DeckFMT.CARD_RARITY_BITS)
    rarity_code = Rarity(rarity_num).name
    index += DeckFMT.CARD_RARITY_BITS

    # If the card is unique, extract the next 16 bits that contain its unique id
    if rarity_code == "U":
        unique_id = decode_chunk(string, index, DeckFMT.CARD_UNIQUE_ID_BITS)
        index += DeckFMT.CARD_UNIQUE_ID_BITS
    else:
        unique_id = None

    return index, product_code, faction_code, number_in_faction, rarity_code, unique_id


def _build_card_referece(
    card_set: str, product: str, faction: str, number: int, rarity: str, unique_id: int
) -> str:
    """Receive a card's identifying factors and generate its reference.

    Args:
        card_set (str): The code of the set.
        product (str): The code of the product.
        faction (str): The code of the faction.
        number (int): The number of the card in its own faction.
        rarity (str): The code of the rarity.
        unique_id (int): If it's unique, the unique id. Otherwise, None.

    Returns:
        str: The reference of a card.
    """

    if faction != "NE":
        return f"ALT_{card_set}_{product}_{faction}_{number:02d}_{rarity}" + (
            f"_{unique_id}" if unique_id else ""
        )
    else:
        # For some reason the Mana Token has its number with a single digit instead of 2
        return f"ALT_{card_set}_{product}_{faction}_{number}_{rarity}"
