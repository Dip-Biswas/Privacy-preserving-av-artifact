import re
from bs4 import BeautifulSoup
from . import Detector


class Idemia(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://www.idemia.com/usa
        # https://www.idemia.com/verify-identity-and-eligibility
        #
        # unclear if they have web av/id stuff. some copy seems to suggest that they do,
        # but I can't find a page about it.
        return {"catchall": re.compile(r"\bidemia\b", re.I).search(webpage) is not None}


def test_shot_in_the_dark():
    link = """
        <a href="https://www.idemia.com/foo/bar">cta</a>
    """
    soup = BeautifulSoup(link, "lxml")
    assert Detector.detect(Idemia.run_checks(link, soup))
