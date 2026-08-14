import re
from bs4 import BeautifulSoup
from . import Detector


class Authenteq(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        authenteq_elems = soup.find_all(class_=re.compile(r"AuthenteqButton", re.I))
        return {
            "button": len(authenteq_elems) > 0,
            "subdomains": ".authenteq.com" in webpage,
        }


def test_authenteq():
    button = """
    <a class="AuthenteqButton" href="<verificationUrl>">
        <img class="AuthenteqButton-logo" src="authenteq-logo.png" alt="Authenteq Logo" />
        <div class="AuthenteqButton-caption">Sign Up with Authenteq</div>
    </a>
    """
    soup = BeautifulSoup(button, "lxml")
    assert Detector.detect(Authenteq.run_checks(button, soup))
