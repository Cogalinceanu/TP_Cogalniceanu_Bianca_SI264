import os
from arsenal.forensics.amprente import tip, amprenta_fisier, scaneaza, amprente_lenes

PROBE = os.path.join(os.path.dirname(__file__), "probe")


def test_tip_din_magic():
    assert tip(b"\x89PNG") == "PNG"
    assert tip(b"%PDF-1.4") == "PDF"
    assert tip(b"PK\x03\x04") == "ZIP"
    assert tip(b"text") == "necunoscut"


def test_amprenta_png():
    r = amprenta_fisier(os.path.join(PROBE, "imagine.png"))
    assert r["sha256"] == "ea3a9848da7e6c1d"
    assert r["tip"] == "PNG"


def test_scaneaza_toate():
    rez = scaneaza(PROBE)
    assert len(rez) == 4
    assert {f["tip"] for f in rez} == {"PNG", "PDF", "ZIP", "necunoscut"}
    assert list(amprente_lenes(PROBE)) == rez
