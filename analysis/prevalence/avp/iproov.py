from bs4 import BeautifulSoup
from . import Detector


class IProov(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://www.iproov.com/

        iproov_me_elems = soup.find_all("iproov-me")

        return {
            "me_elem": len(iproov_me_elems) > 0,
            "template_elem": len(soup.find_all(id="iproov_template")) > 0,
            "heading_elem": len(soup.find_all(class_="iproov-lang-heading")) > 0,
            "subdomains": ".iproov.app" in webpage or ".iproov.me" in webpage,
            "js_fragment": "IProov" in webpage,
        }


def test_iproov():
    fixture = r"""
        <iproov-me token="***YOUR_TOKEN_HERE***">
            <div slot="ready">
                <h1 class="iproov-lang-heading">Ready to iProov</h1>
            </div>
            <div slot="button">
                <button type="button">Scan Face</button>
            </div>
        </iproov-me>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(IProov.run_checks(fixture, soup))
