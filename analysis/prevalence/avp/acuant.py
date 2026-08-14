import re
from bs4 import BeautifulSoup
from . import Detector


class Acuant(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://webui-da-na-id-verify.i.apps.experian.com/
        accuant_elems = soup.find_all(id=re.compile(r"^acuant-"))
        return {"elems": len(accuant_elems) > 0, "subdomains": ".acuant.com" in webpage}


def test_acuant():
    acuant_container = """
        <div id="app-id-proxy">
            <div id="acuant-camera" style="display: none;"></div>
            <div id="acuant-face-capture-container"></div>
        </div>
    """
    soup = BeautifulSoup(acuant_container, "lxml")
    assert Detector.detect(Acuant.run_checks(acuant_container, soup))
