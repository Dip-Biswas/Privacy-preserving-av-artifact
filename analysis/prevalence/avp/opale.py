import re
from bs4 import BeautifulSoup
from . import Detector


class Opale(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://docs.opale.io/technical-integration
        # https://demo.opale.io/
        opale_scripts = soup.find_all(
            "script", attrs={"src": re.compile(r"\.opale\.io", re.I)}
        )
        opale_id_elems = soup.find_all(id=re.compile(r"^opale-"))
        agekey_id_elems = soup.find_all(id=re.compile(r"^agekey-"))

        return {
            "opale_scripts": len(opale_scripts) > 0,
            "opale_id_elems": len(opale_id_elems) > 0,
            "agekey_id_elems": len(agekey_id_elems) > 0,
            "subdomains": (
                ".opale.io" in webpage
                or "api.agekey.org" in webpage
                or "auth.agekey.org" in webpage in webpage
                or ".agekey.org" in webpage
                or "widget.opale.io" in webpage
            ),
            "js_fragment_use_signature": "useOpaleSignature" in webpage,
            "js_fragment_pubkey": "OPALE_PUBLIC_KEY" in webpage,
            "js_fragment_popup": "ageKeyPopup" in webpage,
        }


def test_opale_script():
    script = """
        <script src="https://widget.opale.io/dist/1.js" async=""></script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(Opale.run_checks(script, soup))


def test_opale_id_elem():
    elem = """
        <div id="opale-modal-container" style="display: flex;">
            <div id="opale-modal-content" style="transform: scale(1);"></div>
        </div>
    """
    soup = BeautifulSoup(elem, "lxml")
    assert Detector.detect(Opale.run_checks(elem, soup))


def test_agekey_id_elem():
    elem = """
        <button id="agekey-button" style="display: none;">
            <svg width="20" height="20" viewBox="0 0 256 272" fill="green" xmlns="http://www.w3.org/2000/svg" id="agekey-icon"></svg>
            <span id="agekey-text">AgeKey</span>
            <span id="loader-agekey" class="loader"></span>
        </button>
    """
    soup = BeautifulSoup(elem, "lxml")
    assert Detector.detect(Opale.run_checks(elem, soup))


def test_auth_redirect():
    link = """
        <a href="https://auth.agekey.org/?sessionId=sessionId&publicKey=publicKey&language=fr">auth redirect</a>
    """
    soup = BeautifulSoup(link, "lxml")
    assert Detector.detect(Opale.run_checks(link, soup))


def test_popup():
    script = """
        <script>
            const publicKey = "YOUR_PUBLIC_KEY";
            const sessionId = crypto.randomUUID(); // or your own session ID
            const state = {
            ageThreshold: 18,
            verificationMethod: "ageEstimation"
            };
            const stateEncrypted = await encryptState(state); // Encrypt state in your backend using shared signing secret

            const url = `https://auth.agekey.org/pop/register/?sessionId=${sessionId}&publicKey=${publicKey}&stateEncrypted=${stateEncrypted}`;

            // ...
        </script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(Opale.run_checks(script, soup))
