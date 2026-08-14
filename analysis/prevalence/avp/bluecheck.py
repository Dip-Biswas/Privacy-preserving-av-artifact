from bs4 import BeautifulSoup
from . import Detector


class BlueCheck(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        return {
            "subdomains": ".bluecheck.me" in webpage,
        }


def test_bluecheck():
    fixture = r"""
       <script src="https://verify.bluecheck.me/platforms/lightspeed/js/AgeVerification.js?domain_token=YOUR_DOMAIN_TOKEN_HERE"></script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(BlueCheck.run_checks(fixture, soup))
