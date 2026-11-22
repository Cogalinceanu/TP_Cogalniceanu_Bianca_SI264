"""Teste automate pentru Laboratorul 11."""
import json
from pathlib import Path

from arsenal.windows.inventar import (Eveniment, Inventar, Proces,
                                     construieste_raport, evenimente_din_json,
                                     procese_din_json)

START = Path(__file__).parent / "start"


def test_proces_din_temp_e_suspect():
    assert Proces(1, "x.exe", "ana", r"C:\Users\ana\AppData\Local\Temp\x.exe").e_suspect() is True


def test_proces_din_windows_nu_e_suspect():
    assert Proces(2, "svchost.exe", "SYSTEM", r"C:\Windows\System32\svchost.exe").e_suspect() is False


def test_roaming_e_suspect():
    assert Proces(3, "x.exe", "ana", r"C:\Users\ana\AppData\Roaming\x.exe").e_suspect()


def test_cale_insensibila_la_litere_mari():
    assert Proces(4, "x.exe", "ana", r"C:\USERS\ANA\TEMP\x.exe").e_suspect()


def test_evenimente_suspecte():
    for cod in (4625, 1102, 7045):
        assert Eveniment(cod, "info", "Security", "ana", "test").e_suspect()
    assert Eveniment(1, "critical", "Security", "ana", "test").e_suspect()
    assert not Eveniment(4624, "info", "Security", "ana", "test").e_suspect()


def test_egalitate_dataclass():
    assert Proces(1, "a.exe", "ana", "x") == Proces(1, "a.exe", "ana", "x")
    assert Proces(1, "a.exe", "ana", "x") != Proces(2, "a.exe", "ana", "x")


def test_incarcare_capturi():
    assert len(procese_din_json(START / "procese.json")) == 7
    assert len(evenimente_din_json(START / "evenimente.json")) == 8


def test_inventar_suspecte_si_grupare():
    inv = Inventar.din_json(START / "procese.json")
    assert len(inv) == 7
    assert [p.pid for p in inv.suspecte()] == [3120, 3890]
    assert inv.pe_user()["SYSTEM"] == ["System", "svchost.exe"]
    assert len(inv.pe_user()["ana"]) == 5


def test_raport_si_scor():
    inv = Inventar.din_json(START / "procese.json")
    ev = evenimente_din_json(START / "evenimente.json")
    raport = construieste_raport(inv, ev)
    assert raport["total_procese_suspecte"] == 2
    assert raport["total_alarme"] == 5
    assert raport["scor_risc"] == 7
    assert len(json.dumps(raport)) > 0


def test_explicatii():
    assert "brute force" in Eveniment(4625, "warning", "Security", "ana", "").explica()
    assert "sters" in Eveniment(1102, "critical", "Security", "ana", "").explica()


def test_fisier_json_invalid(tmp_path):
    fisier = tmp_path / "invalid.json"
    fisier.write_text('{"nu": "lista"}', encoding="utf-8")
    try:
        procese_din_json(fisier)
    except ValueError:
        pass
    else:
        raise AssertionError("Trebuia sa fie respins JSON-ul care nu este lista")
