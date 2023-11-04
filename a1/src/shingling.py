class Shingling:
    def __init__(self, k: int) -> None:
        """
        Constructor of Shingling.
        :param k: Length of a single shingle.
        """

        self._k = k

    def get_shingling_set(self, text: str) -> set:
        """
        Get a set of hashed singles from given text.
        :param text: Text.
        :return: A set of hased singles.
        """

        shingling_set = set()
        for i in range(len(text) - self._k + 1):
            text_part = text[i:i + self._k]
            if text_part.isspace():
                continue
            hash_result = self.shingling_hash(text_part)
            shingling_set.add(hash_result)
        return shingling_set

    @staticmethod
    def shingling_hash(text_part) -> int:
        """
        Hash a shingle. (0 -> 10e9 + 7)
        :param text_part: A shingle.
        :return: Hash of the shingle.
        """

        raw_hash = hash(text_part)
        return raw_hash % (10 ** 9 + 7)
