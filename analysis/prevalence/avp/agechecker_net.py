import re
from bs4 import BeautifulSoup
from . import Detector


class AgeCheckerNet(Detector):
    def name() -> str:
        return "AgeChecker.net"

    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://agechecker.net/demo
        #
        # also has a click-through "age gate" that we need to be careful to avoid catching
        # so we can't tack on the usual naive domain string search
        #
        # https://agechecker.net/age-gate/create
        agechecker_class_elems = soup.find_all(class_=re.compile(r"^agechecker_"))
        agechecker_scripts = soup.find_all(
            "script", attrs={"src": re.compile(r"agechecker\.net/static/popup/")}
        )
        return {
            "class_elems": len(agechecker_class_elems) > 0,
            "scripts": len(agechecker_scripts) > 0,
        }


def test_agechecker_popup_script():
    script = """
        <script src="https://cdn.agechecker.net/static/popup/v1/popup.js" crossorigin="anonymous"></script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(AgeCheckerNet.run_checks(script, soup))


def test_agegate_script():
    script = """
        <script src="https://cdn.agechecker.net/static/age-gate/v1/age-gate.js"></script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert not Detector.detect(AgeCheckerNet.run_checks(script, soup))


def test_agechecker_elem():
    button = """
        <button class="green agechecker_1273" id="submit">
            <span>Verify Age &amp; Complete Order</span>
        </button>
    """
    soup = BeautifulSoup(button, "lxml")
    assert Detector.detect(AgeCheckerNet.run_checks(button, soup))


def test_agegate():
    agegate = """
        <div id="age-gate-parent">
            <div id="agechecker-age-gate" style="position: absolute; z-index: 0; opacity: 1;">
            </div>
        </div>
    """
    soup = BeautifulSoup(agegate, "lxml")
    assert not Detector.detect(AgeCheckerNet.run_checks(agegate, soup))
