import datetime
import random
import string
import time


class Gen:

    @staticmethod
    def generate_text(length: int, lang="eng") -> str:
        if lang == "rus":
            cyrillic = "ёйцукенгшщзхъфывапролджэячсмитьбю "
            return ''.join(random.choices(cyrillic, k=length)).replace(' ', '')
        if lang == "eng":
            return ''.join(random.choices(string.ascii_lowercase + " ", k=length)).replace(' ', '')

    @staticmethod
    def generate_title_with_datetime(title: str):
        return f"{title} test : {datetime.datetime.now()}, {Gen.generate_text(7)}"
