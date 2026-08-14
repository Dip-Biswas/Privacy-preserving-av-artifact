import re
from bs4 import BeautifulSoup
from . import Detector


class AirisIdent(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://airisident.com — age estimation API by Irisnet (irisnet.de)
        # GitHub org: github.com/irisnet-ai
        # WordPress plugin: irisnet-api-client
        # REST API: api.irisnet.de (www.irisnet.de/api/ redirects there)
        # API clients exist for Java, Python, PHP, JS

        wp_plugin_scripts = soup.find_all(
            "script", attrs={"src": re.compile(r"/wp-content/plugins/irisnet", re.I)}
        )
        wp_plugin_links = soup.find_all(
            "link", attrs={"href": re.compile(r"/wp-content/plugins/irisnet", re.I)}
        )

        return {
            "wordpress_plugin": (
                len(wp_plugin_scripts) > 0
                or len(wp_plugin_links) > 0
                or "/wp-content/plugins/irisnet" in webpage
            ),
            "api_domain": "api.irisnet.de" in webpage,
            "domain_airisident": "airisident.com" in webpage,
            "domain_irisnet": "irisnet.de" in webpage or "irisnet-ai" in webpage,
        }


def test_airisident_wordpress():
    fixture = """
        <script src="/wp-content/plugins/irisnet-api-client/public/js/irisnet.min.js"></script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(AirisIdent.run_checks(fixture, soup))


def test_airisident_api_domain():
    fixture = """
        <script>
            const response = await fetch("https://api.irisnet.de/v2/age-estimation", {
                headers: { "licenseKey": "..." }
            });
        </script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(AirisIdent.run_checks(fixture, soup))


def test_airisident_domain():
    fixture = """
        <script>
            const endpoint = "https://airisident.com/age-estimation";
        </script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(AirisIdent.run_checks(fixture, soup))
