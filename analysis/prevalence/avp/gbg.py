import re
from bs4 import BeautifulSoup
from . import Detector


class Gbg(Detector):
    def name() -> str:
        return "GBG"

    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # can't find any info on this
        # note that `./idology.py` is a GBG product
        return {
            "catchall": re.compile(r"\bgbg\.com\b", re.I).search(webpage) is not None
        }


def test_shot_in_the_dark():
    fixture = """
        <script src="https://gbg.com/foo/bar.js"></script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(Gbg.run_checks(fixture, soup))
