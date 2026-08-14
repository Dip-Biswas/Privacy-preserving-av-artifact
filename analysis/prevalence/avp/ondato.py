from bs4 import BeautifulSoup
from . import Detector


class Ondato(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        return {
            "subdomains": ".ondato.net" in webpage,
            "in_path": "/ondato/" in webpage,
        }


def test_ondato_styles():
    ondato_css = """
        <link data-v-829e69da="" rel="stylesheet" type="text/css" href="https://stgkycformprod.z6.web.core.windows.net/customs/ondato/styles.css"> <div data-v-829e69da="" class="app-content">
    """
    soup = BeautifulSoup(ondato_css, "lxml")
    assert Detector.detect(Ondato.run_checks(ondato_css, soup))
