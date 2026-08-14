import re
from bs4 import BeautifulSoup
from . import Detector


class OneAccount(Detector):
    def name() -> str:
        return "1Account"

    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # observed:
        #
        # https://www.1account.net/pushApi/index.js
        # https://www.1account.net/push
        # https://demo-shopify.1account.net/

        one_account_scripts = soup.find_all(
            "script", attrs={"src": re.compile(r"1account\.net")}
        )
        one_account_iframes = soup.find_all(
            "iframe", attrs={"src": re.compile(r"1account\.net")}
        )
        one_account_link_elems = soup.find_all(
            "link", attrs={"href": re.compile(r"1account\.net")}
        )

        one_account_id_elems = soup.find_all(id=re.compile(r"^one-account-"))

        return {
            "scripts": len(one_account_scripts) > 0,
            "iframes": len(one_account_iframes) > 0,
            "links": len(one_account_link_elems) > 0,
            "id_elems": len(one_account_id_elems) > 0,
            "js_fragment": "HOSTED_AV.init" in webpage,
            "subdomains": ".1account.net" in webpage,
        }


def test_one_account_script():
    script = """
        <script src="https://www.1account.net/widget/index.js" data-logo="https://one-account-live-image-upload.s3.eu-west-2.amazonaws.com/logo-demo1582722406366.svg" data-secret="REDACTED" id="one-account-hosted-av"></script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(OneAccount.run_checks(script, soup))

    script = """
        <script id="one-account-push-api" data-logo="https://one-account-live-image-upload.s3.eu-west-2.amazonaws.com/logo.svg" src="https://www.1account.net/pushApi/index.js"></script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(OneAccount.run_checks(script, soup))


def test_one_account_iframe():
    iframe = """
        <iframe src="https://www.1account.net/push" title="one-account-push-api" id="one-account-push-api" allow="camera; otp-credentials"></iframe>
    """
    soup = BeautifulSoup(iframe, "lxml")
    assert Detector.detect(OneAccount.run_checks(iframe, soup))


def test_script_elem_init():
    script = """
        <script>
        HOSTED_AV.init({
            industry: 'GAMBLING',
            scope: '2.0',
            clientId: 'ef643d6a-fb2e-4ffa-b',
            authCode: Math.round(Math.random() * 10000000000000000).toString(),
            onComplete: () => {
            console.log('AGE VERIFICATION SUCCESSFUL', 'https://account-18602.firebaseio.com/hosted.json')
            HOSTED_AV.hide()
            }
        })
        </script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(OneAccount.run_checks(script, soup))


def test_one_account_stylesheet():
    stylesheet = """
        <link rel="stylesheet" type="text/css" href="https://www.1account.net/pushApi/style.css">
    """
    soup = BeautifulSoup(stylesheet, "lxml")
    assert Detector.detect(OneAccount.run_checks(stylesheet, soup))
