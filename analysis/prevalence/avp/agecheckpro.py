import re
from bs4 import BeautifulSoup
from . import Detector


class AgeCheckPro(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://agecheck.pro
        # npm: @agecheckpro/sdk  import { agecheck } from '@agecheckpro/sdk'
        # REST API: https://api.agecheck.pro/v1/verify
        # JS init: new agecheck({ apiKey })
        # Response: result.ageVerified

        agecheckpro_scripts = soup.find_all(
            "script", attrs={"src": re.compile(r"\.agecheck\.pro", re.I)}
        )

        return {
            "scripts": len(agecheckpro_scripts) > 0,
            "subdomains": ".agecheck.pro" in webpage,
            "npm_sdk": "@agecheckpro/sdk" in webpage,
            "js_init": "new agecheck(" in webpage,
            "api_endpoint": "api.agecheck.pro" in webpage,
        }


def test_agecheckpro_npm():
    fixture = """
        <script type="module">
            import { agecheck } from '@agecheckpro/sdk';
            const client = new agecheck({ apiKey: 'ak_live_...' });
            const result = await client.verify({ method: 'face_ai' });
        </script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(AgeCheckPro.run_checks(fixture, soup))


def test_agecheckpro_api():
    fixture = """
        <script>
            const res = await fetch('https://api.agecheck.pro/v1/verify', {
                method: 'POST',
                headers: { 'Authorization': 'Bearer ak_live_...' }
            });
        </script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(AgeCheckPro.run_checks(fixture, soup))
