from bs4 import BeautifulSoup
from . import Detector


class ComplyCube(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://docs.complycube.com/api-reference
        return {
            "mount_elem": len(soup.find_all(id="complycube-mount")) > 0,
            "js_fragment": "ComplyCube.mount" in webpage,
            "subdomains": (
                "api.complycube.com" in webpage
                or "flow.complycube.com" in webpage
                or ".complycube.com" in webpage
            ),
        }


def test_complycube_mount_elem():
    example = """
        <body>
            <!-- This is where the Web SDK will be mounted -->
            <div id="complycube-mount"></div>

            <!-- Clicking the button will start the ComplyCube verification UI -->
            <button onClick="startVerification()">Start verification</button>
        </body>
    """

    soup = BeautifulSoup(example, "lxml")
    assert Detector.detect(ComplyCube.run_checks(example, soup))


def test_mount_code():
    example = """
        <script>
            var complycube = {};
            function startVerification() {
            complycube = ComplyCube.mount({
                token: "<YOUR_WEB_SDK_TOKEN>",
                onComplete: function(data) {
                console.log("Capture complete", data)
                },
            });
            }
        </script>
    """

    soup = BeautifulSoup(example, "lxml")
    assert Detector.detect(ComplyCube.run_checks(example, soup))
