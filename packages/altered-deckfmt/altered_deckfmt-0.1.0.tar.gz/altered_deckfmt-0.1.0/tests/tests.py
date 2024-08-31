import unittest

from altered_deckfmt import decode, encode


class TestDeckFMT(unittest.TestCase):
    def setUp(self) -> None:
        self.decklist_files = [
            (
                "list_1offs.txt",
                "ECAU0jEoUoInItIlUqUkUmErEuYwKLkyGxo2E4Y+E+QIuLhK1TpMGMRNlOCPRfpOROU=",
            ),
            ("list_2sets.txt", "ECAjFDNIdKNLNQNRZUdZFaJadcNeQESOrRSTjTw="),
            (
                "list_uniques.txt",
                "EBAVmDGEeGGJWJOIKKaMOPIvqUaTOWFFw4cS/EShnFW6XamRm3mCvIA=",
            ),
            ("list_yzmir.txt", "EBAk3DNQrEPHVKmIvGLLHMPONZvTFcuZvVPWLYHaHZA="),
            ("test_extd_qty.txt", "EBAgTSZQ"),
            ("test_long_uniq.txt", "EBARFnwTSWfJw9Z8wOVn///A"),
            ("test_mana_orb.txt", "EBAg3CN8LhA="),
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
