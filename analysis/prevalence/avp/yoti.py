import re
from bs4 import BeautifulSoup
from . import Detector
from .veriff import Veriff

YOTI_PATTERN = re.compile(r"\.yoti\.com|/yoti", re.I)
YOTI_AVS_GATE = re.compile(r"avsgate\.com.+?age-verify.+?yoti")


class Yoti(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # Restrict link detection to external yoti.com hrefs. The broader
        # YOTI_PATTERN (/yoti) also matched footer nav links like href="/yoti"
        # pointing to the site's own Yoti information page, not a Yoti SDK endpoint.
        yoti_links = soup.find_all(
            "a", attrs={"href": re.compile(r"\.yoti\.com", re.I)}
        )
        yoti_iframes = soup.find_all("iframe", attrs={"src": YOTI_PATTERN})
        yoti_like_elems = soup.find_all(id=re.compile(r"^yoti-"))

        return {
            "links": len(yoti_links) > 0,
            "iframes": len(yoti_iframes) > 0,
            "yoti_id_elems": len(yoti_like_elems) > 0,
            # /wp-content/plugins/yoti-age-verification-wordpress/public/js/yoti-av-modal.js?ver=6.8.2
            "wordpress_plugin": "/wp-content/plugins/yoti-" in webpage,
            "avsgate": YOTI_AVS_GATE.search(webpage) is not None,
            "agegate": "/agegate/yoti" in webpage,  # /yoti_av or /yoti_anon
            # one particular company
            "config_is_yoti_enabled": 'config.isYotiAgeVerificationEnabled = "1"'
            in webpage,
            "subdomains": ".yoti.com" in webpage,
        }


def test_yoti_link():
    # A link pointing to yoti.com should trigger
    link = '<a href="https://connect.yoti.com/verify"></a>'
    soup = BeautifulSoup(link, "lxml")
    assert Detector.detect(Yoti.run_checks(link, soup))

    # A site-internal /yoti path (e.g. a footer "learn about Yoti" link) must not
    link = '<a href="https://example.com/yotiage"></a>'
    soup = BeautifulSoup(link, "lxml")
    assert not Detector.detect(Yoti.run_checks(link, soup))


def test_yoti_iframe():
    iframe = '<iframe src="https://age.yoti.com/stuff"></iframe>'
    soup = BeautifulSoup(iframe, "lxml")
    assert Detector.detect(Yoti.run_checks(iframe, soup))


def test_jyoti():
    link = '<a href="https://jyoti.example.com/"></a>'
    soup = BeautifulSoup(link, "lxml")
    assert not Detector.detect(Yoti.run_checks(link, soup))


def test_yoti_misc():
    fixture = r"""
        <script>const stuff = "https://age.yoti.com";</script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(Yoti.run_checks(fixture, soup))

    fixture = r"""
        <script>const stuff = "https://api.yoti.com";</script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(Yoti.run_checks(fixture, soup))


def test_avsgate_yoti():
    fixture = r"""
    <script>
        const stuff = "https:\/\/avsgate.com\/v1\/age-verify\/yoti";
    </script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert Detector.detect(Yoti.run_checks(fixture, soup))

    fixture = r"""
    <script>
        const stuff = "https:\/\/avsgate.com\/v1\/age-verify\/facetec";
    </script>
    """
    soup = BeautifulSoup(fixture, "lxml")
    assert not Detector.detect(Yoti.run_checks(fixture, soup))


def test_agegate_yoti():
    agegate_yoti = """
        <script>
            const YOTI_POST_URL = "/agegate/yoti_av/?key=key&method=yoti_av";
        </script>
    """
    soup = BeautifulSoup(agegate_yoti, "lxml")
    assert Detector.detect(Yoti.run_checks(agegate_yoti, soup))

    agegate_yoti = """
        <script>
            const YOTI_ANON_POST_URL = "/agegate/yoti_anon/?key=key&method=yoti_anon";
        </script>
    """
    soup = BeautifulSoup(agegate_yoti, "lxml")
    assert Detector.detect(Yoti.run_checks(agegate_yoti, soup))


def test_xh():
    with open("prevalence/fixtures/xhamster1.desi.html") as f:
        webpage = f.read()
        soup = BeautifulSoup(webpage, "lxml")
        assert not Detector.detect(Veriff.run_checks(webpage, soup))
        assert Detector.detect(Yoti.run_checks(webpage, soup))


def test_base64_false_positives():
    with open("prevalence/fixtures/www.cyberabadpolice.gov.in.html") as f:
        webpage = f.read()
        soup = BeautifulSoup(webpage, "lxml")
        assert not Detector.detect(Yoti.run_checks(webpage, soup))


def test_config_is_yoti_enabled():
    # pattern used by some sites (presumably) operated by one particular company
    script = """
        <script>
            window.config.isYotiAgeVerificationEnabled = "1";
            window.config.isIncodeAgeVerificationEnabled = "0";
        </script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(Yoti.run_checks(script, soup))
