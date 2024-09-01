import unittest

from altered_deckfmt import decode, encode


class TestDeckFMT(unittest.TestCase):
    def setUp(self) -> None:
        self.decklist_files = [
            (
                "list_1offs.txt",
                "ECAU2RjKFlBScpaUlWVLJFkwysZc0wLFzMh2NTYZw0+GfIEXS4ZWtOmYNMRmyzgp6N+mcjOU",
            ),
            ("list_2sets.txt", "ECAjGhnSHpR0s6gdRaqPWRrRVp64deQESnV0UqcdPA=="),
            (
                "list_uniques.txt",
                "EBAVnBjhHww4lcSeILFNjDx5S+so2TPLDRcOHGX4iUOcWt1XazI5t8wW8g==",
            ),
            ("list_yzmir.txt", "EBAk3hnUK4h8daVOIvjFyx5h846zfTGuXmb6p9YuwPaHsgA="),
            ("test_extd_qty.txt", "EBAgTTMo"),
            ("test_long_uniq.txt", "EBARGz4JpNnycPbPmBy2f//8"),
            ("test_mana_orb.txt", "EBAg3hHfC8IA"),
        ]

    def test_encode_string(self):
        for file, expected_result in self.decklist_files:
            with self.subTest(file=file):
                decklist = self.read_decklist(file)
                result = encode(decklist)
                self.assertEqual(result, expected_result)

    def test_decode_string(self):
        for file, encoded_decklist in self.decklist_files:
            with self.subTest(file=file):
                result = decode(encoded_decklist)
                decklist = self.read_decklist(file)
                self.assertEqual(result, decklist)

    @staticmethod
    def read_decklist(decklist_file) -> str:

        with open(f"./tests/decklists/{decklist_file}") as f:
            return f.read()


if __name__ == "__main__":
    unittest.main()
