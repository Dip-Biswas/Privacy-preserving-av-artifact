from bs4 import BeautifulSoup
from . import Detector


class KidsWebServices(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://dev.epicgames.com/docs/kids-web-services/set-up-pv-service/config-api
        # no info on client-side stuff afaict
        return {"subdomain": ".kidswebservices.com" in webpage}


def test_shot_in_the_dark():
    script = """
        <script>
            const url = "https://auth.kidswebservices.com";
        </script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(KidsWebServices.run_checks(script, soup))
