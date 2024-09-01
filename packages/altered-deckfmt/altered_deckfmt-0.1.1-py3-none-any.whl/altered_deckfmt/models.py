"""This module defines all the necessary models and constants for this package.

To encode and decode decklists it's necessary to convert multiple values between their
code and it's value and viceversa (e.g. "CORE" to 2 and 2 to "CORE").

To avoid maintaining two dicts to convert between those values, this package makes use
of Enums, as they allow the following operations:

```
CardSet["CORE"]  # CardSet.CORE
CardSet(2)       # CardSet.CORE
```

And from the Enum the reverse value or name can be obtained:

```
CardSet["CORE"].value  # 2
CardSet(2).name        # "CORE"
```

However, whilst this works perfectly, a base Enum class and a metaclass are also
defined because this allows to use the custom exceptions for encoding and decoding
errors.

```
CardSet["TANUKI"]   # Raises EncodeException
CardSet(2024)       # Raises DecodeException
```
"""

from enum import Enum, EnumMeta

from .exceptions import DecodeException, EncodeException


class FMTEnumMeta(EnumMeta):
    """This metaclass is a trick to manipulate how an enum is accessed. Doing it this
    way it allows to add a more relevant exception when the operation fails."""

    def __getitem__(cls, name: str):
        """Custom __getitem__ method used to raise EncodeException if `name` is not a
        valid item for the Enum."""
        try:
            return super().__getitem__(name)
        except KeyError:
            raise EncodeException(
                f"Code '{name}' could not be converted to {cls.__name__}"
            )


class FMTEnum(Enum, metaclass=FMTEnumMeta):
    """Base class for the Enums used to encode and decode values."""

    @classmethod
    def _missing_(cls, value):
        """If attempting to instantiate an object with a value that doesn't exist in
        the enum, this method will raise a DecodeException.
        """
        raise DecodeException(
            f"Value '{value}' could not be converted to {cls.__name__}"
        )


class CardSet(FMTEnum):
    """Enum representing different sets of cards."""

    COREKS = 1
    CORE = 2


class Product(FMTEnum):
    """Enum representing the extended products (other than boosters)"""

    P = 1
    A = 2


class Faction(FMTEnum):
    """Enum representing the different factions."""

    AX = 1
    BR = 2
    LY = 3
    MU = 4
    OR = 5
    YZ = 6
    NE = 7


class Rarity(FMTEnum):
    """Enum representing different rarity levels of cards."""

    C = 0
    R1 = 1
    R2 = 2
    U = 3


class DeckFMT:
    """
    Class containing constants for deck format specifications.

    Attributes:
        VERSION_NUMBER (int): Version number of the deck format (value: 1).

        *_BITS (int): Number of bits allocated for the field in the frame.

        SET_GROUP_START_INDEX (int): Start index for set groups (calculated from
                                     version and group bits, which comprise the header)
    """

    VERSION_NUMBER = 1
    DEFAULT_PRODUCT = "B"

    VERSION_BITS = 4
    GROUPS_COUNT_BITS = 8
    SET_COUNT_BITS = 8
    REFS_COUNT_BITS = 6
    CARD_QUANTITY_BITS = 2
    CARD_EXTENDED_QUANTITY_BITS = 6
    CARD_BOOSTER_BITS = 1
    CARD_PRODUCT_BITS = 2
    CARD_FACTION_BITS = 3
    CARD_NUMBER_BITS = 5
    CARD_RARITY_BITS = 2
    CARD_UNIQUE_ID_BITS = 16

    SET_GROUP_START_INDEX = VERSION_BITS + GROUPS_COUNT_BITS
