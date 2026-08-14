from bs4 import BeautifulSoup
from . import Detector


class IdNow(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://www.idnow.io/
        # https://api.idcheck-sandbox.ariadnext.io/gw/cis/api/index.html
        # https://docs-autoident.idnow.io/?version=latest
        # https://docs-videoident.idnow.io/?version=latest
        # https://sdkweb.idcheck-sandbox.ariadnext.io/rest/api/index.html
        # https://www.identity.tm/res/uploads/dokumente/WebService-Customer.pdf

        domain_patterns = [
            ".ariadnext.io",
            ".idcheck.io",
            ".ariadnext.com",
            ".idnow.ae",
            ".online-ident.ch",
            ".idnow.de",
            ".identity.tm",
        ]

        were_subdomains_found = False
        for domain in domain_patterns:
            if domain in webpage:
                were_subdomains_found = True
                break

        return {"subdomains": were_subdomains_found}


def test_idnow_1():
    fixture = r"""
        <script>
            const thing = "https://api.idcheck-sandbox.ariadnext.io/auth/realms/customer-identity/protocol/openid-connect/token";
        </script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(IdNow.run_checks(fixture, soup))


def test_idnow_2():
    fixture = r"""
        <script>
            const thing = "https://gateway.idnow.de";
        </script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(IdNow.run_checks(fixture, soup))


def test_idnow_3():
    fixture = r"""
        <script>
            const thing = "https://gateway.online-ident.ch";
        </script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(IdNow.run_checks(fixture, soup))


def test_idnow_4():
    fixture = r"""
        <script>
            const thing = "https://gateway.idnow.ae";
        </script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(IdNow.run_checks(fixture, soup))


def test_idnow_5():
    fixture = r"""
        <script>
            const thing = "https://customer.identity.tm/api/2.10/getVideoFileBinaryAsync/OrderID";
        </script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(IdNow.run_checks(fixture, soup))
