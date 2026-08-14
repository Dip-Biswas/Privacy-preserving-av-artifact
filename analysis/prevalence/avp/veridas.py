import re
from bs4 import BeautifulSoup
from . import Detector


class Veridas(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        veridas_elems = soup.find_all(
            id=re.compile(
                r"^popup_Veridas|fldOTPEntryVeridasFace|imgVeridasLoginVideo|VeridasLogin.+?Output|VeridasEnroll.+?Output|btnOTPVeridasFace|btnVeridasFaceCapture|PGTokenVeridas$",
                re.I,
            )
        )

        return {
            "elems": len(veridas_elems) > 0,
            "subdomains": ".veridas.com" in webpage,
        }


def test_veridas_popup():
    veridas_popup = """
        <div id="popup_Veridas" class="popupWin" role="dialog" aria-labelledby="lblVeridasTitle" style="display: none">
    """
    soup = BeautifulSoup(veridas_popup, "lxml")
    assert Detector.detect(Veridas.run_checks(veridas_popup, soup))


def test_veridas_enroll():
    veridas_enroll = """
        <div class="row">
            <video id="VeridasEnrollCameraOutput" width="640" height="480" autoplay="" style="display: none"></video><br>
            <canvas id="VeridasEnrollPreviewOutput" width="240" height="240"></canvas><br>
        </div>
    """
    soup = BeautifulSoup(veridas_enroll, "lxml")
    assert Detector.detect(Veridas.run_checks(veridas_enroll, soup))


def test_veridas_form():
    veridas_form = """
        <form>
            <input type="hidden" id="VeridasAcctStep" name="AcctStep" value="1">
            <input id="VeridasSourceData" type="hidden" name="SourceData">
            <input id="UsernameVeridas" type="hidden" name="Username">
            <input id="PasswordVeridas" type="hidden" name="Password">
            <input id="PGTokenVeridas" type="hidden" name="PGToken" value=""
        </form>
    """
    soup = BeautifulSoup(veridas_form, "lxml")
    assert Detector.detect(Veridas.run_checks(veridas_form, soup))
