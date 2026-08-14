from bs4 import BeautifulSoup
from . import Detector


class Roc(Detector):
    def name() -> str:
        return "ROC"

    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        return {"subdomains": ".roc.ai" in webpage, "domain": "://roc.ai" in webpage}


def test_shot_in_the_dark():
    script = """
        <script src="https://roc.ai/sdk/foo/bar.js"></script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(Roc.run_checks(script, soup))
