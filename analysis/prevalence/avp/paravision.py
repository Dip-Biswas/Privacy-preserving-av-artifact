import re
from bs4 import BeautifulSoup
from . import Detector


class Paravision(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://www.paravision.ai/product/age-estimation/
        # https://www.paravision.ai/liveness/
        # https://www.paravision.ai/partners/
        #
        # they don't seem to have any web-focused products
        return {
            "catchall": re.compile(r"\bparavision\b").search(webpage) is not None,
            "subdomains": ".paravision.ai" in webpage,
        }


def test_shot_in_the_dark():
    script = """
        <script>
            const url = "https://foo.paravision.ai/bar";
        </script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(Paravision.run_checks(script, soup))
