import re
from bs4 import BeautifulSoup
from . import Detector


class VerifyMyAge(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        vma_img_tags = soup.find_all(
            "img", attrs={"src": re.compile(r"verifymyage\.co\.uk")}
        )
        vma_scripts = soup.find_all(
            "script", attrs={"src": re.compile(r"\.verifymyage\.com")}
        )
        vma_links = soup.find_all(
            "a", attrs={"href": re.compile(r"\.verifymyage\.com")}
        )

        vma_elems = soup.find_all(
            class_=re.compile(r"(-verifyMyAge|age-verification-vma-)")
        )

        return {
            "imgs": len(vma_img_tags) > 0,
            "scripts": len(vma_scripts) > 0,
            "links": len(vma_links) > 0,
            "elems": len(vma_elems) > 0,
            "agegate": "/agegate/verifymy" in webpage,
            "subdomains": (
                ".verifymyage.com" in webpage
                or ".verifymyage.co.uk" in webpage
                or ".verifymy.io" in webpage
            ),
        }


def test_verifymyage_a():
    fixture = r"""
        <a
            href="https://oauth.verifymyage.com/oauth/authorize?client_id=key-p-75ccf01e-1d04-4293-8a30-a1317bba7c1f&amp;country=us4&amp;scope=adult&amp;redirect_uri=https%3A%2F%2Fwww.thenude.com%2Fage-verification-callback.php"
            class="btn btn-default center-block"
            data--h-bstatus="0OBSERVED"
        >
        Alternative VerifyMyAge
        </a>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(VerifyMyAge.run_checks(fixture, soup))

    fixture = """
        <a class="age-verification-vma-link" href="https://backend.verifymyage.com/start/verification/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJoYXNoZWRfY2xpZW50X2lkIjoiNzAyMzU0YjRlYjlkNjg3MTAzY2RiMDljMzM3OWZlNTMwMTdlZmE0YWFhY2M3ZGNlMjYzMGEyMWVlOGE5NTY1YSIsInZlcmlmaWNhdGlvbl9pZCI6IjY4OWM3YTg1ODdiMGFmZmVlM2RhMTQwMSIsImNsaWVudF9pZCI6ImtleS1wLWMwMDFkOTA0LTlhOGItNDczZi1iZTc3LTRkYWRlYzgzMjM4MiIsImV4cCI6MTc1NTEwNzA0NX0.xn0wqzqJgzWvNJIhbz6nGaVkaXJzPrUXE4WDqB16QaQ" id="js_verify_age" target="_blank">
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(VerifyMyAge.run_checks(fixture, soup))


def test_verifymyage_div():
    fixture = r"""
            <div class="avp-config-content__option avp-config-content__option--verifyMyAge avp-config-option avp-config-option--selected" data--h-bstatus="0OBSERVED">
                <div class="avp-config-option__radio" data--h-bstatus="0OBSERVED"></div>
                <div class="avp-config-option__text" data--h-bstatus="0OBSERVED">VerifyMyAge</div>
                <div class="avp-config-option__image-wrp" data--h-bstatus="0OBSERVED">
                    <img src="https://assets.strpst.com/assets/activation/avp/components/AvpConfigContent/images/verifymyage.svg" alt="logo" class="avp-config-option__image" data--h-bstatus="0OBSERVED">
                </div>
            </div>
        """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(VerifyMyAge.run_checks(fixture, soup))

    fixture = '<div class="age-verification-vma-text">'
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(VerifyMyAge.run_checks(fixture, soup))


def test_agegate_verifymy():
    agegate_verifymy = """
        <script>
            const VERIFYMY_URL = "/agegate/verifymy/?key=key&method=verifymy_email";
        </script>
    """
    soup = BeautifulSoup(agegate_verifymy, "lxml")
    assert Detector.detect(VerifyMyAge.run_checks(agegate_verifymy, soup))
