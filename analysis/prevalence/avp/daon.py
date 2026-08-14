from bs4 import BeautifulSoup
from . import Detector


class Daon(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://www.daon.com/
        # hard to find documentation or demos
        return {"domain": "daon.com" in webpage}


def test_shot_in_the_dark():
    fixture = """
        <script src="https://www.daon.com/foo/bar.js"></script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(Daon.run_checks(fixture, soup))
