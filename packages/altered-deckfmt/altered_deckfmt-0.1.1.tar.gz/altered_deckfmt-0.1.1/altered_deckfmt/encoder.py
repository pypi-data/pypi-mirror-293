from .exceptions import EncodeException
from .models import CardSet, DeckFMT, Faction, Product, Rarity
from .utils import encode_chunk, parse_decklist, string_to_base64


def encode(string: str, sep: str = "\n") -> str:
    """Method that receives a decklist and encodes it to DeckFMT.

    The basic idea that uses is:
    * Parse the decklist to a datastructure that it's easier to iterate.
    * Generate the header and encode the amount of set groups.
    * For each set, encode its identifier and the amount of cards it contains.
    * For each card, encode its quantity and the card reference.

    While doing this, the variable 'result' will be a string containing 0s and 1s with
    the generated chunks. Once a frame has been encoded, it will be appended to this
    string. The end result will contain the whole decklist encoded, which will then
    need to be converted to base64 before returning.

    Args:
        string (str): The decklist.
        sep (str, optional): The character separating each card. Defaults to "\n".

    Raises:
        EncodeError: If a value cannot be represented in the designated amount of bits.
                     For example, if attempting to encode a card's unique id that is
                     greater than 65535.
                     It is also raised if attempting to encode 0 set groups or a set
                     with 0 cards.

    Returns:
        str: The encoded decklist.
    """

    # Transform the decklist to a more maleable data structure: A dictionary where each
    # key is a set identifier and contains its cards information:
    # {
    #     "COREKS": [(1, "ALT_COREKS_B_AX_03_C"), (2, "ALT_COREKS_B_AX_08_R1")],
    #     "CORE": [(1, "ALT_CORE_B_AX_14_C"), (2, "ALT_CORE_B_AX_11_R1")],
    # }
    cards = parse_decklist(string, sep)

    # Encode the header (version + set groups count)
    result = _encode_header(len(cards))

    # Iterate each group set
    for card_set, cards in cards.items():

        # Encode each set data (id + card count)
        result += _encode_set_group(card_set, len(cards))

        # Iterate and encode each card
        for quantity, card in cards:
            result += _encode_card_ref_quantity(quantity)
            result += _encode_card(card)

    # Change the string in binary to base64
    return string_to_base64(result)


def _encode_header(card_sets: int) -> str:
    """Encode the header of the decklist. It is comprised of the current version of
    DeckFMT and the amount of set groups.

    Args:
        card_sets (int): Amount of sets in the decklist.

    Raises:
        EncodeError: If attempting to encode a group count of 0 or less.

    Returns:
        str: The encoded header.
    """

    # Encode the DeckFMT version
    result = encode_chunk(DeckFMT.VERSION_NUMBER, DeckFMT.VERSION_BITS)

    # Assert that it's a valid amount of groups and encode it
    if card_sets <= 0:
        raise EncodeException(f"Cannot encode '{card_sets}' set groups")
    result += encode_chunk(card_sets, DeckFMT.GROUPS_COUNT_BITS)

    return result


def _encode_set_group(card_set: str, card_count: int) -> str:
    """Encode a set group's information, which is comprised of its set value and the
    amount of cards from that set.

    Args:
        card_set (str): The set's code (e.g. CORE).
        card_count (int): The amount of cards of the given set.

    Raises:
        EncodeError: If there are 0 or less cards from the set.

    Returns:
        str: The encoded set group.
    """

    # Encode the set id
    result = encode_chunk(CardSet[card_set].value, DeckFMT.SET_COUNT_BITS)

    # Assert that there's a valid amount of cards and encode it
    if card_count <= 0:
        raise EncodeException(f"Cannot encode '{card_count}' cards")
    result += encode_chunk(card_count, DeckFMT.REFS_COUNT_BITS)

    return result


def _encode_card_ref_quantity(quantity: int) -> str:
    """Encode the amount of copies of a given card. It uses a variable amount of bits
    to encode it depending on the number.

    Args:
        quantity (int): The amount of copies of a card.

    Raises:
        EncodeError: If attempting to encode a quantity of 0 or less.

    Returns:
        str: The encoded card quantity.
    """

    if quantity > 3:
        # If there are more than 3 cards, subtract 3, set the quantity's base bits to 0
        # and encode the extended quantity in the next bits
        return encode_chunk(0, DeckFMT.CARD_QUANTITY_BITS) + encode_chunk(
            quantity - 3, DeckFMT.CARD_EXTENDED_QUANTITY_BITS
        )
    elif quantity <= 0:
        # Raise an encoding exception if attempting to encode an invalid amount
        raise EncodeException(f"Cannot encode '{quantity}' copies of a card")
    else:
        # Encode the quantity
        return encode_chunk(quantity, DeckFMT.CARD_QUANTITY_BITS)


def _encode_card(reference: str) -> str:
    """Encode the card's reference. Extracts and encodes the product, faction, number
    and rarity of a card. If the card is unique, it also encodes the unique id.

    Args:
        reference (str): A card's reference.

    Returns:
        str: The encoded card.
    """

    # Extract the card's information ignoring the set and product information
    product, faction, number, rarity, *extra = reference.split("_")[2:]

    # Indicate if the product is the default (B). If it isn't use some extra bits to
    # encode the actual product
    if product == DeckFMT.DEFAULT_PRODUCT:
        result = encode_chunk(1, DeckFMT.CARD_BOOSTER_BITS)
    else:
        result = encode_chunk(0, DeckFMT.CARD_BOOSTER_BITS)
        result += encode_chunk(Product[product], DeckFMT.CARD_PRODUCT_BITS)

    # Encode the extracted information
    result += encode_chunk(Faction[faction].value, DeckFMT.CARD_FACTION_BITS)
    result += encode_chunk(int(number), DeckFMT.CARD_NUMBER_BITS)
    result += encode_chunk(Rarity[rarity].value, DeckFMT.CARD_RARITY_BITS)
    if rarity == "U":
        result += encode_chunk(int(extra[0]), DeckFMT.CARD_UNIQUE_ID_BITS)

    return result
