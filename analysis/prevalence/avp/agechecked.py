import re
from bs4 import BeautifulSoup
from . import Detector


class AgeChecked(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # observed:
        # https://agechecked.verifico.io
        # https://unity.agechecked.com

        agechecked_scripts = soup.find_all(
            "script", attrs={"src": re.compile(r".+\.(verifico\.io|agechecked\.com).+")}
        )

        agechecked_link_tags = soup.find_all(
            "link", attrs={"href": re.compile(r".+\.(verifico\.io|agechecked\.com).+")}
        )

        return {
            "scripts": len(agechecked_scripts) > 0,
            "link_tags": len(agechecked_link_tags) > 0,
            "verifico_subdomains": ".verifico.io" in webpage,
            "agechecked_subdomains": ".agechecked.com" in webpage,
        }


def test_agechecked_script():
    agechecked_script = """
        <script src="https://unity.agechecked.com/tr/?domain=example.com" async="">
    """
    soup = BeautifulSoup(agechecked_script, "lxml")
    assert Detector.detect(AgeChecked.run_checks(agechecked_script, soup))


def test_agechecked_link_tags():
    agechecked_stylsheet = """
        <link type="text/css" rel="stylesheet" href="https://agechecked.verifico.io/css/tracking.css">
    """
    soup = BeautifulSoup(agechecked_stylsheet, "lxml")
    assert Detector.detect(AgeChecked.run_checks(agechecked_stylsheet, soup))
