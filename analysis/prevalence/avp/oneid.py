from bs4 import BeautifulSoup
from . import Detector


class OneId(Detector):
    def name() -> str:
        return "OneID"

    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://docs.oneid.uk/guides/api-overview
        return {"subdomains": ".myoneid.co.uk" in webpage or ".oneid.uk" in webpage}


def test_oneid_base_url():
    script = """
        <script>
            const base = "https://controller.myoneid.co.uk";
        </script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(OneId.run_checks(script, soup))


def test_oneid_api_url():
    script = """
        <script>
            const base = "https://api.oneid.uk/v1/";
        </script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(OneId.run_checks(script, soup))


def test_oneid_link():
    link = """
        <a href="
            https://controller.myoneid.co.uk/v2/authorize
                ?client_id=1234
                &redirect_uri=https://example.myoneid.co.uk/return
                &response_type=code&scope=openid profile address email phone
                &state=randomstateid1234
        "> Verify with OneID</a>
    """
    soup = BeautifulSoup(link, "lxml")
    assert Detector.detect(OneId.run_checks(link, soup))
