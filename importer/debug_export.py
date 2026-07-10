"""
LaundryBot V6

Debug Export
"""

from pathlib import Path


def save_debug(pdf_file, text):

    debug_folder = Path("service_reports/debug")

    debug_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    txt = debug_folder / (pdf_file.stem + ".txt")

    with open(
        txt,
        "w",
        encoding="utf-8",
    ) as f:

        f.write(text)