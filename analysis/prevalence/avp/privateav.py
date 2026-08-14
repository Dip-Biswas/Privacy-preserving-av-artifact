from bs4 import BeautifulSoup
from . import Detector


class PrivateAV(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://privateav.com — age verification with JS SDK and Sessions API
        # Subdomains: portal.privateav.com, docs.privateav.com, demo.privateav.com
        # SDK details not publicly documented; lax domain matching.

        return {
            "subdomains": ".privateav.com" in webpage,
        }


def test_privateav_portal_link():
    fixture = """
        <a href="https://portal.privateav.com/login">Sign in to verify</a>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(PrivateAV.run_checks(fixture, soup))


def test_privateav_sdk_ref():
    fixture = """
        <script src="https://cdn.privateav.com/sdk/v1/pav.min.js"></script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(PrivateAV.run_checks(fixture, soup))
