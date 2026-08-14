import re
from bs4 import BeautifulSoup
from . import Detector

# Gataca QR web components (github.com/gataca-io/gataca-QR):
# <gataca-qr>, <gataca-qrdisplay>, <gataca-qrws>, <gataca-ssibutton>
GATACA_COMPONENT = re.compile(r"<gataca-(?:qr|ssibutton)", re.I)


class Amie(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://www.amievouch.com — age verification by Gataca (gataca.io)
        # Demo at https://legalage.gataca.io/ (Amie-specific age verification portal)
        # Integration via OIDC redirect flow or embedded Gataca QR web components.
        # Web components from @gataca-io/gataca-qr npm package.

        return {
            "domain": "amievouch.com" in webpage,
            "legalage_portal": "legalage.gataca.io" in webpage,
            "gataca_webcomponent": GATACA_COMPONENT.search(webpage) is not None,
            "gataca_amie": "gataca.io" in webpage and "amie" in webpage.lower(),
        }


def test_amie_domain():
    fixture = """
        <a href="https://verify.amievouch.com/start?session=xyz">Verify your age</a>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(Amie.run_checks(fixture, soup))


def test_amie_legalage_portal():
    fixture = """
        <script>
            window.location.href = "https://legalage.gataca.io/?session=abc&callback=...";
        </script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(Amie.run_checks(fixture, soup))


def test_amie_web_component():
    fixture = """
        <gataca-qr
            callback-server="https://connect.gataca.io"
            qr-role="certify"
        ></gataca-qr>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(Amie.run_checks(fixture, soup))


def test_no_false_positive_gataca_alone():
    fixture = """
        <a href="https://gataca.io/products/wallet/">Download Gataca Wallet</a>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert not Detector.detect(Amie.run_checks(fixture, soup))
