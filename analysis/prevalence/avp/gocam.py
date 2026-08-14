import re
from bs4 import BeautifulSoup
from . import Detector


class GoCam(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://go.cam — hosted embed CDN: avs-v2.dev.cam
        # Hosted script: https://avs-v2.dev.cam/static/js/app/avsHosted.js?p=<account_id>&key=<site_key>
        # Iframe SDK global: AvsJsSdk.V1.Core / AvsJsSdk.V1.Config
        # SDK filename (standard implementation, may be self-hosted): avsJsSdkV1.js
        # Agerify (agerify.com) is a white-label of go.cam using the same backend

        cdn_scripts = soup.find_all(
            "script", attrs={"src": re.compile(r"avs-v2\.dev\.cam", re.I)}
        )
        gocam_iframes = soup.find_all(
            "iframe", attrs={"src": re.compile(r"\.go\.cam", re.I)}
        )
        agerify_scripts = soup.find_all(
            "script", attrs={"src": re.compile(r"agerify\.com", re.I)}
        )

        return {
            "cdn_script": len(cdn_scripts) > 0,
            "avs_cdn_domain": "avs-v2.dev.cam" in webpage,
            "js_sdk_global": "AvsJsSdk" in webpage,
            "sdk_filename": "avsJsSdkV1.js" in webpage,
            "gocam_iframe": len(gocam_iframes) > 0,
            "gocam_subdomain": ".go.cam" in webpage,
            "agerify_script": len(agerify_scripts) > 0,
            "agerify_domain": "agerify.com" in webpage,
        }


def test_gocam_hosted_cdn():
    fixture = """
        <script type="application/javascript"
            src="https://avs-v2.dev.cam/static/js/app/avsHosted.js?p=12345&key=abc&language=en">
        </script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(GoCam.run_checks(fixture, soup))


def test_gocam_js_sdk():
    fixture = """
        <script src="avsJsSdkV1.js"></script>
        <script>
            AvsJsSdk.V1.Config.create({ iframeLocationUrl: verificationUrl });
            var avsInstance = new AvsJsSdk.V1.Core();
        </script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(GoCam.run_checks(fixture, soup))


def test_gocam_iframe():
    fixture = """
        <iframe src="https://verify.go.cam/session/abc123" frameborder="0"></iframe>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(GoCam.run_checks(fixture, soup))


def test_agerify_domain():
    fixture = """
        <script src="https://cdn.agerify.com/sdk/v1/agerify.js"></script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(GoCam.run_checks(fixture, soup))


def test_no_false_positive_gocam():
    # Plain link to go.cam homepage should not trigger
    fixture = '<a href="https://go.cam">age verification by go.cam</a>'
    soup = BeautifulSoup(fixture, "lxml")
    assert not Detector.detect(GoCam.run_checks(fixture, soup))
