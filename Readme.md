# Tamil Dictionary Parser (SQL/CSV → Structured Data)

---🤖 AI Assistance Disclosure

AI assistance was used in the development of this project.

Specifically:
	Large Language Models (LLMs) were used as a coding and design assistant:
		to help formalize parsing rules
		to refactor and validate Python code
		to generate documentation and tests
		
Important clarifications:
	The parsing rules, logic, and linguistic decisions were provided and validated by the project author.
	No training data from this dictionary was used to train any AI model.
	The parser itself is fully deterministic and rule-based.
	AI did not generate or infer dictionary content.

AI was used as a tool, not as an authority.

---

This repository contains a **rule-based parser** for processing a legacy Tamil dictionary dataset originally stored as SQL and later converted to CSV.  
The parser extracts **structured linguistic data** (headwords, meanings, sources, etymology, cross-references, etc.) from a single complex text field that uses custom inline tags.

The project is designed for **accuracy, data preservation, and scholarly use**, not heuristic guessing.

---

## ✨ Features

- Parses a single complex CSV field (`ResultText`) into structured data
- Supports:
  - Headword and headword ID (`<Red>`, `<Super>`)
  - Transliteration
  - Tamil & English parts of speech
  - Single-meaning and multi-meaning entries
  - Meaning numbering (robust to misformatting)
  - Tamil meanings with preserved italics
  - English meanings and continuations
  - Sources and source annotations
  - Etymology blocks (multiple lines)
  - Cross-references (`see` / `பார்க்க`)
- Preserves **editorial fidelity** while also producing **normalized fields**
- Outputs:
  - JSON
  - YAML
  - Hybrid normalized CSVs (entry-level, meaning-level, etymology, cross-references)
- Fully rule-based (no ML guessing at parse time)
- Includes automated unit tests (pytest)

---

## 📁 Repository Structure

├── parser.py # Core rule-based parser

├── run_parser.py # CSV → JSON / YAML / Hybrid CSV pipeline

├── test_parser.py # Pytest unit tests

├── requirements.txt # Python dependencies

├── README.md


---

## 🧠 Parsing Philosophy

This project follows three core principles:

1. **Faithful extraction first**
   - The parser does not "fix" or normalize content aggressively.
   - Misformatted data is preserved for later correction.

2. **Explicit rules, not heuristics**
   - Every decision is driven by documented tag patterns and structural rules.

3. **Separation of concerns**
   - Parsing ≠ correction ≠ analysis.
   - Metadata (e.g., meaning numbers, italics) is preserved to support later cleanup.

---

## 🏷️ Tag Semantics (Simplified)

| Tag | Meaning |
|----|--------|
| `<Red>` | Headword |
| `<Super>` | Headword ID (disambiguates identical headwords) |
| `<Blue_Italic><myfirstfont_13>` | Transliteration / English meaning |
| `<Green>` | Parts of speech |
| `<Three_Space>` | Meaning start (context-dependent) |
| `<Five_Space><Italics>` | Source |
| `<Five_Space>` (no italics) | Etymology |
| `<Italics>` | Tamil annotation / source / emphasis |
| `<BR><BR>` | Logical line break |

---

## 📦 Installation

### Requirements

- Python 3.9+
- pandas
- PyYAML
- pytest (for tests)

Install dependencies:

```bash
pip install -r requirements.txt

---

Usage

Input

A CSV file with at least this column: ID,NAME,ResultText

Where ResultText contains tagged dictionary content.

Run the parser - python run_parser.py


This generates:
	dictionary.json
	dictionary.yaml
	entries.csv
	meanings.csv
	cross_references.csv
	etymology.csv
	
JSON / YAML Output

Each dictionary entry is represented as structured data, for example:

	{
  "headword": "வட்டம்",
  "headword_id": "2",
  "meanings": [
    {
      "meaning_number": "1",
      "tamil_raw": "மண்டலம் <Italics>(பிங்.)</Italics>",
      "tamil": "மண்டலம்",
      "tamil_italics": ["(பிங்.)"],
      "english": "circle",
      "source": null
    }
  ],
  "etymology": [
    "த. வட்டம் → Skt. வ்ருத்த"
  ]
}

---

Hybrid CSV Output (Recommended)


+----------------------+------------------------------+
| File                 | Description                  |
+----------------------+------------------------------+
| meanings.csv         | One row per meaning          |
+----------------------+------------------------------+
| cross_references.csv | All cross-references         |
+----------------------+------------------------------+
| etymology.csv        | Multi-line etymology         |
+----------------------+------------------------------+
| entries.csv          | One row per dictionary entry |
+----------------------+------------------------------+


This structure is suitable for:
	SQL databases
	Linguistic analysis
	Search indexing
	Manual editorial review


🧪 Running Tests
	pytest test_parser.py
	
	Tests include:
		Header/body separation
		Single vs multi-meaning logic
		Source vs etymology detection
		Cross-reference exceptions
		Regression tests for known edge cases
		


⚠️ Known Limitations
	The parser assumes the legacy tag conventions are consistent.
	Extremely malformed entries may require post-processing.
	The parser does not attempt semantic correction or deduplication.
	These are intentional design decisions.


