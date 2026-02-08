import pandas as pd
import json
import yaml
from parser import parse_entry


INPUT_CSV = "dictionary.csv"

OUTPUT_JSON = "dictionary.json"
OUTPUT_YAML = "dictionary.yaml"

OUTPUT_ENTRIES_CSV = "entries.csv"
OUTPUT_MEANINGS_CSV = "meanings.csv"
OUTPUT_CROSSREF_CSV = "cross_references.csv"
OUTPUT_ETYMOLOGY_CSV = "etymology.csv"


def process_csv(csv_path: str):
    df = pd.read_csv(csv_path)

    parsed_entries = []

    for _, row in df.iterrows():
        parsed = parse_entry(row["ResultText"])

        # Preserve original CSV identifiers
        parsed["_csv_id"] = row.get("ID")
        parsed["_csv_name"] = row.get("NAME")

        parsed_entries.append(parsed)

    return parsed_entries


def write_json_yaml(entries):
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

    with open(OUTPUT_YAML, "w", encoding="utf-8") as f:
        yaml.dump(entries, f, allow_unicode=True, sort_keys=False)


def write_hybrid_csv(entries):
    entry_rows = []
    meaning_rows = []
    crossref_rows = []
    etymology_rows = []

    for entry in entries:
        entry_id = entry.get("_csv_id")

        # -------- ENTRY LEVEL --------
        entry_rows.append({
            "csv_id": entry_id,
            "headword": entry["headword"],
            "headword_id": entry["headword_id"],
            "transliteration": entry["transliteration"],
            "pos_tamil": entry["pos_tamil"],
            "pos_english": entry["pos_english"],
        })

        # -------- MEANINGS --------
        for idx, m in enumerate(entry["meanings"], start=1):
            meaning_rows.append({
                "csv_id": entry_id,
                "meaning_index": idx,
                "meaning_number": m["meaning_number"],
                "tamil": m["tamil"],
                "tamil_italics": " | ".join(m["tamil_italics"]),
                "english": m["english"],
                "source": m["source"],
                "source_extra": m["source_extra"],
            })

        # -------- CROSS REFERENCES --------
        for cr in entry["cross_references"]:
            crossref_rows.append({
                "csv_id": entry_id,
                "cross_reference": cr,
            })

        # -------- ETYMOLOGY --------
        for idx, et in enumerate(entry["etymology"], start=1):
            etymology_rows.append({
                "csv_id": entry_id,
                "line_no": idx,
                "etymology_text": et,
            })

    # Write CSVs
    pd.DataFrame(entry_rows).to_csv(OUTPUT_ENTRIES_CSV, index=False)
    pd.DataFrame(meaning_rows).to_csv(OUTPUT_MEANINGS_CSV, index=False)
    pd.DataFrame(crossref_rows).to_csv(OUTPUT_CROSSREF_CSV, index=False)
    pd.DataFrame(etymology_rows).to_csv(OUTPUT_ETYMOLOGY_CSV, index=False)


if __name__ == "__main__":
    entries = process_csv(INPUT_CSV)

    write_json_yaml(entries)
    write_hybrid_csv(entries)

    print(f"Processed {len(entries)} dictionary entries")
    print("Outputs written:")
    print(f" - {OUTPUT_JSON}")
    print(f" - {OUTPUT_YAML}")
    print(f" - {OUTPUT_ENTRIES_CSV}")
    print(f" - {OUTPUT_MEANINGS_CSV}")
    print(f" - {OUTPUT_CROSSREF_CSV}")
    print(f" - {OUTPUT_ETYMOLOGY_CSV}")
