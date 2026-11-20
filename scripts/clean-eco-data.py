"""Normalize Eco Agro sources without modifying originals or inventing technical facts.

Run with .venv/Scripts/python.exe -X utf8 scripts/clean-eco-data.py
Outputs are local data artifacts, not a running chatbot.
"""

from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import unicodedata

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data/cleaned"
AUDIT = ROOT / "data/private/audit"
FILES = ("ECO_Du_lieu_san_pham.xlsx", "DB-Chatbot-Chan-Doan-Sau-Benh.xlsx")
PILOT = ("SB-XIMU-PHYTO", "SB-XIMU-FUSA", "SB-THOI-RE", "SB-THOI-TRAI", "SB-SAU-DUC-TRAI")
SECTIONS = {
    "Dấu hiệu": "symptoms",
    "Biện pháp canh tác": "cultivation",
    "Hoạt chất khuyến cáo": "active_ingredients",
    "Thời gian cách ly (PHI)": "phi",
    "Sản phẩm ECO hỗ trợ": "eco_support",
    "Khi nào chuyển kỹ sư": "escalation",
}
SECTION_RE = re.compile(r"^(" + "|".join(map(re.escape, SECTIONS)) + r"):\s*", re.M)
ID_RE = re.compile(r"SB-[A-Z0-9-]+")
changes = []
issues = []


def normalized(value):
    if not isinstance(value, str):
        return value
    value = unicodedata.normalize("NFC", value).replace("\r\n", "\n").replace("\r", "\n")
    value = value.replace("\u00a0", " ").replace("\u200b", "").replace("\ufeff", "")
    value = "\n".join(re.sub(r"[ \t]+", " ", line).strip() for line in value.split("\n"))
    return re.sub(r"\n{3,}", "\n\n", value).strip() or None


def no_icons(text):
    # Preserve the meanings carried by the source's yes/no/warning symbols.
    for old, new in (("✅", "[có]"), ("❌", "[không]"), ("❓", "[cần xác minh]"),
                     ("⚠️", "Lưu ý:"), ("⚠", "Lưu ý:")):
        text = text.replace(old, new)
    text = re.sub("[\U0001f000-\U0001faff\u2600-\u27bf\ufe0f\u200d]", "", text)
    return normalized(text) or ""


def chunks(text, limit=900):
    result = []
    while len(text) > limit:
        split = text.rfind("\n", 0, limit + 1)
        if split < limit // 3:
            split = text.rfind(" ", 0, limit + 1)
        if split <= 0:
            split = limit
        result.append(text[:split].strip())
        text = text[split:].strip()
    if text:
        result.append(text)
    return result


def provenance(filename, sheet, row):
    return {"source_file": filename, "source_sheet": sheet, "source_row": row}


def issue(code, record, field, detail):
    issues.append({"code": code, "record_id": record.get("id") or record.get("ma_sp")
                   or record.get("ma_combo") or record.get("ma_hoi"),
                   "field": field, "detail": detail, **record["_source"]})


def records(workbook, filename, sheet_name, header_row):
    sheet = workbook[sheet_name]
    headers = [normalized(cell.value) for cell in sheet[header_row]]
    assert all(headers) and len(headers) == len(set(headers)), f"Invalid headers: {sheet_name}"
    first_data = header_row + (2 if header_row == 2 else 1)
    result = []
    seen = {}
    for row in sheet.iter_rows(min_row=first_data):
        raw = {field: cell.value for field, cell in zip(headers, row)}
        if all(value is None for value in raw.values()):
            continue
        item = {key: normalized(value) for key, value in raw.items()}
        item["_source"] = provenance(filename, sheet_name, row[0].row)
        for key in raw:
            if raw[key] != item[key]:
                changes.append({**item["_source"], "field": key, "before": raw[key], "after": item[key]})
        fingerprint = json.dumps({key: item[key] for key in headers}, sort_keys=True, ensure_ascii=False)
        if fingerprint in seen:
            issue("EXACT_DUPLICATE", item, "*", f"Identical business values to source row {seen[fingerprint]}; retained for traceability")
        seen[fingerprint] = row[0].row
        result.append(item)
    return headers, result


