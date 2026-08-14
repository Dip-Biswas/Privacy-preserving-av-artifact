from bs4 import BeautifulSoup
from . import Detector


class EarthId(Detector):
    def name() -> str:
        return "EarthID"

    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # not a lot of info
        return {"subdomains": ".myearth.id" in webpage}


def test_shot_in_the_dark():
    link = '<a href="https://www.myearth.id/foo">cta</a>'
    soup = BeautifulSoup(link, "lxml")
    assert Detector.detect(EarthId.run_checks(link, soup))
