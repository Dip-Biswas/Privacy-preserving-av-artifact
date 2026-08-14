from bs4 import BeautifulSoup
from . import Detector


class ShareRing(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        sharering_buttons = soup.find_all("img", attrs={"alt": "sharering me"})

        return {
            "buttons": len(sharering_buttons) > 0,
            "domains": (
                "sharering.network" in webpage
                or "sharering.link" in webpage
                or "sharer.ing" in webpage
                or "//sharering.internal" in webpage
            ),
            "url_scheme": "sharering://" in webpage,
        }


def test_sharering_link():
    link = """
        <a href="https://sharering.link">link</a>
    """
    soup = BeautifulSoup(link, "lxml")
    assert Detector.detect(ShareRing.run_checks(link, soup))


def test_sharelink_logo():
    logo = """
        <a href="#" class=""><img src="/oauth2/statics/assets/images/srme.svg" width="64" height="64" alt="sharering me" style="cursor: pointer;"></a>
    """
    soup = BeautifulSoup(logo, "lxml")
    assert Detector.detect(ShareRing.run_checks(logo, soup))
