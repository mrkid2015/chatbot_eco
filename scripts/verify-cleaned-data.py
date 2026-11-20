"""Verify workbook preservation, SQLite references and pilot message rendering offline."""

import hashlib
import json
from pathlib import Path
import re
import sqlite3

from openpyxl import load_workbook


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data/cleaned"


def main():
    manifest = json.loads((OUT / "manifest.json").read_text(encoding="utf-8"))
    for source in manifest["sources"]:
        assert hashlib.sha256((ROOT / source["filename"]).read_bytes()).hexdigest() == source["sha256"]
    changes = json.loads((ROOT / "data/private/audit/cell-changes.json").read_text(encoding="utf-8"))
    change_map = {(c["source_file"], c["source_sheet"], c["source_row"], c["field"]): c for c in changes}
    for filename, spec in manifest["outputs"].items():
        cleaned = load_workbook(OUT / filename)
        source = load_workbook(ROOT / spec["source"])
        assert "NHAT_KY_CHAT" not in cleaned.sheetnames
        for name, count in spec["sheets"].items():
            sheet = cleaned[name]
            assert sheet.max_row == count + 1, (name, sheet.max_row, count)
            header = [c.value for c in sheet[1]]
            source_header_row = 2 if spec["source"].startswith("ECO_") and name != "DANH_MUC" else 1
            source_sheet = source[name]
            source_headers = [c.value for c in source_sheet[source_header_row]]
            assert header[:len(source_headers)] == source_headers
            source_rows = set()
            for row in sheet.iter_rows(min_row=2):
                record = dict(zip(header, (c.value for c in row)))
                source_row = record["source_row"]
                source_rows.add(source_row)
                for index, field in enumerate(source_headers, 1):
                    original = source_sheet.cell(source_row, index).value
                    change = change_map.get((spec["source"], name, source_row, field))
                    if change:
                        assert original == change["before"]
                        expected = change["after"]
                    else:
                        expected = original
                    assert record[field] == expected, (name, source_row, field)
            first_data = source_header_row + (2 if source_header_row == 2 else 1)
            expected_rows = {row[0].row for row in source_sheet.iter_rows(min_row=first_data)
                             if any(c.value is not None for c in row)}
            assert source_rows == expected_rows, f"Lost/added rows: {name}"
        cleaned.close()
        source.close()
    connection = sqlite3.connect(f"{(OUT / 'eco_agro.sqlite').as_uri()}?mode=ro", uri=True)
    assert connection.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    assert not connection.execute("PRAGMA foreign_key_check").fetchall()
    expected_counts = {"products": 26, "diseases": 143, "symptom_groups": 7, "questions": 16, "pilot_members": 5}
    for table, expected in expected_counts.items():
        assert connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] == expected
    assert not connection.execute("SELECT name FROM sqlite_master WHERE name LIKE '%chat%'").fetchall()
    assert set(manifest["pilot_ids"]) == {r[0] for r in connection.execute("SELECT disease_id FROM pilot_members")}
    for field, expected in (("SP-003", "08897"), ("SP-012", "08616")):
        assert connection.execute("SELECT registration_code FROM products WHERE id=?", (field,)).fetchone()[0] == expected
    preview = json.loads((OUT / "pilot-message-preview.json").read_text(encoding="utf-8"))
    assert len(preview) == 5
    total_messages = 0
    for item in preview:
        messages = item["messages"]
        assert item["disease_id"] in manifest["pilot_ids"]
        assert len(messages[0]) <= 900
        for message in messages:
            assert 0 < len(message) <= 900
            assert not re.search("[\U0001f000-\U0001faff\u2600-\u27bf\ufe0f]", message)
        total_messages += len(messages)
        # Chunks must preserve every section's text after whitespace normalization.
        joined = re.sub(r"\s+", " ", " ".join(messages))
        for (body,) in connection.execute("SELECT body_display FROM answer_sections WHERE disease_id=?", (item["disease_id"],)):
            assert re.sub(r"\s+", " ", body) in joined, f"Lost display content: {item['disease_id']}"
    connection.close()
    print(f"PASS: original hashes; all source business cells/rows; {len(changes)} logged changes; SQLite integrity/FKs; 5 pilot IDs; {total_messages} icon-free preview messages <=900 characters")


if __name__ == "__main__":
    main()
