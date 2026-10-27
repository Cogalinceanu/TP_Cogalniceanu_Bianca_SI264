from arsenal.forensics.decode import desfa, ghici_strat, citibil


def test_base64():
    strat, b = desfa("U2FsdXQ=")
    assert strat == "base64"
    assert b == b"Salut"


def test_hex():
    strat, b = desfa("48656c6c6f")
    assert strat == "hex"
    assert b == b"Hello"


def test_url():
    strat, b = desfa("%2Fetc")
    assert strat == "url"
    assert b == b"/etc"


def test_citibil():
    assert citibil(b"Salut!")
    assert not citibil(b"\x00\xff")


def test_ghici_strat():
    assert ghici_strat("%2Fetc") == "url"
    assert ghici_strat("48656c6c6f") == "hex"
    assert ghici_strat("U2FsdXQ=") == "base64"
