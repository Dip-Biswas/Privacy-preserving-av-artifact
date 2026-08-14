import re
from bs4 import BeautifulSoup
from . import Detector


class Shufti(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://shuftipro.com/document-verification/
        # https://shuftipro.com/age-verification/
        #
        # no public docs or demo
        return {
            "catchall": re.compile(r"\bshufti(pro)?\b").search(webpage) is not None,
            "subdomains": ".shuftipro.com" in webpage,
        }


def test_shot_in_the_dark():
    script = """
        <script src="https://shuftipro.com/foo/bar.js"></script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(Shufti.run_checks(script, soup))
