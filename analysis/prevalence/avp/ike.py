from bs4 import BeautifulSoup
from . import Detector


class Ike(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # not a lot of info; doesn't really target web AV
        return {"subdomains": ".iketech.com" in webpage}


def test_shot_in_the_dark():
    link = '<a href="https://www.iketech.com/foo">cta</a>'
    soup = BeautifulSoup(link, "lxml")
    assert Detector.detect(Ike.run_checks(link, soup))
