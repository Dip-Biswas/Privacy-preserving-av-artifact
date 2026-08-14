import re
from bs4 import BeautifulSoup
from . import Detector


class Kid(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://k-id.com — AgeKit / CDK (Compliance Development Kit)
        # Widget iframe: family.k-id.com/widget?token=[TOKEN]
        # iframe IDs: id="vpc-widget", id="vpc-container"
        # JS postMessage events: Widget.AgeGate.Result, Widget.AgeGate.Challenge
        # API: game-api.k-id.com

        kid_iframes = soup.find_all(
            "iframe", attrs={"src": re.compile(r"\.k-id\.com", re.I)}
        )
        kid_iframes_id = soup.find_all("iframe", attrs={"id": "vpc-widget"})

        return {
            "iframe_src": len(kid_iframes) > 0,
            "iframe_id": len(kid_iframes_id) > 0,
            "vpc_container": 'id="vpc-container"' in webpage or "vpc-container" in webpage,
            "agegate_event": "Widget.AgeGate" in webpage,
            "api_domain": "game-api.k-id.com" in webpage,
            "subdomains": ".k-id.com" in webpage,
        }


def test_kid_iframe():
    fixture = """
        <div id="vpc-container">
            <iframe
                id="vpc-widget"
                src="https://family.k-id.com/widget?token=abc123"
                width="100%"
                height="600"
                allow="camera;payment;publickey-credentials-get">
            </iframe>
        </div>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(Kid.run_checks(fixture, soup))


def test_kid_agegate_event():
    fixture = """
        <script>
            window.addEventListener("message", (event) => {
                if (event.data.type === "Widget.AgeGate.Result") {
                    const { sessionId } = event.data;
                    // grant access
                }
            });
        </script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(Kid.run_checks(fixture, soup))


def test_kid_api_domain():
    fixture = """
        <script>
            const res = await fetch("https://game-api.k-id.com/api/v1/widget/generate-e2e-url", {
                method: "POST",
                headers: { "Authorization": "Bearer ..." }
            });
        </script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(Kid.run_checks(fixture, soup))


def test_no_false_positive_kid():
    fixture = '<a href="https://k-id.com/blog">blog post</a>'
    soup = BeautifulSoup(fixture, "lxml")
    assert not Detector.detect(Kid.run_checks(fixture, soup))
