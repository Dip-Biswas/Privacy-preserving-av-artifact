import re
from bs4 import BeautifulSoup
from . import Detector


class Privately(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # observed:
        #
        # https://showroom-demo.privately.swiss/video_age_verification?useSpoof=false&session_id=yourAPIKey&session_password=yourAPISecret"

        privately_iframe_tags = soup.find_all(
            "iframe", attrs={"src": re.compile(r"\.privately\.swiss", re.I)}
        )

        return {
            "iframes": len(privately_iframe_tags) > 0,
            "subdomains": ".privately.swiss" in webpage,
        }


def test_privately_iframe():
    privately_iframe = """
        <iframe src="https://showroom-demo.privately.swiss/video_age_verification?useSpoof=false&session_id=yourAPIKey&session_password=yourAPISecret" />
    """
    soup = BeautifulSoup(privately_iframe, "lxml")
    assert Detector.detect(Privately.run_checks(privately_iframe, soup))
