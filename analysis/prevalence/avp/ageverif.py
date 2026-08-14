import re
from bs4 import BeautifulSoup
from . import Detector


class AgeVerif(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # observed:
        # https://www.ageverif.com/checker.js

        ageverif_scripts = soup.find_all(
            "script", attrs={"src": re.compile(r".+\.ageverif\.com.+")}
        )

        ageverif_imgs = soup.find_all(
            "img", attrs={"src": re.compile(r".+\.ageverif\.com.+")}
        )

        return {
            "scripts": len(ageverif_scripts) > 0,
            "imgs": len(ageverif_imgs) > 0,
            "subdomains": ".ageverif.com" in webpage,
        }


def test_ageverif_script():
    ageverif_script = """
        <head>
            <!-- Load AgeVerif Checker -->
            <script src="https://www.ageverif.com/checker.js?key=redacted"></script>
        </head>
    """
    soup = BeautifulSoup(ageverif_script, "lxml")
    assert Detector.detect(AgeVerif.run_checks(ageverif_script, soup))


def test_ageverif_img():
    ageverif_img = """
        <img src="https://checker.ageverif.com/assets/logos/ageverif-full.svg" style="display: inline-block; height: 32px; margin-bottom: 16px;">
    """
    soup = BeautifulSoup(ageverif_img, "lxml")
    assert Detector.detect(AgeVerif.run_checks(ageverif_img, soup))
