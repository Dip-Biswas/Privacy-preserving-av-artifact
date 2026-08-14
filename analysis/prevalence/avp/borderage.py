from bs4 import BeautifulSoup
from . import Detector


class BorderAge(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://borderage.com/
        # hard to find documentation or demos
        return {"domain": "borderage.com" in webpage or "needemand.com" in webpage}


def test_shot_in_the_dark():
    fixture = '<a href="https://something.borderage.com/foo"></a>'
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(BorderAge.run_checks(fixture, soup))

    fixture = '<a href="https://something.needemand.com/foo"></a>'
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(BorderAge.run_checks(fixture, soup))
