import re
from bs4 import BeautifulSoup
from . import Detector


class Socure(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        socure_scripts = soup.find_all(
            "script", attrs={"src": re.compile(r"socure\.(com|io)")}
        )
        socure_preloads = soup.find_all("link", attrs={"href": re.compile(r"/socure")})

        return {
            "berbix_subdomains": ".berbix.com" in webpage,
            "berbix_catchall": "berbix" in webpage,
            "socure_subdomains": ".socure.com" in webpage or ".socure.io" in webpage,
            "socure_scripts": len(socure_scripts) > 0,
            "socure_link_elems": len(socure_preloads) > 0,
            "js_socure_sdk_key": "socureSdkKey" in webpage,
        }


def test_socure_script():
    script = """
        <script src="https://websdk.socure.com/bundle.js"></script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(Socure.run_checks(script, soup))

    script = """
        <script src="https://sdk.dv.socure.io/latest/device-risk-sdk.js" data-public-key="redacted"></script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(Socure.run_checks(script, soup))


def test_socure_preload():
    third_party_preload = """
        <link rel="modulepreload" crossorigin="" href="/assets/socure-fBwydOsh.js">
    """
    soup = BeautifulSoup(third_party_preload, "lxml")
    assert Detector.detect(Socure.run_checks(third_party_preload, soup))
