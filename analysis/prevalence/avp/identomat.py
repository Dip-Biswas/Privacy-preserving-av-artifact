import re
from bs4 import BeautifulSoup
from . import Detector


class Identomat(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://www.identomat.com/about-us
        # don't seem to have actual web stuff yet?
        return {
            "catchall": re.compile(r"\bidentomat\b", re.I).search(webpage) is not None
        }


def test_shot_in_the_dark():
    fixture = """
        <script src="https://www.identomat.com/foo/bar.js"></script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(Identomat.run_checks(fixture, soup))
