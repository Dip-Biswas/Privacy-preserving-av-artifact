import re
from bs4 import BeautifulSoup
from . import Detector


class Aware(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://docs.knomi.aware.com/knomi_web/knomi_web/design.html
        #
        # they have dev docs but can't seem to find any fingerprintable info
        # couldn't find a demo or deployment either
        return {
            "catchall": re.compile(r"\bknomi\b|\bknomiweb", re.I).search(webpage)
            is not None,
            "js_identifiers": (
                "getCaptureParameter" in webpage
                or "GetAutocapturePayload" in webpage
                or "autocaptureVideoEncrypted" in webpage
                or "autocaptureDocumentEncrypted" in webpage
                or "GetAnalyzePayload" in webpage
                or "analyzeEncrypted" in webpage
                or "analyzeDocumentEncrypted" in webpage
            ),
            "subdomains": ".aware.com" in webpage,
        }


def test_knomi_script():
    script = '<script type="text/javascript" src="bin/KnomiWeb.js"></script>'
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(Aware.run_checks(script, soup))


def test_knomi_function():
    script = """
        <script>
            const payload = payloadObj.GetAnalyzePayload(cameraObj);
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: payload,
            })
            const results = await response.json();
        </script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(Aware.run_checks(script, soup))
