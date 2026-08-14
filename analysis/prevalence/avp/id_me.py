import re
from bs4 import BeautifulSoup
from . import Detector


class IdMe(Detector):
    def name() -> str:
        return "ID.me"

    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://id.me/
        # demo: https://0t3e4.csb.app/
        id_me_scripts = soup.find_all("script", attrs={"src": re.compile(r"/idme/")})

        id_me_links = soup.find_all(
            "a", attrs={"href": re.compile(r".*groups\.id\.me/", re.I)}
        )

        # https://github.com/IDme/javascript-sample-code/blob/AWE-17422/idme.js
        id_me_verification_elems = soup.find_all(id="idme-verification")

        id_me_button_elems = soup.find_all("a", id="idme-button")

        return {
            "scripts": len(id_me_scripts) > 0,
            "links": len(id_me_links) > 0,
            "general_elems": (
                len(id_me_verification_elems) > 0 or len(id_me_button_elems) > 0
            ),
            # Require word boundary after "me" so ".id.message" in JS variables
            # (e.g. GLOBAL.locale.id.message on Russian sites) does not match.
            "subdomains": re.compile(r"\.id\.me\b", re.I).search(webpage) is not None,
        }


def test_id_me_script():
    example = """
        <script src="https://s3.amazonaws.com/idme/developer/idme-buttons-2.0.1/assets/js/idme-modal.min.js" type="text/javascript"></script>
    """
    soup = BeautifulSoup(example, "lxml")
    assert Detector.detect(IdMe.run_checks(example, soup))


def test_id_me_link():
    example = """
        <a id="idme-button" href="https://groups.id.me?client_id=REDACTED&amp;redirect_uri=https://0t3e4.csb.app/callback&amp;response_type=token&amp;scopes=identity,military_us,responder_us,student_us,teacher_us,government_us,alumni,medical,nurse,employee,senior,military_canada,responder_canada,student_canada,teacher_canada,government_canada,nurse_canada,hospital_employee,kba_replacement/covid/verify,kba_replacement/covid/questionnaire"><img class="responsive-img" src="https://s3.amazonaws.com/idme/buttons/v4/verify-with-idme-green.png" alt="Verify with ID.me"></a>
    """
    soup = BeautifulSoup(example, "lxml")
    assert Detector.detect(IdMe.run_checks(example, soup))
