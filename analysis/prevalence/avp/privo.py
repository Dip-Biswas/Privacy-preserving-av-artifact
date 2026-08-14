import re
from bs4 import BeautifulSoup
from . import Detector


class Privo(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # docs:
        #
        # https://developer.privo.com/introduction/environments.html

        privo_scripts = soup.find_all(
            "script", attrs={"src": re.compile(r"\.privo\.com", re.I)}
        )

        return {
            "scripts": len(privo_scripts) > 0,
            "subdomains": (
                "privohub-int.privo.com" in webpage
                or "api-gw-svc-int.privo.com" in webpage
                or "privohub.privo.com" in webpage
                or "api-gw-svc.privo.com" in webpage
                or "age-int.privo.com" in webpage
                or "age.privo.com" in webpage
                or "consent-int.privo.com" in webpage
                or "consent.privo.com" in webpage
                or ".privo.com" in webpage  # for cross-provider consistency
            ),
            "js_privolock": "PRIVOLOCK" in webpage,
            "js_ageverification": "privo.ageVerification" in webpage,
            "js_agegate": "privo.ageGate" in webpage,
            "js_ageestimation": "privo.ageEstimation" in webpage,
        }


def test_api_endpoint():
    script = """
        <script>
            const base = "https://privohub-int.privo.com";
        </script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(Privo.run_checks(script, soup))

    script = """
        <script>
            const base = "https://api-gw-svc-int.privo.com";
        </script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(Privo.run_checks(script, soup))


def test_privo_script():
    scripts = """
        <head>
            <title>Age Gate load Demo</title>
            <script src="https://age.privo.com/gate/privo.min.js"></script>
            <script>
                window.onload = async () => {
                privo.ageGate.init({
                    serviceIdentifier: "your_identifier",
                    displayMode: "redirect"
                });
                const response = await privo.ageGate.getStatus("user-identifier");
                console.log(response)
                }
            </script>
        </head>
    """
    soup = BeautifulSoup(scripts, "lxml")
    assert Detector.detect(Privo.run_checks(scripts, soup))


def test_privo_estimation_init():
    script = """
        <script>
            window.onload = async () => {
                privo.ageEstimation.init({
                    env: "prod",
                    serviceIdentifier: "your_identifier",
                });
            };
        </script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(Privo.run_checks(script, soup))
