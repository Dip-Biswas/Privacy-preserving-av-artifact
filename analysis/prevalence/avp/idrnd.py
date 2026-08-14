import re
from bs4 import BeautifulSoup
from . import Detector


class IdRnd(Detector):
    def name() -> str:
        return "ID RnD"

    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://www.idrnd.ai/ | https://docs.idrnd.net/ | https://www.miteksystems.com/idrnd-mitek
        #
        # can't find this
        return {
            "catchall": re.compile(r"\bidrnd|ID R(&|&amp;)D\b", re.I).search(webpage)
            is not None
        }


def test_idrnd_shot_in_the_dark():
    fixture = '<a href="https://idrnd.ai/foo"></a>'
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(IdRnd.run_checks(fixture, soup))

    fixture = '<a href="https://example.com">id r&amp;d</a>'
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(IdRnd.run_checks(fixture, soup))
