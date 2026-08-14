import re
from bs4 import BeautifulSoup
from . import Detector


class Didit(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://didit.me / https://docs.didit.me
        # Hosted verification UI: verify.didit.me
        # Sessions API: verification.didit.me
        # Auth: apx.didit.me
        # Web SDK npm: @didit-protocol/sdk-web

        didit_iframes = soup.find_all(
            "iframe", attrs={"src": re.compile(r"\.didit\.me", re.I)}
        )
        didit_scripts = soup.find_all(
            "script", attrs={"src": re.compile(r"\.didit\.me", re.I)}
        )

        return {
            "iframes": len(didit_iframes) > 0,
            "scripts": len(didit_scripts) > 0,
            "subdomains": ".didit.me" in webpage,
            "npm_sdk": "@didit-protocol/" in webpage,
        }


def test_didit_hosted_session():
    fixture = """
        <iframe src="https://verify.didit.me/session/abc123"></iframe>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(Didit.run_checks(fixture, soup))


def test_didit_sdk():
    fixture = """
        <script>
            import { DiditSDK } from "@didit-protocol/sdk-web";
            const client = new DiditSDK({ clientId: "..." });
        </script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(Didit.run_checks(fixture, soup))


def test_didit_api_ref():
    fixture = """
        <script>
            const response = await fetch("https://verification.didit.me/v3/session/", {
                method: "POST",
                headers: { "x-api-key": "..." }
            });
        </script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(Didit.run_checks(fixture, soup))
