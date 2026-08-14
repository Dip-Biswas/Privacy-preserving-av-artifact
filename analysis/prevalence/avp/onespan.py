import re
from bs4 import BeautifulSoup
from . import Detector


class OneSpan(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://docs.onespan.com/docs/integration-model
        # https://docs.onespan.com/v1/docs/onespan-identity-verification-rest-api
        # https://docs.onespan.com/docs/document-and-selfie-capture-guidelines
        #
        # doesn't seem very frontend-focused. not sure if they have any client-side integrations
        return {
            "catchall": re.compile(r"\bonespan\b").search(webpage) is not None
            or ".onespan.com" in webpage
        }


def test_shot_in_the_dark():
    script = """
        <script>
            const url = "https://foo.onespan.com/bar";
        </script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(OneSpan.run_checks(script, soup))
