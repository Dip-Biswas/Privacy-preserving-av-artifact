import re
from bs4 import BeautifulSoup
from . import Detector


class Veriff(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        veriff_scripts = soup.find_all(
            "script", attrs={"src": re.compile(r"\.veriff\.me")}
        )

        return {
            "scripts": len(veriff_scripts) > 0,
            "subdomains": ".veriff.com" in webpage or ".veriff.me" in webpage,
            "container_class": ".veriff_container" in webpage,
        }


def test_veriff_script():
    veriff_script = """
        <script data-n-head="1" src="https://cdn.veriff.me/incontext/js/v1/veriff.js"></script>
    """
    soup = BeautifulSoup(veriff_script, "lxml")
    assert Detector.detect(Veriff.run_checks(veriff_script, soup))


def test_veriff_css():
    veriff_css = """
        .veriff_container {
            text-align: center;
            font-family: proxima-soft, sans-serif !important;
            font-size: 16px !important;
            font-weight: 300;
        }
    """
    soup = BeautifulSoup(veriff_css, "lxml")
    assert Detector.detect(Veriff.run_checks(veriff_css, soup))


def test_veriff_blob():
    blob = """
        window.corona.globalTranslations.reactivation_veriff_doi = "\u003ch4 class=\"title\"\u003eVerifizierung erforderlich\u003c/h4\u003e\n\u003cp\u003e\n\t\u003cstrong\u003eUm Ihr Konto zu schützen, bestätigen Sie bitte Ihre Identität mit unserem sicheren Partner Veriff.\u003c/strong\u003e\n\u003c/p\u003e\n\u003cp\u003e\n\tMachen Sie bitte:\n\t\u003cbr\u003e\n\t\u003cul\u003e\n\t\t\u003cli\u003e\n\t\t\tein Selfie (ein Foto von Ihrem Gesicht) und\n\t\t\u003c/li\u003e\n\t\t\u003cli\u003e\n\t\t\tein Foto Ihres Ausweises (z. B. Führerschein, Reisepass oder Personalausweis).\n\t\t\u003c/li\u003e\n\t\u003c/ul\u003e\n\u003c/p\u003e\n\u003cp\u003e\n\tAnmerkung: Fotos von Ausweisen, die auf Bildschirmen (Telefon, Tablet, Computer usw.) gezeigt werden, werden nicht akzeptiert.\n\u003c/p\u003e\n\u003cbutton class=\"btn button buttonPrimary\" onclick=\"reactivation.verifyAccount();return false;\"\u003eVERIFIZIEREN UND FORTFAHREN\u003c/button\u003e\n\u003cp\u003e Veriff verwendet Ihre Daten nur zur Verifizierung \u003ca href=\"https://www.veriff.com/privacy-notice\" target=\"_blank\" aria-label=\"Datenschutzrichtlinie (wird in einem neuen Tab geöffnet)\"\u003e(Datenschutzrichtlinie)\u003c/a\u003e. Sie möchten sich nicht verifizieren? Kündigen Sie Ihre Mitgliedschaft \u003ca onclick=\"reactivation.areYouSure(); return false;\"\u003ehier\u003c/a\u003e.\n\u003c/p\u003e";
    """
    soup = BeautifulSoup(blob, "lxml")
    assert Detector.detect(Veriff.run_checks(blob, soup))
