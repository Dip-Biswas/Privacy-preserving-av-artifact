import re
from bs4 import BeautifulSoup
from . import Detector


class Trustmatic(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://trustmatic.com/
        # https://demo.trustmatic.io/documentation/
        # https://demo.trustmatic.io/login
        return {
            "catchall": re.compile(r"\btrustmatic\b").search(webpage) is not None,
            "subdomains": ".trustmatic.com" in webpage or ".trustmatic.io" in webpage,
        }


def test_shot_in_the_dark():
    link = """
        <a href="https://www.trustmatic.io/foo/bar">cta</a>
    """
    soup = BeautifulSoup(link, "lxml")
    assert Detector.detect(Trustmatic.run_checks(link, soup))
