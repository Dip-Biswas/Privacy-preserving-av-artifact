import re
from bs4 import BeautifulSoup
from . import Detector


class BioId(Detector):
    def name() -> str:
        return "BioID"

    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        grpc_api = re.compile(r"\b(grpc|face)\.[a-z-]+\.bioid\.com", re.I)

        # https://developer.bioid.com/classicbws/bwsreference/webapi/upload
        return {
            "subdomains": (
                "bws.bioid.com" in webpage
                or "schemas.bioid.com" in webpage
                or ".bioid.com" in webpage
                or grpc_api.search(webpage) is not None
            ),
            "url_schemes": "bioid-verify://" in webpage or "bioid-enroll://" in webpage,
        }


def test_bioid_jquery_example():
    fixture = """
        <script>
            const dataURL = canvas.toDataURL();
            jQuery.ajax({
                url: "https://bws.bioid.com/extension/upload?" + jQuery.param({
                    "tag": "up"
                }),
                type: "POST",
                headers: {
                    "Authorization": "Bearer " + token
                },
                data: dataURL,
            }).done(function (data, textStatus, jqXHR) {
            if (data.Accepted) {
                console.log("upload succeeded", data.Warnings);
            } else {
                console.log("upload error", data.Error);
            }
            });
        </script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(BioId.run_checks(fixture, soup))


def test_bioid_grpc_api():
    fixture = """
        <script>
            const endpoint = "https://grpc.{bws-location}.bioid.com";
        </script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(BioId.run_checks(fixture, soup))
