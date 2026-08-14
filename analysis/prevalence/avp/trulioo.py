from bs4 import BeautifulSoup
from . import Detector


class Trulioo(Detector):
    @staticmethod
    def run_checks(webpage: str, soup: BeautifulSoup) -> dict[str, bool]:
        # https://www.trulioo.com/
        # https://developer.trulioo.com/reference/api-reference-overview
        # https://developer.trulioo.com/reference/web#3-start-a-verification-flow
        return {
            "js_init": "Trulioo.initialize" in webpage,
            "js_launch": "Trulioo.launch" in webpage,
            "js_workflow": "Trulioo.workflow" in webpage,
            "js_new_capture": "new TruliooCapture" in webpage,
            "js_import": "@trulioo/" in webpage,
            "subdomains": (
                "api.trulioo.com" in webpage
                or "verification.trulioo.com" in webpage
                or ".trulioo.com" in webpage
            ),
        }


def test_init_and_launch():
    script = """
        <script>
            // Initialize the SDK with the workflow configuration
            Trulioo.initialize(workflowOption)
                .then(complete => {
                    console.info("Initialize complete:", complete)
                    // Launch the UI with the provided HTML element ID
                    Trulioo.launch(elementID, callbackOption)
                        .then(success => {
                            console.info("Launch success:", success)
                        })
                })
                .catch(error =>
                    console.error("Error:", error)
                )
        </script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(Trulioo.run_checks(script, soup))


def test_workflow_options():
    script = """
        <script>
            const workflowOption = Trulioo.workflow()
            .setShortCode(shortCode)
            .setTheme(workflowTheme) // Set the created WorkflowTheme object as part of the Workflow configuration
        </script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(Trulioo.run_checks(script, soup))


def test_trulioo_capture():
    script = """
        <script>
            const shortCode = "generatedFromTruliooAPI"

            const truliooCapture = new TruliooCapture()

            truliooCapture.initialize(shortCode).then((transactionId: string) => {
                console.log(`Successfully initialized with transaction ID: ${transactionId}`)
            }).catch((error: any) => {
                console.log(`Error on initialize: ${error}`)
            })
        </script>
    """
    soup = BeautifulSoup(script, "lxml")
    assert Detector.detect(Trulioo.run_checks(script, soup))


def test_stylesheet():
    link_elem = """
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@trulioo/docv-csp/main.css">
    """
    soup = BeautifulSoup(link_elem, "lxml")
    assert Detector.detect(Trulioo.run_checks(link_elem, soup))
