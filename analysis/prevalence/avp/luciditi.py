import re
from bs4 import BeautifulSoup
from . import Detector


class Luciditi(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://plugin-demo.luciditi-api.net/
        luciditi_links_elems = soup.find_all(
            "link", attrs={"href": re.compile(r"luciditi-age-assurance")}
        )
        luciditi_scripts = soup.find_all(
            "script", attrs={"src": re.compile(r"\.luciditi-api\.net")}
        )

        luciditi_id_elems = soup.find_all(id=re.compile(r"^luciditi"))
        luciditi_class_elems = soup.find_all(class_=re.compile(r"^luciditi|luciditi$"))
        luciditi_meta_elems = soup.find_all(
            "meta", attrs={"name": re.compile(r"^luciditi")}
        )

        return {
            "links": len(luciditi_links_elems) > 0,
            "scripts": len(luciditi_scripts) > 0,
            "id_elems": len(luciditi_id_elems) > 0,
            "class_elems": len(luciditi_class_elems) > 0,
            "meta_elems": len(luciditi_meta_elems) > 0,
            "subdomains": ".luciditi-api.net" in webpage
            or ".luciditi.co.uk" in webpage,
        }


def test_luciditi_script():
    script = """
        <body>
            <script src="https://sdk-live3.luciditi-api.net/js/luciditi-sdk.js?ver=1.0.3" id="luciditi_aa-sdk-js"></script>
            <script type="module" src="https://sdk-live3.luciditi-api.net/js-sdk?ver=1.0.3" id="luciditi_aa-ui-sdk-js"></script>
            <script src="/wp-content/plugins/luciditi-age-assurance/includes/assets/js/min/public.min.js?ver=1.0.3" id="luciditi_aa-scripts-js"></script>
        </body>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(Luciditi.run_checks(script, soup))


def test_powered_by_luciditi():
    powered_by_luciditi = """
        <img src="/wp-content/plugins/luciditi-age-assurance//includes/assets/img/powered-by-luciditi.svg" class="powered-by-luciditi">
    """
    soup = BeautifulSoup(powered_by_luciditi, "lxml")
    assert Detector.detect(Luciditi.run_checks(powered_by_luciditi, soup))


def test_luciditi_link_elem():
    link_elem = """
        <link rel="stylesheet" id="luciditi_aa-styles-css" href="/wp-content/plugins/luciditi-age-assurance/includes/assets/css/min/public.min.css?ver=1.0.3" media="all">
    """
    soup = BeautifulSoup(link_elem, "lxml")
    assert Detector.detect(Luciditi.run_checks(link_elem, soup))
