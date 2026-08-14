import os
import json

from bs4 import BeautifulSoup

from prevalence.avp import Detector, ADetector, DETECTORS, COLUMN_NAMES
from prevalence.cloudflare import has_cloudflare_error
from prevalence.rta import has_rta_label


def check_site(
    params: tuple[str, str], detectors=DETECTORS, column_names=COLUMN_NAMES
) -> dict[str, str | bool]:
    dir_path, file = params

    fname = file
    file = os.path.join(dir_path, file)

    with open(file) as f:
        site_name, _ = fname.split(".html")
        row = {"name": site_name}
        for c in column_names:
            row[c] = 0

        if os.stat(file).st_size == 0:
            row["is_empty"] = 1
            return row

        file_contents = f.read()
        row.update(run_detectors(site_name, file_contents, detectors, column_names))
        return row


def run_detectors(
    name: str, webpage: str, detectors=DETECTORS, column_names=COLUMN_NAMES
) -> dict[str, str | int]:
    row = {"name": name}
    for c in column_names:
        row[c] = 0

    soup = None
    try:
        soup = BeautifulSoup(webpage, "lxml")
    except BaseException:
        row["parse_error"] = 1
        return row

    if has_cloudflare_error(soup):
        row["cloudflare"] = 1
        return row
    else:
        row["cloudflare"] = 0

    row["rta"] = 1 if has_rta_label(soup) else 0

    results_dict = dict([check_soup((d, (webpage, soup))) for d in detectors])

    # holy list comprehension
    prepped_results = dict(
        [
            (provider, 1 if was_detected else 0)
            for provider, (was_detected, _) in results_dict.items()
        ]
    )
    prepped_results["meta_info"] = json.dumps(
        dict(
            [
                (provider, fingerprint_names)
                for provider, (was_detected, fingerprint_names) in results_dict.items()
                if was_detected
            ]
        )
    )

    row.update(prepped_results)
    return row


def check_soup(
    params: tuple[
        ADetector,
        tuple[str, BeautifulSoup],  # (webpage, soup)
    ],
) -> tuple[str, tuple[bool, list[str]]]:
    detector, webpage_soup = params
    webpage, soup = webpage_soup

    result = False
    try:
        check_results = detector.run_checks(webpage, soup)
        result = Detector.detect(check_results)
        passed_checks = Detector.passed_checks(check_results)
    except BaseException:
        pass

    return (detector.name(), (result, passed_checks))
