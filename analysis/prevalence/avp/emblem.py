import re
from bs4 import BeautifulSoup
from . import Detector


class Emblem(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # observed at:
        # https://demo-staging.emblemapp.com/

        emblem_links = soup.find_all(
            "a",
            attrs={
                "href": re.compile(
                    r"(emblem\.generflow\.com|.+\.generflow\.com.+emblem|emblemapp\.com|emblemState)",
                    re.I,
                )
            },
        )

        emblem_scripts = soup.find_all(
            "script",
            attrs={
                "src": re.compile(
                    r"emblemstate\.js",
                    re.I,
                )
            },
        )

        has_emblem_elements = (
            len(soup.find_all(class_="emblem-container")) > 0
            or len(soup.find_all(class_="emblem-verify-now-button")) > 0
            or len(soup.find_all(class_="emblem-login")) > 0
        )

        return {
            "links": len(emblem_links) > 0,
            "scripts": len(emblem_scripts) > 0,
            "elements": has_emblem_elements,
            "subdomains": ".emblemapp.com" in webpage or ".generflow.com" in webpage,
        }


def test_emblem_link():
    emblem_link = """
        <a href="https://emblem.emblem-staging.devspace.lsea3.generflow.com/redirect?projectKey=zikzsfkr5xwkbeexvcxavyr3&amp;emblemState=ffca0280-8c20-498b-8a03-5e690fe581a7&amp;qr=true&amp;login=true" class="emblem-login"
            Login
        </a>
    """
    soup = BeautifulSoup(emblem_link, "lxml")
    assert Detector.detect(Emblem.run_checks(emblem_link, soup))


def test_emblem_elements():
    elem = '<div class="emblem-container"></div>'
    soup = BeautifulSoup(elem, "lxml")
    assert Detector.detect(Emblem.run_checks(elem, soup))

    elem = '<a href="https://example.com" class="emblem-login">Login</a>'
    soup = BeautifulSoup(elem, "lxml")
    assert Detector.detect(Emblem.run_checks(elem, soup))


def test_emblem_indirect_ref():
    emblem_ref = """
        <script src="https://cdn.tanktrouble.com/RELEASE-2025-06-30-01/js/tt/roundmodel.js+projectilestate.js+trapstate.js+collectiblestate.js+weaponstate.js+upgradestate.js+counterstate.js+zonestate.js+tankstate.js+playerstate.js+scorestate.js+emblemstate.js+inputstate.js+gamestate.js+roundstate.js.pagespeed.jc.pZ0fcHJziN.js"></script>
    """
    soup = BeautifulSoup(emblem_ref, "lxml")
    assert Detector.detect(Emblem.run_checks(emblem_ref, soup))
