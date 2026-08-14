from bs4 import BeautifulSoup
from . import Detector


class TokenOfTrust(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://tokenoftrust.com/product/age-assurance/
        # https://help.tokenoftrust.com/article/513-apitoken-of-trust-verify-person-api
        return {"subdomains": ".tokenoftrust.com" in webpage}


def test_tot_script():
    tot_script = """
        <script>
            const totEndpoint = "app.tokenoftrust.com";
            var vpOptions = {
                method: "POST",
                uri: "https://" + totEndpoint + "/api/person",
                body: verifyPersonBody,
                json: true, // Automatically stringifies the body to JSON
            };
        </script>
    """
    soup = BeautifulSoup(tot_script, "lxml")
    assert Detector.detect(TokenOfTrust.run_checks(tot_script, soup))
