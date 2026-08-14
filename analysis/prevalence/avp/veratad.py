import re
from bs4 import BeautifulSoup
from . import Detector


class Veratad(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://veratad.com/
        # https://api.veratad.com/agematch/united-states

        dcams_links = soup.find_all(
            "link", attrs={"href": re.compile(r"\.dcams\.app\b", re.I)}
        )
        dcams_iframes = soup.find_all(
            "iframe", attrs={"src": re.compile(r"\.dcams\.app\b", re.I)}
        )

        idmax_button_containers = soup.find_all(id="idmax-button-container")

        return {
            "dcams_links": len(dcams_links) > 0,
            "dcams_iframes": len(dcams_iframes) > 0,
            "idmax_button_containers": len(idmax_button_containers) > 0,
            "veratad_frames": len(soup.find_all(id="veratad-frame")) > 0,
            "subdomains": ".idresponse.com" in webpage or ".dcams.app" in webpage,
            "js_modal": "veratad.modal" in webpage,
            "js_idmax": "window.IDMax" in webpage,
        }


def test_veratad_iframe_1():
    iframe_with_src = """
        <iframe
            src="https://fe.dcams.app/d2568a05-47a2-4ec7-b3e3-c5bd194461a7"
            width="420"
            height="670"
            style="overflow: hidden; border: none;"
            allow="camera"
            allowfullscreen
            <!-- Make sure to set the allow properly in case one of your verification components needs access -->
        ></iframe>
    """
    soup = BeautifulSoup(iframe_with_src, "lxml")
    assert Detector.detect(Veratad.run_checks(iframe_with_src, soup))


def test_veratad_iframe_2():
    iframe_with_id = """
        <iframe allow="camera" style="display:none;" id="veratad-frame" scrolling="no"></iframe>
    """
    soup = BeautifulSoup(iframe_with_id, "lxml")
    assert Detector.detect(Veratad.run_checks(iframe_with_id, soup))


def test_veratad_endpoints():
    idresponse_prod = """
        <script>
            const thing = "https://production.idresponse.com/process/comprehensive/gateway";
        </script>
    """
    soup = BeautifulSoup(idresponse_prod, "lxml")
    assert Detector.detect(Veratad.run_checks(idresponse_prod, soup))

    idresponse_documents = """
        <script>
            const thing = "https://docs.idresponse.com/process/comprehensive/gateway";
        </script>
    """
    soup = BeautifulSoup(idresponse_documents, "lxml")
    assert Detector.detect(Veratad.run_checks(idresponse_documents, soup))


def test_veratad_inline_script():
    vanilla_js = """
    <script>
        document.addEventListener("DOMContentLoaded", function () {
            if (window.IDMax && window.IDMax.ButtonCreator) {
                new window.IDMax.ButtonCreator({
                    targetElement: document.getElementById("idmax-button-container"),
                    providers: ["clear", "plaid"],
                    onInit: (provider) =>
                        console.log(`Button for ${provider} initialized`),
                    onComplete: (data) => console.log("Completed with data:", data),
                    onError: (error) => console.error("Error:", error),
                    onClose: () => console.log("User closed the interaction"),
                });
            }
        });
    </script>
    """
    soup = BeautifulSoup(vanilla_js, "lxml")
    assert Detector.detect(Veratad.run_checks(vanilla_js, soup))


def test_veratad_idmax_container():
    idmax_container = '<div id="idmax-button-container"></div>'
    soup = BeautifulSoup(idmax_container, "lxml")
    assert Detector.detect(Veratad.run_checks(idmax_container, soup))
