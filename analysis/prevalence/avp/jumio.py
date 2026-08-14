from bs4 import BeautifulSoup
from . import Detector


class Jumio(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        return {
            "popup_classes": (
                ".jumio-verify-popup" in webpage
                or ".age-verification-jumio-popup" in webpage
                or "jumio-verification-custom-popup" in webpage
            ),
            "kyx": "jumiokyx" in webpage,
            "document_type": "jumioDocumentType" in webpage,
            "all_uploaded": "jumio_all_uploaded" in webpage,
        }


def test_jumio_css():
    jumio_style = """
    <head>
        <!-- Tag name is CSS jumio-verify-popup -->
        <style>
            .jumio-verify-popup {
                font-size: 1rem;
                min-height: 13em;
                max-width: 42em;
                border-radius: .156em;
                align-self: center;
            }
        </style>
    </head>
    """
    soup = BeautifulSoup(jumio_style, "lxml")
    assert Detector.detect(Jumio.run_checks(jumio_style, soup))

    jumio_style = ".age-verification-jumio-popup .popup-modal__button_type_close{display:block;top:.5em;right:1em}"
    soup = BeautifulSoup(jumio_style, "lxml")
    assert Detector.detect(Jumio.run_checks(jumio_style, soup))


def test_jumio_js():
    jumio_inline_script = """
        <script>
            const jumResponse = await Playtech.API.server.initiateDocumentUpload({
                service: 'jumiokyx',
                successUrl: location.origin + '/successful-upload?hideHeader=1&hideFooter=1&hideWidgets=1',
                errorUrl: location.origin + '/unsuccessful-upload?hideHeader=1&hideFooter=1&hideWidgets=1',
                documentType: 'AAA1',
            });

            Playtech.API.popup.showPopup({
                title: '',
                content: '<style>.popup-modal__buttons.Popup__actionButtons--3N7{display:none} .desktop .application-root .Popup__inner--2Ba .jum-pend-pop-ver a.logout-popup-btn:hover{color:#000!important;} .logout-popup-btn{margin-left:10px;border-radius:5px; background-color:transparent;color:#000; padding:10px 20px; display:inline-block; text-align:center; font-weight:bold;}</style><div class="jum-pend-pop-ver"><p>Para concluir con la validación de tu cuenta solo necesitamos tu comprobante de domicilio no mayor a tres meses. </p><a href="' + jumResponse.data.redirectURL + '" class="verify-me-btn" style="width:auto;">Valida tu dirección</a></div>',
                isModal: false,
                id: 'jumio-verification-custom-popup',
                buttons: false
            });
        </script>
    """
    soup = BeautifulSoup(jumio_inline_script, "lxml")
    assert Detector.detect(Jumio.run_checks(jumio_inline_script, soup))

    more_jumio_refs = "<script>const TAG = 'risk/jumio_all_uploaded';</script>"
    soup = BeautifulSoup(more_jumio_refs, "lxml")
    assert Detector.detect(Jumio.run_checks(more_jumio_refs, soup))

    more_jumio_refs = "<script>var styles = `#jumioDocumentType, .label-for-jum-doc-type {display:none;};`</script>"
    soup = BeautifulSoup(more_jumio_refs, "lxml")
    assert Detector.detect(Jumio.run_checks(more_jumio_refs, soup))
