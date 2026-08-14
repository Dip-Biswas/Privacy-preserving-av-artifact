import re
from bs4 import BeautifulSoup
from . import Detector


class Scytales(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://www.scytales.com/
        return {
            "catchall": re.compile(r"\bscytales\b", re.I).search(webpage) is not None
        }


def test_shot_in_the_dark():
    link = """
        <a href="https://www.scytales.com/foo/bar">cta</a>
    """
    soup = BeautifulSoup(link, "lxml")
    assert Detector.detect(Scytales.run_checks(link, soup))
