import re
from bs4 import BeautifulSoup
from . import Detector


class Aristotle(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://integrity.aristotle.com/
        # https://integrity.aristotle.com/age-verification/
        # https://integrity.aristotle.com/compliance-verification/
        return {
            "identity.aristotle": re.compile(r"\bidentity\.aristotle\b").search(webpage)
            is not None,
            "subdomains": ".aristotle.com" in webpage,
        }


def test_aristotle_shot_in_the_dark():
    fixture = '<a href="https://identity.aristotle.com/foo">'
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(Aristotle.run_checks(fixture, soup))
