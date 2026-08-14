from bs4 import BeautifulSoup
from . import Detector


class Au10tix(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        return {
            "wrapper-class": ".mwc-external-id-verification-au10tix-wrapper" in webpage,
            "iframe-wrapper": ".mwc-au10tix-iframe-wrapper" in webpage,
            "subdomains": (
                ".au10tixservicesstaging.com" in webpage
                or "secure-me.au10tixservices.com" in webpage
                or ".au10tixservices.com" in webpage
            ),
            "should_process_docs": 'shouldProcessDocumentsThroughAU10TIX:"1"'
            in webpage,
        }


def test_aut10tix_elems():
    elems = """
        .mwc-external-id-verification-au10tix-wrapper .mwc-au10tix-iframe-wrapper{max-width:800px;margin:0 auto}
    """
    soup = BeautifulSoup(elems, "lxml")
    assert Detector.detect(Au10tix.run_checks(elems, soup))


def test_aut10tix_links():
    link = """
        <a href="https://secure-me.au10tixservicesstaging.com"></a>
    """
    soup = BeautifulSoup(link, "lxml")
    assert Detector.detect(Au10tix.run_checks(link, soup))

    link = """
        <a href="https://secure-me.au10tixservices.com"></a>
    """
    soup = BeautifulSoup(link, "lxml")
    assert Detector.detect(Au10tix.run_checks(link, soup))
