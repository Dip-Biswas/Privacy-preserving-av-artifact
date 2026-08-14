import re
from bs4 import BeautifulSoup
from . import Detector


class Idenfy(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://www.idenfy.com/
        # https://documentation.idenfy.com/face-auth/FaceAuthenticationIframe
        has_idenfy_iframes = soup.find_all(
            "iframe", src=re.compile(r"\b\.idenfy\.com\b", re.I)
        )

        return {
            "iframes": len(has_idenfy_iframes) > 0,
            "subdomains": "ivs.idenfy.com" in webpage or ".idenfy.com" in webpage,
        }


def test_idenfy_iframe():
    example = """
    <iframe
      id="iframe"
      style="width: 80%; height: 800px"
      src="https://face.authentication.idenfy.com/?token=REDACTED"
      allow="camera"></iframe>
    """
    soup = BeautifulSoup(example, "lxml")
    assert Detector.detect(Idenfy.run_checks(example, soup))
