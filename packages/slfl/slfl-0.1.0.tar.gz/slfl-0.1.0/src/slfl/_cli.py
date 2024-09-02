import argparse
import logging
from pathlib import Path
from ._dsl import exec_all


def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "tasks_file", type=Path, help="Path to .py file with tasks. Should be relative."
    )
    parser.add_argument(
        "-j",
        "--job_id",
        type=str,
        help="Job ID to resume. If not passed, a new job will be started.",
    )
    args = parser.parse_args()

    exec_all(tasks_file=args.tasks_file, job_id=args.job_id)

    return 0
