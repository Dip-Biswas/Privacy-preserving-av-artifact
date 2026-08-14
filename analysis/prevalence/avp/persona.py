import re
from bs4 import BeautifulSoup
from . import Detector


class Persona(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://withpersona.com/
        # https://docs.withpersona.com/security
        # https://ccq8nh.csb.app/

        persona_links = soup.find_all(
            "a", attrs={"href": re.compile(r"\.withpersona\.com\b", re.I)}
        )

        persona_iframes = soup.find_all(
            "iframe", attrs={"src": re.compile(r"\.withpersona\.com\b", re.I)}
        )

        return {
            "links": len(persona_links) > 0,
            "iframes": len(persona_iframes) > 0,
            "buttons": len(soup.find_all(id="verify_with_persona__button")) > 0,
            "js_fragment": "Persona.Client" in webpage,
            "subdomains": ".withpersona.com" in webpage,
        }


def test_persona_link():
    link = '<a href="https://inquiry.withpersona.com/inquiry?inquiry-template-id=itmpl_y3B7qEELMkQ8XogGev77QsZn">persona</a>'
    soup = BeautifulSoup(link, "lxml")
    assert Detector.detect(Persona.run_checks(link, soup))


def test_persona_iframe():
    iframe = """
        <iframe data-testid="persona-widget__iframe" title="Verify your identity" class="persona-widget__iframe" allow="camera;microphone;clipboard-write" sandbox="allow-scripts allow-same-origin allow-popups allow-forms allow-modals allow-top-navigation-by-user-activation" frameborder="0" src="https://inquiry.withpersona.com/widget?client-version=5.1.5&amp;container-id=persona-widget-70f711yuo1573n1r&amp;flow-type=inline&amp;inquiry-template-id=itmpl_y3B7qEELMkQ8XogGev77QsZn&amp;environment=sandbox&amp;iframe-origin=https%3A%2F%2F8lkyf9.csb.app"></iframe>
    """
    soup = BeautifulSoup(iframe, "lxml")
    assert Detector.detect(Persona.run_checks(iframe, soup))


def test_persona_init_js():
    persona_init_code = """
    <script>
        const client = new Persona.Client({
        // ...
        fields: {
            nameFirst: "Jane",
            nameLast: "Doe",
            birthdate: "2000-12-31",
            addressStreet1: "132 Second St.",
            addressCity: "San Francisco",
            addressSubdivision: "California",
            addressPostalCode: "93441",
            addressCountryCode: "US",
            phoneNumber: "+14154154154",
            emailAddress: "janedoe@persona.com",
            customAttribute: "hello",
        }
        })
    </script>
    """
    soup = BeautifulSoup(persona_init_code, "lxml")
    assert Detector.detect(Persona.run_checks(persona_init_code, soup))
