from bs4 import BeautifulSoup
from . import Detector


class Hyperverge(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://hyperverge.co/
        #
        # couldn't find a demo but they have a small snippet
        # https://hyperverge.co/use-cases/age-verification/
        return {
            "js_fragments": "HyperKycConfig" in webpage or "HyperKYCModule" in webpage,
            "subdomains": ".hyperverge.co" in webpage,
        }


def test_hyperverge():
    fixture = r"""
    <script>
        const config = new HyperKycConfig(authToken, "workflow_id", "user_id");
        HyperKYCModule.launch(config,  (HyperKycResult) => {
            // handle KYC results
        });
    </script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(Hyperverge.run_checks(fixture, soup))
