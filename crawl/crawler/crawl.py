import os
import gc
import time
import shutil
import tempfile
from urllib3.exceptions import (
    HTTPError,
    NewConnectionError,
    MaxRetryError,
    TimeoutError,
)

from pyvirtualdisplay import Display

from selenium import webdriver


def visit_website(
    page: str,
    container_output_dir: str,
    proxy_port: int | None = None,
    output_path: str | None = None,
) -> None:
    # display must exist before we run selenium
    with Display(visible=False, size=(800, 600)):
        chrome_options = webdriver.ChromeOptions()

        # chrome_options.add_experimental_option("useAutomationExtension", False)
        # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_argument("enable-automation")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--remote-debugging-pipe")
        # https://stackoverflow.com/a/40528075
        chrome_options.add_argument("--dns-prefetch-disable")
        chrome_options.add_argument("ignore-certificate-errors")
        user_data_dir = tempfile.mkdtemp()
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

        driver = None
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_script_timeout(25)
            driver.set_page_load_timeout(25)
        except Exception as e:
            print(e)
            # os.system("pkill chromedriver")
            # os.system("pkill google-chrome")
            driver = None
        except (HTTPError, NewConnectionError, MaxRetryError, TimeoutError) as e:
            print(e)
            # os.system("pkill chromedriver")
            # os.system("pkill google-chrome")
            driver = None

        if driver is None:
            print(f"bailing on {page}")
            return

        _, domain = page.split("://")
        sources_path = output_path or f"{container_output_dir}/{domain}.html"

        try:
            if os.path.exists(sources_path):
                print(f"skipping {page} (already exists)")
                driver.close()
                driver.quit()
                return

            driver.get(page)
            time.sleep(2)

            with open(sources_path, "w") as outf:
                outf.write(driver.page_source)
        except Exception as e:
            print(e)
            print(f"bailing on {page}")
        except (HTTPError, NewConnectionError, MaxRetryError, TimeoutError) as e:
            print(e)
            print(f"bailing on {page}")
        finally:
            try:
                driver.close()
            except (
                Exception,
                HTTPError,
                NewConnectionError,
                MaxRetryError,
                TimeoutError,
            ) as e:
                print(e)
                print("error closing driver")

            try:
                driver.quit()
            except (
                Exception,
                HTTPError,
                NewConnectionError,
                MaxRetryError,
                TimeoutError,
            ) as e:
                print(e)
                print("error closing driver")

            del driver
            gc.collect()
            shutil.rmtree(user_data_dir, ignore_errors=True)
