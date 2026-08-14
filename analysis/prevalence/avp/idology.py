import re
from bs4 import BeautifulSoup
from . import Detector


class Idology(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://www.gbg.com/en-us/gbg-idology/
        idology_id_elems = soup.find_all(id=re.compile(r"^idology-"))
        idology_class_elems = soup.find_all(class_=re.compile(r"-idology$"))

        return {
            "id_elems": len(idology_id_elems) > 0,
            "class_elems": len(idology_class_elems) > 0,
            "container_id": "#idology-container" in webpage,
            "iframe_class": ".iframe-idology" in webpage,
        }


def test_idology_elems():
    idology_container = '<div id="idology-container"></div>'
    soup = BeautifulSoup(idology_container, "lxml")
    assert Detector.detect(Idology.run_checks(idology_container, soup))

    idology_iframe = (
        '<iframe class="iframe-idology" src="https://example.com"></iframe>'
    )
    soup = BeautifulSoup(idology_iframe, "lxml")
    assert Detector.detect(Idology.run_checks(idology_iframe, soup))


def test_idology_css():
    idology_container_css = """
        #idology-container .step-title::after {
          content: "Age Check";
          text-indent: 0;
          display: block;
          line-height: initial;
        }
    """
    soup = BeautifulSoup(idology_container_css, "lxml")
    assert Detector.detect(Idology.run_checks(idology_container_css, soup))

    idology_iframe_css = """
        .iframe-idology{max-width:700px;margin:auto}
        .iframe-idology .modal-content .modal-body{background:#fff}
    """
    soup = BeautifulSoup(idology_iframe_css, "lxml")
    assert Detector.detect(Idology.run_checks(idology_iframe_css, soup))
