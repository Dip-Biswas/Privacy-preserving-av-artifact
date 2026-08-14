import re
from bs4 import BeautifulSoup
from . import Detector


class Mitek(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://www.miteksystems.com/
        # https://www.miteksystems.com/use-cases/age-verification
        #
        # associated with `./idrnd.py`
        # Original word-boundary placement (\bmitek without trailing \b) matched
        # "mitekuru" (Japanese text) and "mitek" as a casino game-provider name in
        # JSON catalogs. Requiring a domain suffix ties the match to real SDK refs.
        return {
            "catchall": re.compile(r"mitek(?:systems)?\.com", re.I).search(webpage)
            is not None
        }


def test_shot_in_the_dark():
    link = """
        <a href="https://www.miteksystems.com/foo/bar/do/stuff">cta</a>
    """
    soup = BeautifulSoup(link, "lxml")
    assert Detector.detect(Mitek.run_checks(link, soup))
