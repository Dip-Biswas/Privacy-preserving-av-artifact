import argparse
import os
import json

from .check_site import check_site

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-dir", type=str, help="directory containing HTML files to scan"
    )
    parser.add_argument(
        "--output-dir", type=str, help="directory where JSON results will be written"
    )
    parser.add_argument(
        "-n",
        "--num-workers",
        type=int,
        default=1,
        help="number of workers",
    )
    parser.add_argument(
        "-w",
        "--worker",
        type=int,
        default=0,
        help="worker id (0-indexed)",
    )

    args = parser.parse_args()

    dirp = os.path.normpath(args.input_dir)
    outp = os.path.normpath(args.output_dir)

    os.makedirs(outp, exist_ok=True)

    targets = os.listdir(dirp)

    for name in targets[args.worker : len(targets) : args.num_workers]:
        row = {}
        try:
            row = check_site((dirp, name))
        except BaseException:
            continue

        # write to json file
        output_file = os.path.join(outp, os.path.splitext(name)[0] + ".json")
        with open(output_file, "w") as f:
            f.write(json.dumps(row))
