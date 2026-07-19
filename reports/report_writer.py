import json
from pathlib import Path
from datetime import datetime


def save_report(report):
    time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    folder = Path('reports')
    folder.mkdir(exist_ok=True)


    filename = folder / f"{time}_debug_run.json"

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            report.to_dict(),
            file,
            indent=4
        )

    return filename