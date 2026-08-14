import re
from bs4 import BeautifulSoup
from . import Detector


class Regula(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://regulaforensics.com/
        # https://faceapi.regulaforensics.com/
        # https://docs.regulaforensics.com/develop/doc-reader-sdk/web-components/getting-started/installation/

        regula_scripts = soup.find_all(
            "script", attrs={"src": re.compile(r"/@regulaforensics/", re.I)}
        )
        document_reader_webcomponents = soup.find_all("document-reader")
        camera_snapshot_webcomponents = soup.find_all("camera-snapshot")
        face_liveness_webcomponents = soup.find_all("face-liveness")

        # some potential for false-positives
        liveness_elems = soup.find_all(class_=re.compile(r"^Liveness_", re.I))

        return {
            "scripts": len(regula_scripts) > 0,
            "document_reader_webcomponent": len(document_reader_webcomponents) > 0,
            "camera_snapshot_webcomponent": len(camera_snapshot_webcomponents) > 0,
            "liveness_elems": len(liveness_elems) > 0,
            "liveness_webcomponent": len(face_liveness_webcomponents) > 0,
            "js_sdk": "RegulaDocumentSDK" in webpage,
            "subdomains": ".regulaforensics.com" in webpage,
        }


def test_regula_script():
    script = """
        <script src="https://unpkg.com/@regulaforensics/vp-frontend-document-components@latest/dist/main.iife.js"></script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(Regula.run_checks(script, soup))


def test_webcomponents():
    component = "<document-reader></document-reader>"
    soup = BeautifulSoup(component, "lxml")
    assert Detector.detect(Regula.run_checks(component, soup))

    component = "<camera-snapshot></camera-snapshot>"
    soup = BeautifulSoup(component, "lxml")
    assert Detector.detect(Regula.run_checks(component, soup))

    component = "<face-liveness></face-liveness>"
    soup = BeautifulSoup(component, "lxml")
    assert Detector.detect(Regula.run_checks(component, soup))


def test_liveness_elems():
    elem = """
        <div class="Liveness_instruction__j2sX9"></div>
    """
    soup = BeautifulSoup(elem, "lxml")
    assert Detector.detect(Regula.run_checks(elem, soup))
