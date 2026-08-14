import re
from bs4 import BeautifulSoup
from . import Detector


class AgeGo(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        agego_scripts = soup.find_all(
            "script", attrs={"src": re.compile(r".+?\.agego\.com.+?")}
        )

        return {
            "scripts": len(agego_scripts) > 0,
            "subdomains": "myapi.agego.com" in webpage or ".agego.com" in webpage,
        }


def test_agego_noscript():
    agego_noscript = """
        <noscript>
            <meta http-equiv="refresh" content="0; url=https://myapi.agego.com/noJS" />
        </noscript>
    """
    soup = BeautifulSoup(agego_noscript, "lxml")
    assert Detector.detect(AgeGo.run_checks(agego_noscript, soup))


def test_agego_script():
    agego_script_tag = """
        <!-- Age verification -->
        <script src="https://verifycdn.agego.com/v1/verify.js"></script>
    """
    soup = BeautifulSoup(agego_script_tag, "lxml")
    assert Detector.detect(AgeGo.run_checks(agego_script_tag, soup))
