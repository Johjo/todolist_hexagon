class TextFilter:
    def __init__(self, included_words: tuple[str, ...], excluded_words: tuple[str, ...]):
        self._included_words = included_words
        self._excluded_words = excluded_words

    def include(self, text: str) -> bool:
        if not self.match_included_words(text):
            return False

        if self.match_excluded_words(text):
            return False

        return True

    def match_included_words(self, text: str) -> bool:
        if self._included_words == ():
            return True

        for included_word in self._included_words:
            if any(included_word == word for word in text.split()):
                return True
        return False

    def match_excluded_words(self, text: str) -> bool:
        for excluded_word in self._excluded_words:
            if any(excluded_word == word for word in text.split()):
                return True
        return False

