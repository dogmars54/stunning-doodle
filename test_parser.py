from parser import parse_entry


def test_headword_and_super():
    text = "<Red>அக்கரம்</Red><Super>2</Super>"
    e = parse_entry(text)
    assert e["headword"] == "அக்கரம்"
    assert e["headword_id"] == "2"


def test_transliteration():
    text = "<Blue_Italic><myfirstfont_13>akkaram,</myfirstfont_13></Blue_Italic>"
    e = parse_entry(text)
    assert e["transliteration"] == "akkaram,"


def test_pos_split():
    text = "<Green>பெ. <myfirstfont_13>(n.)</myfirstfont_13></Green>"
    e = parse_entry(text)
    assert e["pos_tamil"] == "பெ."
    assert e["pos_english"] == "n."


def test_meaning_number():
    text = "<Three_Space>12. சுற்று;<Blue_Italic><myfirstfont_13>cycle</myfirstfont_13></Blue_Italic>"
    e = parse_entry(text)
    m = e["meanings"][0]
    assert m["meaning_number"] == "12"
    assert m["tamil"] == "சுற்று"


def test_tamil_italics():
    text = "<Three_Space>குளம் <Italics>(பிங்.)</Italics>;"
    e = parse_entry(text)
    assert "(பிங்.)" in e["meanings"][0]["tamil_italics"]


def test_source_and_extra():
    text = """
    <Three_Space>குளம்
    <BR><BR>
    <Five_Space><Italics>Source</Italics>.{U, test}.
    """
    e = parse_entry(text)
    m = e["meanings"][0]
    assert m["source"] == "Source"
    assert m["source_extra"] == "{U, test}."


def test_cross_reference():
    text = "அக்கரகாரம் பார்க்க ;see akkara-karam."
    e = parse_entry(text)
    assert len(e["cross_references"]) == 1


def test_etymology_block():
    text = """
    <BR><BR>
    த. வட்டம் → Skt. வ்ருத்த
    <BR><BR>
    """
    e = parse_entry(text)
    assert "வட்டம்" in e["etymology"][0]


def test_english_continuation():
    text = """
    <Three_Space>குளம்;<Blue_Italic><myfirstfont_13>pond</myfirstfont_13></Blue_Italic>
    <BR><BR>
    <Blue_Italic><myfirstfont_13>water body</myfirstfont_13></Blue_Italic>
    """
    e = parse_entry(text)
    assert "water body" in e["meanings"][0]["english"]
