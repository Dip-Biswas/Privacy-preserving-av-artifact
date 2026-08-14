import argparse
import csv
import itertools
import pathlib
import random
import time
from typing import Generator

from crawl import visit_website

CLOUDFLARED_CONTROL = "https://example.com"
NON_CLOUDFLARED_CONTROL = "https://example.com"


def random_csv_reader(filename: str) -> Generator[str]:
    offsets = []
    with open(filename, "rb") as f:
        _ = f.readline()  # headers
        line = f.readline()
        while line:
            offsets.append(f.tell() - len(line))
            line = f.readline()

    random.shuffle(offsets)

    with open(filename, "r", newline="", encoding="utf-8") as f:
        for offset in offsets:
            f.seek(offset)
            line = f.readline()
            row = next(csv.reader([line]))
            yield row


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "domain_csv_path",
        type=pathlib.Path,
        help="path to the (rank, domain) csv of domains",
    )
    parser.add_argument(
        "-n",
        "--num-workers",
        type=int,
        help="number of workers",
    )
    parser.add_argument(
        "-w",
        "--worker",
        type=int,
        help="worker id",
    )
    parser.add_argument(
        "--seed-file",
        type=pathlib.Path,
        help="path to a file with the hex-encoded randomness seed",
    )
    parser.add_argument(
        "--container-output-dir",
        type=str,
        default="/opt/pages",
        help="in-container path to the output directory",
    )
    parser.add_argument(
        "--proxy",
        type=int,
        default=None,
        help="port to use socks5 proxy on (if any)",
    )
    parser.add_argument(
        "--skip",
        type=int,
        default=0,
        help="number of pages to skip",
    )
    parser.add_argument(
        "--num-targets",
        type=int,
        default=1_000_000,
        help="total number of top domains to crawl from the list",
    )

    args = parser.parse_args()

    visit_website(
        CLOUDFLARED_CONTROL,
        args.container_output_dir,
        proxy_port=args.proxy,
        output_path=f"{args.container_output_dir}/_{args.worker}_{round(time.time())}_cf-av_control.html",
    )

    visit_website(
        NON_CLOUDFLARED_CONTROL,
        args.container_output_dir,
        proxy_port=args.proxy,
        output_path=f"{args.container_output_dir}/_{args.worker}_{round(time.time())}_nocf-av_control.html",
    )

    seed = b""
    with open(args.seed_file, "r") as f:
        seed = bytes.fromhex(f.read())

    random.seed(seed)

    targets = enumerate(random_csv_reader(args.domain_csv_path))

    if args.skip > 0:
        print(f"skipping {args.skip} pages...")
        for i, (page, _) in itertools.islice(targets, 0, args.skip):
            print(f"skipping [{i}] {page}")

    NUM_TARGETS = args.num_targets
    for i, (page, rank) in itertools.islice(
        targets, args.worker, NUM_TARGETS - args.skip, args.num_workers
    ):
        print(f"index: {i}, rank: {rank}, site: {page}")
        visit_website(page, args.container_output_dir, proxy_port=args.proxy)

    visit_website(
        CLOUDFLARED_CONTROL,
        args.container_output_dir,
        proxy_port=args.proxy,
        output_path=f"{args.container_output_dir}/_{args.worker}_{round(time.time())}_cf-av_control.html",
    )

    visit_website(
        NON_CLOUDFLARED_CONTROL,
        args.container_output_dir,
        proxy_port=args.proxy,
        output_path=f"{args.container_output_dir}/_{args.worker}_{round(time.time())}_nocf-av_control.html",
    )
