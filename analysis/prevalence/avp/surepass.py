from bs4 import BeautifulSoup
from . import Detector


class SurePassIo(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://surepass.io/ (not to be confused with https://surepass.com/)
        # not a lot of info, doesn't seem to target the AV market. mostly kyc.
        return {"subdomains": ".surepass.io" in webpage}


def test_shot_in_the_dark():
    link = """
        <a href="https://api.surepass.io/foo/bar">cta</a>
    """
    soup = BeautifulSoup(link, "lxml")
    assert Detector.detect(SurePassIo.run_checks(link, soup))
