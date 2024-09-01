# altered-deckfmt

> This repository is a Python library of the original specification defined in [Taum/altered-deckfmt](https://github.com/Taum/altered-deckfmt).

A Compact format to share decklists for Altered TCG.

This binary format can be encoded to Base64 to share decks in URL-safe codes. As an example, a reasonable decklist such as:

```
1 ALT_CORE_B_YZ_03_C
3 ALT_CORE_B_BR_16_R2
2 ALT_CORE_B_YZ_04_C
3 ALT_CORE_B_YZ_07_R1
1 ALT_CORE_B_BR_10_R2
1 ALT_CORE_B_MU_08_R2
3 ALT_CORE_B_YZ_06_C
2 ALT_CORE_B_YZ_11_C
1 ALT_CORE_B_YZ_12_C
3 ALT_CORE_B_YZ_14_C
3 ALT_CORE_B_BR_25_R2
3 ALT_CORE_B_YZ_19_C
1 ALT_CORE_B_BR_28_R2
3 ALT_CORE_B_MU_25_R2
3 ALT_CORE_B_YZ_21_C
3 ALT_CORE_B_YZ_22_C
2 ALT_CORE_B_YZ_24_C
1 ALT_CORE_B_YZ_26_C
1 ALT_CORE_B_YZ_25_C
```

Can be encoded into the string:
```
EBAk3DNQrEPHVKmIvGLLHMPONZvTFcuZvVPWLYHaHZA=
```

This project provides a Python package that can be imported into a project.

Demo page to encode/decode decklists: https://taum.github.io/altered-deckfmt/

Note that this is a Python implementation of [the original format specification](https://github.com/Taum/altered-deckfmt/blob/main/FORMAT_SPEC.md), which I will try to keep up to date.

## Installation

Install the [PyPI package](https://pypi.org/project/altered-deckfmt/) using `pip`.
```bash
pip install altered-deckfmt
```

## Usage

Encode a decklist:

```python
from altered_deckfmt import encode, EncodeException


decklist = """1 ALT_COREKS_B_AX_08_C
1 ALT_COREKS_B_AX_03_C
1 ALT_COREKS_B_AX_08_R1
"""

try:
    encoded_decklist = encode(decklist)
    print(encoded_decklist)
    # EBAQ0oEjEoQ=
except EncodeException:
    print("Failed to encode the decklist")
```

Decode a decklist:

```python
from altered_deckfmt import decode, DecodeException


encoded_decklist = "EBAQ0oEjEoQ="

try:
    decklist = decode(encoded_decklist)
    print(decklist)
    # 1 ALT_COREKS_B_AX_08_C
    # 1 ALT_COREKS_B_AX_03_C
    # 1 ALT_COREKS_B_AX_08_R1
except DecodeException:
    print("Failed to decode the decklist")
```


##  Run Tests

```
python -m unittest discover tests
```
