import re
from bs4 import BeautifulSoup
from . import Detector


class Onfido(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # aka [something else]
        # https://documentation.onfido.com/api/
        return {
            "subdomains": (
                re.compile(r"\bapi(\.(eu|us|ca))?\.onfido\.com").search(webpage)
                is not None
                or ".onfido.com" in webpage
            )
        }


def test_api_endpoint():
    endpoint = """
        <script>
            const endpoint = "https://api.eu.onfido.com/v3.6/repeat_attempts/match";
        </script>
    """
    soup = BeautifulSoup(endpoint, "lxml")
    assert Detector.detect(Onfido.run_checks(endpoint, soup))
