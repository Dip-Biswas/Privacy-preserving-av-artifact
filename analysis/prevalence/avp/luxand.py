from bs4 import BeautifulSoup
from . import Detector


class Luxand(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://luxand.cloud — cloud face recognition / age estimation API
        # API access via dashboard.luxand.cloud; purely server-side REST API.
        # No embedded widget or client-side SDK found in public docs.
        # Note: luxand.com is a separate on-premises desktop SDK product.
        # Data source: marketing site only — lax domain matching.

        return {
            "domain": "luxand.cloud" in webpage,
        }


def test_luxand_api_ref():
    fixture = """
        <script>
            const LUXAND_API = "https://api.luxand.cloud/photo/age";
        </script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(Luxand.run_checks(fixture, soup))


def test_no_false_positive_luxand_com():
    fixture = '<a href="https://luxand.com/facesdk/">FaceSDK</a>'
    soup = BeautifulSoup(fixture, "lxml")
    assert not Detector.detect(Luxand.run_checks(fixture, soup))
