import re
from bs4 import BeautifulSoup
from . import Detector


class Incode(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://developer.incode.com/
        # https://developer.incode.com/docs/face-authentication
        # https://developer.incode.com/docs/releases-web-sdk

        incode_links = soup.find_all(
            "a", attrs={"href": re.compile(r"/agegate/incode", re.I)}
        )

        incode_images = soup.find_all(
            "img", attrs={"alt": "Incode"}, class_="incode-logo"
        )
        incode_inputs = soup.find_all("input", attrs={"value": "incode-id"})
        incode_labels = soup.find_all("label", attrs={"for": "choice-incode-id"})
        incode_containers = soup.find_all(id="incode-container")

        return {
            "links": len(incode_links) > 0,
            "images": len(incode_images) > 0,
            "inputs": len(incode_inputs) > 0,
            "labels": len(incode_labels) > 0,
            "containers": len(incode_containers) > 0,
            "agegate": "/agegate/incode" in webpage,
            "config_is_yoti_enabled": 'config.isIncodeAgeVerificationEnabled = "1"'
            in webpage,
            "subdomains": ".incode.com" in webpage,
        }


def test_incode_form():
    form = """
        <input type="radio" id="choice-incode-id" name="av-choice" value="incode-id" autocomplete="off">
        <label for="choice-incode-id">

            <img src="https://web.static.mmcdn.com/images/id-scan.svg" alt="ID">

            <span>ID Scan</span>
        </label>
    """
    soup = BeautifulSoup(form, "lxml")
    assert Detector.detect(Incode.run_checks(form, soup))


def test_incode_link():
    incode_link = """
        <a id="av-choice-submit" class="nooverlay" data-testid="age-gate-verify" href="/agegate/incode/?key=key&amp;method=incode">
    """
    soup = BeautifulSoup(incode_link, "lxml")
    assert Detector.detect(Incode.run_checks(incode_link, soup))


def test_script_incode_refs():
    script_incode_refs = """
        <script>
            const FACE_POST_URL = "/agegate/incode/?key=key&method=incode_est";
            const ID_POST_URL = "/agegate/incode/?key=key&method=incode";
        </script>
    """
    soup = BeautifulSoup(script_incode_refs, "lxml")
    assert Detector.detect(Incode.run_checks(script_incode_refs, soup))


def test_config_is_incode_enabled():
    # pattern used by some sites (presumably) operated by one particular company
    script = """
        <script>
            window.config.isYotiAgeVerificationEnabled = "1";
            window.config.isIncodeAgeVerificationEnabled = "1";
        </script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(Incode.run_checks(script, soup))
