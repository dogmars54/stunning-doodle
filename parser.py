import re
from typing import List, Dict, Optional

BR_SPLIT = "<BR><BR>"


def clean_text(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"<[^>]+>", "", text).strip()


def extract_first(pattern: str, text: str) -> Optional[str]:
    m = re.search(pattern, text, re.DOTALL)
    return m.group(1).strip() if m else None


def split_lines(text: str) -> List[str]:
    return [line.strip() for line in text.split(BR_SPLIT) if line.strip()]


def contains_see_and_parka(text: str) -> bool:
    return "see" in text.lower() and "பார்க்க" in text


def is_blue_italic_only(line: str) -> bool:
    return (
        line.startswith("<Blue_Italic>")
        and "<Three_Space>" not in line
        and "<Five_Space>" not in line
    )


def parse_entry(text: str) -> Dict:
    entry = {
        "headword": None,
        "headword_id": None,
        "transliteration": None,
        "pos_tamil": None,
        "pos_english": None,
        "meanings": [],
        "etymology": [],
        "cross_references": [],
    }

    # ================= HEADER =================
    entry["headword"] = extract_first(r"<Red>(.*?)</Red>", text)
    entry["headword_id"] = extract_first(r"<Super>(.*?)</Super>", text)

    entry["transliteration"] = extract_first(
        r"<Blue_Italic><myfirstfont_13>(.*?)</myfirstfont_13></Blue_Italic>",
        text,
    )

    green = extract_first(r"<Green>(.*?)</Green>", text)
    if green:
        entry["pos_english"] = extract_first(
            r"<myfirstfont_13>\(?([^)]+)\)?</myfirstfont_13>", green
        )
        entry["pos_tamil"] = clean_text(
            re.sub(r"<myfirstfont_13>.*?</myfirstfont_13>", "", green)
        )

    # ================= BODY =================
    parts = text.split(BR_SPLIT, 1)
    body_text = parts[1] if len(parts) > 1 else ""
    lines = split_lines(body_text)

    # Phase A: detect multi-meaning
    has_numbered_meaning = any(
        line.startswith("<Three_Space>")
        and re.match(r"<Three_Space>\s*\d+\.", line)
        for line in lines
    )

    current_meaning = None
    meaning_count = 0

    # Phase B: parse
    for line in lines:
        if line.startswith("<Three_Space>"):
            raw_content = line.replace("<Three_Space>", "").strip()
            content = raw_content

            mnum = extract_first(r"^(\d+)\.", content)

            # multi-meaning rules
            if has_numbered_meaning and mnum:
                content = content[len(mnum) + 1 :].strip()
            elif not has_numbered_meaning:
                if meaning_count > 0:
                    entry["etymology"].append(clean_text(content))
                    continue
            elif has_numbered_meaning and not mnum:
                entry["etymology"].append(clean_text(content))
                continue

            meaning_count += 1
            current_meaning = {
                "meaning_number": mnum,
                "tamil_raw": clean_text(raw_content),
                "tamil": "",
                "tamil_italics": [],
                "english": "",
                "source": None,
                "source_extra": None,
            }

            # extract tamil italics
            italics = re.findall(r"<Italics>(.*?)</Italics>", content, re.DOTALL)
            if italics:
                current_meaning["tamil_italics"].extend(
                    [clean_text(i) for i in italics]
                )
                content = re.sub(
                    r"<Italics>.*?</Italics>", "", content, flags=re.DOTALL
                )

            # extract english meaning
            eng = extract_first(
                r"<Blue_Italic><myfirstfont_13>(.*?)</myfirstfont_13></Blue_Italic>",
                content,
            )
            if eng:
                current_meaning["english"] = clean_text(eng)
                content = re.sub(
                    r"<Blue_Italic>.*?</Blue_Italic>", "", content, flags=re.DOTALL
                )

            current_meaning["tamil"] = clean_text(content).rstrip(";")
            entry["meanings"].append(current_meaning)
            continue

        # ---------- SOURCE ----------
        if line.startswith("<Five_Space>") and "<Italics>" in line:
            if current_meaning:
                src = extract_first(r"<Italics>(.*?)</Italics>", line)
                current_meaning["source"] = clean_text(src)

                outside = re.sub(
                    r"<Italics>.*?</Italics>", "", line, flags=re.DOTALL
                )
                outside = clean_text(outside)
                if outside:
                    current_meaning["source_extra"] = outside
            continue

        # ---------- FIVE_SPACE without italics ----------
        if line.startswith("<Five_Space>"):
            entry["etymology"].append(clean_text(line))
            continue

        # ---------- CROSS REFERENCE ----------
        if contains_see_and_parka(line):
            entry["cross_references"].append(clean_text(line))
            continue

        # ---------- ENGLISH CONTINUATION ----------
        if is_blue_italic_only(line) and current_meaning:
            cont = extract_first(
                r"<Blue_Italic><myfirstfont_13>(.*?)</myfirstfont_13></Blue_Italic>",
                line,
            )
            if cont:
                current_meaning["english"] += " " + clean_text(cont)
            continue

        # ---------- FALLBACK ----------
        if meaning_count > 0:
            entry["etymology"].append(clean_text(line))

    return entry
