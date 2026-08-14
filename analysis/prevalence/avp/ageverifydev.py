from bs4 import BeautifulSoup
from . import Detector


class AgeVerifyDev(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://ageverify.dev
        # Site has TLS certificate issues; no public documentation found.
        # Lax domain matching only.

        return {
            "domain": "ageverify.dev" in webpage,
        }


def test_ageverifydev_domain():
    fixture = '<script src="https://cdn.ageverify.dev/v1/avd.js"></script>'
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(AgeVerifyDev.run_checks(fixture, soup))
