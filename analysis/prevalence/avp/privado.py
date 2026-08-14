import re
from bs4 import BeautifulSoup
from . import Detector


class Privado(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://mobileidworld.com/topics/privado-id/
        return {
            "catchall": re.compile(r"\bprivado\b", re.I).search(webpage) is not None
        }