def set_text(cell, value):
    cell.value = value
    if isinstance(value, str):
        cell.data_type = "s"  # Never turn source strings into spreadsheet formulas.


def add_table(workbook, title, headers, rows):
    sheet = workbook.create_sheet(title)
    sheet.append(headers)
    for record in rows:
        for column, field in enumerate(headers, 1):
            value = record.get(field)
            if isinstance(value, (list, dict)):
                value = json.dumps(value, ensure_ascii=False)
            set_text(sheet.cell(sheet.max_row + 1, column) if column == 1 else sheet.cell(sheet.max_row, column), value)
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions
    for cell in sheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="256044")
    for column in sheet.columns:
        sheet.column_dimensions[column[0].column_letter].width = min(44, max(16, len(str(column[0].value)) + 2))


def flat_record(item):
    return {**{key: value for key, value in item.items() if not key.startswith("_")}, **item["_source"]}


def answer_sections(item):
    text = item["cau_tra_loi_mau"]
    matches = list(SECTION_RE.finditer(text))
    sections = []
    if not matches:
        issue("UNSTRUCTURED_ANSWER", item, "cau_tra_loi_mau", "No known section headers; original retained")
        matches = []
    if not matches or text[:matches[0].start()].strip():
        body = text[:matches[0].start()] if matches else text
        sections.append({"section_key": "original", "title": "Nội dung nguồn", "body_original": body.strip()})
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append({"section_key": SECTIONS[match.group(1)], "title": match.group(1),
                         "body_original": text[match.end():end].strip()})
    for index, section in enumerate(sections):
        section.update(disease_id=item["id"], position=index + 1,
                       body_display=no_icons(section["body_original"]), _source=item["_source"])
    return sections


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    AUDIT.mkdir(parents=True, exist_ok=True)
    sources = [{"filename": name, "sha256": hashlib.sha256((ROOT / name).read_bytes()).hexdigest()}
               for name in FILES]
    product_book = load_workbook(ROOT / FILES[0], data_only=False)
    disease_book = load_workbook(ROOT / FILES[1], data_only=False)
    tables = {}
    for name in ("SAN_PHAM", "COMBO", "HOI_DAP", "DANH_GIA"):
        tables[name] = records(product_book, FILES[0], name, 2)
    tables["DANH_MUC"] = records(product_book, FILES[0], "DANH_MUC", 1)
    for name in ("01_CAU_TRA_LOI", "02_NHOM_TRIEU_CHUNG", "03_CAU_HOI_PHAN_BIET"):
        tables[name] = records(disease_book, FILES[1], name, 1)
    products = tables["SAN_PHAM"][1]
    diagnoses = tables["01_CAU_TRA_LOI"][1]
    groups = tables["02_NHOM_TRIEU_CHUNG"][1]
    questions = tables["03_CAU_HOI_PHAN_BIET"][1]
    by_id = {item["id"]: item for item in diagnoses}
    assert len(by_id) == len(diagnoses), "Duplicate disease IDs require manual resolution"
    assert len({item["ma_sp"] for item in products}) == len(products), "Duplicate product IDs"
    assert set(PILOT) <= by_id.keys()

    for item in products:
        pack = item.get("quy_cach")
        match = re.fullmatch(r"(\d+(?:[.,]\d+)?)\s*(kg|g|ml|l)", pack or "", re.I)
        if match:
            unit = {"kg": "kg", "g": "g", "ml": "mL", "l": "L"}[match.group(2).lower()]
            after = f"{match.group(1)} {unit}"
            if after != pack:
                changes.append({**item["_source"], "field": "quy_cach", "before": pack, "after": after})
                item["quy_cach"] = after
        for key in ("cach_dung", "lieu_sau_rieng", "cong_dung_chatbot", "nguoi_duyet_ngay"):
            if item.get(key) is None:
                issue("MISSING_PRODUCT_FIELD", item, key, "Missing in source; no value inferred")
        if item.get("can_kiem_tra"):
            issue("SOURCE_REVIEW_NOTE", item, "can_kiem_tra", item["can_kiem_tra"])
        if item.get("trang_thai") == "Nháp":
            issue("SOURCE_DRAFT", item, "trang_thai", "Source status retained; not an added approval gate")
    by_registration = defaultdict(list)
    for item in products:
        if item.get("mspb"):
            by_registration[str(item["mspb"])].append(item["ma_sp"])
    for item in products:
        peers = by_registration[str(item.get("mspb"))]
        if len(peers) > 1:
            issue("SHARED_REGISTRATION", item, "mspb", "Same registration across " + ", ".join(peers) + "; not merged")
    by_name = {item["ten_eco"].casefold(): item["ma_sp"] for item in products}
    combo_components = []
    for item in tables["COMBO"][1]:
        for index in range(1, 5):
            if not item.get(f"sp_{index}"):
                continue
            name = item[f"sp_{index}"]
            product_id = by_name.get(name.casefold())
            combo_components.append({"combo_id": item["ma_combo"], "position": index,
                                     "source_name": name, "product_id": product_id,
                                     "dose_original": item.get(f"lieu_{index}")})
            if not product_id:
                issue("UNRESOLVED_PRODUCT", item, f"sp_{index}", f"No exact catalog match for {name}; no guessed alias")
            issue("DOSE_UNIT_MISSING", item, f"lieu_{index}", "Dose has no confirmed unit; kept as text")
    for item in tables["HOI_DAP"][1]:
        if not item.get("tra_loi"):
            issue("FAQ_NO_ANSWER", item, "tra_loi", "Question exists, answer is empty")

    all_sections = []
    for item in diagnoses:
        item["_data_tier"] = "raw" if str(item.get("trang_thai_goc_file_goc", "")).startswith("THO") else "standardized"
        if item["_data_tier"] == "raw":
            issue("RAW_SOURCE", item, "trang_thai_goc_file_goc", "Source says symptoms were taken from cause field; technical meaning not corrected automatically")
        all_sections.extend(answer_sections(item))
    candidate_rows = []
    coverage = set()
    group_by_id = {item["id"]: item for item in groups}
    question_by_id = {item["id"]: item for item in questions}
    for item in groups:
        ids = [part.strip() for part in item["id_ung_vien"].split(",")]
        item["_candidate_ids"] = ids
        coverage.update(ids)
        for disease_id in ids:
            if disease_id not in by_id:
                issue("BROKEN_CANDIDATE_REFERENCE", item, "id_ung_vien", disease_id)
            else:
                candidate_rows.append({"group_id": item["id"], "disease_id": disease_id})
        for crop in [part.strip() for part in item["cay_ap_dung"].split(",")]:
            if not any(by_id.get(disease_id, {}).get("cay") == crop for disease_id in ids):
                issue("CROP_WITHOUT_CANDIDATES", item, "cay_ap_dung", crop)
        if item["cau_hoi_dau_tien"] not in question_by_id:
            issue("BROKEN_FIRST_QUESTION", item, "cau_hoi_dau_tien", item["cau_hoi_dau_tien"])
    for item in questions:
        try:
            rules = json.loads(item["rules_json"])
            assert isinstance(rules, list)
        except (ValueError, AssertionError, TypeError):
            issue("INVALID_RULE_JSON", item, "rules_json", "Cannot parse as a rule list")
            rules = []
        item["_rules"] = rules
        group = group_by_id.get(item["nhom_trieu_chung"])
        if group is None:
            issue("BROKEN_GROUP_REFERENCE", item, "nhom_trieu_chung", item["nhom_trieu_chung"])
        branches = {rule.get("tra_loi"): rule for rule in rules}
        for label in ("co", "khong"):
            if label not in branches:
                issue("RULE_BRANCH_NOT_ENCODED", item, "rules_json", label)
        issue("UNKNOWN_BRANCH_NOT_ENCODED", item, "rules_json", "Unknown/unobserved response must preserve candidates and never act as no")
        for rule in rules:
            for disease_id in ID_RE.findall(json.dumps(rule)):
                if disease_id not in by_id:
                    issue("BROKEN_RULE_REFERENCE", item, "rules_json", disease_id)
                elif group and disease_id not in group["_candidate_ids"]:
                    issue("RULE_OUTSIDE_GROUP", item, "rules_json", disease_id)
        # Compare explicit exclusions only; do not guess medical/technical semantics.
        for label, field in (("co", "neu_tra_loi_co"), ("khong", "neu_tra_loi_khong")):
            text = item.get(field) or ""
            exclusion = re.search(r"(?:Loại|loại)\s+([^;(→>]+)", text)
            if exclusion:
                ids_text = set(ID_RE.findall(exclusion.group(1)))
                ids_json = set(branches.get(label, {}).get("loai", []))
                if ids_text != ids_json:
                    issue("TEXT_JSON_EXCLUSION_CONFLICT", item, field,
                          f"Text excludes {sorted(ids_text)}; JSON excludes {sorted(ids_json)}; neither silently overwritten")

    manifests = {}
    source_columns = ["source_file", "source_sheet", "source_row"]
    for source_name, names, filename in (
        (FILES[0], ("SAN_PHAM", "COMBO", "HOI_DAP", "DANH_GIA", "DANH_MUC"), "ECO_Du_lieu_san_pham.cleaned.xlsx"),
        (FILES[1], ("01_CAU_TRA_LOI", "02_NHOM_TRIEU_CHUNG", "03_CAU_HOI_PHAN_BIET"), "DB-Chatbot-Chan-Doan-Sau-Benh.cleaned.xlsx"),
    ):
        cleaned = Workbook()
        cleaned.remove(cleaned.active)
        add_table(cleaned, "CLEANING_INFO", ["key", "value"], [
            {"key": "source", "value": source_name},
            {"key": "policy", "value": "No approval gate added. Source status and technical meaning retained. Pilot is five selected IDs."},
            {"key": "chat_log", "value": "Excluded from knowledge; original retained in source and private audit only."},
            {"key": "rules", "value": "Source rules may conflict with prose; see data-quality-issues.csv. This is not a runtime engine."},
        ])
        original = product_book if source_name == FILES[0] else disease_book
        guide = "HUONG_DAN" if source_name == FILES[0] else "00_HUONG_DAN"
        sheet = cleaned.create_sheet(guide)
        for row in original[guide]:
            for cell in row:
                if cell.value is not None:
                    set_text(sheet.cell(cell.row, cell.column), normalized(cell.value))
        dictionary = []
        for name in names:
            headers, data = tables[name]
            add_table(cleaned, name, headers + source_columns, [flat_record(item) for item in data])
            if source_name == FILES[0] and name != "DANH_MUC":
                for column, field in enumerate(headers, 1):
                    dictionary.append({"sheet": name, "field": field,
                                       "group": normalized(original[name].cell(1, column).value),
                                       "source_instruction": normalized(original[name].cell(3, column).value)})
        if dictionary:
            add_table(cleaned, "DATA_DICTIONARY", ["sheet", "field", "group", "source_instruction"], dictionary)
        if source_name == FILES[1]:
            add_table(cleaned, "NOI_DUNG_THEO_MUC", ["disease_id", "section_key", "position", "title", "body_original", "body_display"] + source_columns,
                      [flat_record(item) for item in all_sections])
        cleaned.save(OUT / filename)
        cleaned.close()
        manifests[filename] = {"source": source_name, "sheets": {name: len(tables[name][1]) for name in names}}

    with (OUT / "normalized-records.jsonl").open("w", encoding="utf-8") as stream:
        for name, (_, data) in tables.items():
            for item in data:
                stream.write(json.dumps({"entity": name, **flat_record(item)}, ensure_ascii=False, default=str) + "\n")
    database_path = OUT / "eco_agro.sqlite"
    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys = ON")
    # Only our generated staging schema is recreated, inside its own output database.
    connection.executescript("""
        DROP TABLE IF EXISTS pilot_members;
        DROP TABLE IF EXISTS answer_sections;
        DROP TABLE IF EXISTS questions;
        DROP TABLE IF EXISTS group_candidates;
        DROP TABLE IF EXISTS symptom_groups;
        DROP TABLE IF EXISTS diseases;
        DROP TABLE IF EXISTS combo_components;
        DROP TABLE IF EXISTS combos;
        DROP TABLE IF EXISTS faqs;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS sources;
        CREATE TABLE sources(id INTEGER PRIMARY KEY, filename TEXT UNIQUE NOT NULL, sha256 TEXT NOT NULL);
        CREATE TABLE products(id TEXT PRIMARY KEY, name TEXT NOT NULL, pack_size TEXT, registration_code TEXT,
            source_status TEXT, source_id INTEGER NOT NULL REFERENCES sources(id), source_sheet TEXT, source_row INTEGER,
            fields_json TEXT NOT NULL CHECK(json_valid(fields_json)));
        CREATE TABLE combos(id TEXT PRIMARY KEY, name TEXT, fields_json TEXT NOT NULL CHECK(json_valid(fields_json)));
        CREATE TABLE combo_components(combo_id TEXT REFERENCES combos(id), position INTEGER, source_name TEXT,
            product_id TEXT REFERENCES products(id), dose_original TEXT, PRIMARY KEY(combo_id,position));
        CREATE TABLE faqs(id TEXT PRIMARY KEY, question TEXT NOT NULL, answer TEXT, fields_json TEXT NOT NULL CHECK(json_valid(fields_json)));
        CREATE TABLE diseases(id TEXT PRIMARY KEY, crop TEXT NOT NULL, name TEXT NOT NULL, data_tier TEXT NOT NULL,
            source_status TEXT, legacy_status TEXT, answer_original TEXT NOT NULL,
            source_id INTEGER NOT NULL REFERENCES sources(id), source_sheet TEXT, source_row INTEGER,
            fields_json TEXT NOT NULL CHECK(json_valid(fields_json)));
        CREATE TABLE answer_sections(disease_id TEXT REFERENCES diseases(id), section_key TEXT, position INTEGER,
            title TEXT NOT NULL, body_original TEXT NOT NULL, body_display TEXT NOT NULL,
            PRIMARY KEY(disease_id,section_key));
        CREATE TABLE symptom_groups(id TEXT PRIMARY KEY, crops_json TEXT NOT NULL CHECK(json_valid(crops_json)),
            fields_json TEXT NOT NULL CHECK(json_valid(fields_json)));
        CREATE TABLE group_candidates(group_id TEXT REFERENCES symptom_groups(id), disease_id TEXT REFERENCES diseases(id),
            PRIMARY KEY(group_id,disease_id));
        CREATE TABLE questions(id TEXT PRIMARY KEY, group_id TEXT REFERENCES symptom_groups(id), text TEXT NOT NULL,
            rules_json TEXT NOT NULL CHECK(json_valid(rules_json)), source_fields_json TEXT NOT NULL CHECK(json_valid(source_fields_json)),
            rule_state TEXT NOT NULL DEFAULT 'source_unresolved');
        CREATE TABLE pilot_members(disease_id TEXT PRIMARY KEY REFERENCES diseases(id));
        CREATE INDEX diseases_crop_idx ON diseases(crop);
        CREATE INDEX questions_group_idx ON questions(group_id);
        PRAGMA user_version = 1;
    """)
    for index, source in enumerate(sources, 1):
        connection.execute("INSERT INTO sources VALUES (?,?,?)", (index, source["filename"], source["sha256"]))
    for item in products:
        connection.execute("INSERT INTO products VALUES (?,?,?,?,?,?,?,?,?)",
                           (item["ma_sp"], item["ten_eco"], item["quy_cach"], item.get("mspb"), item.get("trang_thai"),
                            1, item["_source"]["source_sheet"], item["_source"]["source_row"], json.dumps(flat_record(item), ensure_ascii=False)))
    for item in tables["COMBO"][1]:
        connection.execute("INSERT INTO combos VALUES (?,?,?)", (item["ma_combo"], item["ten_combo"], json.dumps(flat_record(item), ensure_ascii=False)))
    for item in combo_components:
        connection.execute("INSERT INTO combo_components VALUES (?,?,?,?,?)", tuple(item[key] for key in ("combo_id", "position", "source_name", "product_id", "dose_original")))
    for item in tables["HOI_DAP"][1]:
        connection.execute("INSERT INTO faqs VALUES (?,?,?,?)", (item["ma_hoi"], item["cau_hoi"], item.get("tra_loi"), json.dumps(flat_record(item), ensure_ascii=False)))
    for item in diagnoses:
        connection.execute("INSERT INTO diseases VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                           (item["id"], item["cay"], item["ten"], item["_data_tier"], item["trang_thai"], item.get("trang_thai_goc_file_goc"),
                            item["cau_tra_loi_mau"], 2, item["_source"]["source_sheet"], item["_source"]["source_row"], json.dumps(flat_record(item), ensure_ascii=False)))
    for section in all_sections:
        connection.execute("INSERT INTO answer_sections VALUES (?,?,?,?,?,?)", tuple(section[key] for key in
                           ("disease_id", "section_key", "position", "title", "body_original", "body_display")))
    for item in groups:
        connection.execute("INSERT INTO symptom_groups VALUES (?,?,?)", (item["id"], json.dumps(item["cay_ap_dung"].split(", "), ensure_ascii=False), json.dumps(flat_record(item), ensure_ascii=False)))
    for item in candidate_rows:
        connection.execute("INSERT INTO group_candidates VALUES (?,?)", (item["group_id"], item["disease_id"]))
    for item in questions:
        connection.execute("INSERT INTO questions(id,group_id,text,rules_json,source_fields_json) VALUES (?,?,?,?,?)",
                           (item["id"], item["nhom_trieu_chung"], item["cau_hoi_ngan"], json.dumps(item["_rules"], ensure_ascii=False), json.dumps(flat_record(item), ensure_ascii=False)))
    connection.executemany("INSERT INTO pilot_members VALUES (?)", [(value,) for value in PILOT])
    connection.commit()
    assert connection.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    assert not connection.execute("PRAGMA foreign_key_check").fetchall()
    connection.close()

    preview = []
    display_fields = (("tac_nhan", "Tác nhân theo nguồn"), ("bo_phan", "Bộ phận"), ("dieu_kien", "Điều kiện"),
                      ("giai_doan", "Giai đoạn"), ("tac_hai", "Tác hại"), ("nguon", "Nguồn tham khảo"))
    for disease_id in PILOT:
        item = by_id[disease_id]
        # Short first message is a separate field, never an LLM paraphrase at runtime.
        first_sign = item["dau_hieu"].split("\n")[0].lstrip("- ")
        messages = [f"Đối chiếu tham khảo: {item['ten']}.\nDấu hiệu theo mẫu: {no_icons(first_sign)}\nMã hồ sơ: {disease_id}."]
        for section in [s for s in all_sections if s["disease_id"] == disease_id]:
            messages.extend(chunks(f"{section['title']}\n{section['body_display']}"))
        for field, title in display_fields:
            if item.get(field):
                messages.extend(chunks(f"{title}\n{no_icons(item[field])}"))
        preview.append({"disease_id": disease_id, "name": item["ten"], "messages": messages,
                        "delivery": "Preview only. Runtime section selection/order and outbound pacing are not implemented."})
    write_json(OUT / "pilot-message-preview.json", preview)
    write_json(AUDIT / "cell-changes.json", changes)
    write_json(OUT / "data-quality-issues.json", issues)
    with (OUT / "data-quality-issues.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["code", "record_id", "field", "detail"] + source_columns)
        writer.writeheader()
        writer.writerows(issues)
    for source in sources:
        assert hashlib.sha256((ROOT / source["filename"]).read_bytes()).hexdigest() == source["sha256"], "Original changed"
    log_count = sum(any(cell.value is not None for cell in row) for row in disease_book["NHAT_KY_CHAT"].iter_rows(min_row=2))
    summary = {
        "schema_version": 1, "sources": sources, "outputs": manifests,
        "counts": {name: len(value[1]) for name, value in tables.items()},
        "pilot_ids": list(PILOT), "cell_changes": len(changes),
        "issue_counts": dict(sorted(Counter(item["code"] for item in issues).items())),
        "diagnosis_crops": dict(Counter(item["cay"] for item in diagnoses)),
        "data_tiers": dict(Counter(item["_data_tier"] for item in diagnoses)),
        "source_group_coverage": len(coverage),
        "diagnoses_outside_source_groups": len(diagnoses) - len(coverage),
        "chat_log_messages_excluded": log_count,
        "source_bytes_unchanged": True,
        "business_facts_verified_externally": False,
        "approval_gate_required": False,
        "runtime_implemented": False,
    }
    write_json(OUT / "manifest.json", summary)
    product_book.close()
    disease_book.close()
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
