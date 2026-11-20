"""Read every worksheet/cell, retaining source coordinates for the cleanup audit."""

import hashlib
import json
from pathlib import Path

from openpyxl import load_workbook


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data/private/audit"
FILES = ("ECO_Du_lieu_san_pham.xlsx", "DB-Chatbot-Chan-Doan-Sau-Benh.xlsx")


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    reports = []
    for filename in FILES:
        path = ROOT / filename
        workbook = load_workbook(path, data_only=False)
        report = {
            "file": filename,
            "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "sheets": [],
        }
        with (OUTPUT / f"{path.stem}.raw.jsonl").open("w", encoding="utf-8") as stream:
            for sheet in workbook:
                rows = []
                columns = {}
                formulas = []
                for row in sheet:
                    cells = []
                    for cell in row:
                        if cell.value is None:
                            continue
                        entry = {"cell": cell.coordinate, "value": cell.value, "type": cell.data_type}
                        if cell.hyperlink:
                            entry["hyperlink"] = cell.hyperlink.target
                        cells.append(entry)
                        columns.setdefault(cell.column_letter, {"nonempty": 0, "samples": []})
                        stat = columns[cell.column_letter]
                        stat["nonempty"] += 1
                        if len(stat["samples"]) < 5:
                            stat["samples"].append({"row": cell.row, "value": cell.value})
                        if cell.data_type == "f":
                            formulas.append(cell.coordinate)
                    if cells:
                        record = {"file": filename, "sheet": sheet.title, "row": row[0].row, "cells": cells}
                        stream.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
                        rows.append(row[0].row)
                report["sheets"].append({
                    "name": sheet.title,
                    "state": sheet.sheet_state,
                    "max_row": sheet.max_row,
                    "max_column": sheet.max_column,
                    "nonempty_rows": len(rows),
                    "first_rows": rows[:12],
                    "merges": [str(item) for item in sheet.merged_cells.ranges],
                    "formulas": formulas,
                    "images": len(sheet._images),
                    "columns": columns,
                })
        workbook.close()
        reports.append(report)
    (OUTPUT / "workbook-profile.json").write_text(
        json.dumps(reports, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8"
    )
    print(json.dumps(reports, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
