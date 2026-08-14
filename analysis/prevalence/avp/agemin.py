from bs4 import BeautifulSoup
from . import Detector


class AgeMin(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://agemin.com — AI-Powered Identity Verification
        # No public SDK documentation or known live deployments found.
        # Lax domain matching only.

        return {
            "domain": "agemin.com" in webpage,
        }


def test_agemin_domain():
    fixture = '<script src="https://cdn.agemin.com/widget.js"></script>'
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(AgeMin.run_checks(fixture, soup))
