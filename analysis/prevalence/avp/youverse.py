from bs4 import BeautifulSoup
from . import Detector


class Youverse(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://www.youverse.id/docs/3.x/web
        return {
            "user_verification_path": "/user_verification/decentralized" in webpage
            or "/user_verification/verify_template" in webpage,
            "face_process_path": "/face/process" in webpage,
            "bit_verify_imgs_path": "/bit/verify_images" in webpage,
            "subdomains": ".youverse.id" in webpage,
        }


def test_youverse_links():
    script_with_reference = """
        <script>
            const base = "https://example.com";
            const link = `${base}/face/process?foo=bar`;
        </script>
    """
    soup = BeautifulSoup(script_with_reference, "lxml")
    assert Detector.detect(Youverse.run_checks(script_with_reference, soup))
