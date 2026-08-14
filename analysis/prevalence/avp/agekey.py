from bs4 import BeautifulSoup
from . import Detector


class AgeKey(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://agekey.org — Privacy-First Age Verification
        # No public SDK documentation or known live deployments found.
        # Lax domain matching only.

        return {
            "domain": "agekey.org" in webpage,
        }


def test_agekey_domain():
    fixture = '<a href="https://verify.agekey.org/start">Verify Age</a>'
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(AgeKey.run_checks(fixture, soup))
