"""Teste automate pentru ambele lucrari, inclusiv cazuri limita."""
from collections import Counter
import json
import subprocess
import sys
from pathlib import Path
import pytest
from arsenal.aparare.parse_auth import esec, citeste_esecuri, pe_ip
from arsenal.aparare.detector import suspecti, genereaza_raport

LOG = Path(__file__).parent / "start" / "auth.log"


def test_pragul_taie():
    c = Counter({"a": 13, "b": 2})
    assert suspecti(c, 10) == [("a", 13)]
    assert suspecti(c, 2) == [("a", 13), ("b", 2)]


def test_prag_invalid():
    with pytest.raises(ValueError, match="prag invalid: 0"):
        suspecti({}, 0)


def test_esec_valid_si_invalid():
    assert esec("Failed password for root from 203.0.113.9 port 51230 ssh2") == ("root", "203.0.113.9")
    assert esec("Failed password for invalid user admin from 203.0.113.9 port 12 ssh2") == ("admin", "203.0.113.9")
    assert esec("<linie stricata fara structura>") is None
    assert esec("Accepted password for ana from 192.168.56.10 port 42 ssh2") is None


def test_numarare_jurnal():
    esecuri = citeste_esecuri(LOG)
    assert len(esecuri) == 15
    assert pe_ip(esecuri) == Counter({"203.0.113.9": 13, "198.51.100.7": 2})


def test_fisier_inexistent(capsys, tmp_path):
    assert citeste_esecuri(tmp_path / "lipsa.log") == []
    assert "nu gasesc" in capsys.readouterr().out


def test_raport_json():
    raport = genereaza_raport(citeste_esecuri(LOG))
    assert raport["esecuri"] == 15
    assert raport["suspecti"] == [{"ip": "203.0.113.9", "incercari": 13}]
    assert json.loads(json.dumps(raport)) == raport


def test_cli_json():
    rezultat = subprocess.run([sys.executable, "-m", "arsenal.aparare.detector", str(LOG), "--json"],
                              capture_output=True, text=True, check=True)
    assert json.loads(rezultat.stdout)["esecuri"] == 15


def test_prag_negativ_si_bool():
    for prag in (-1, True):
        with pytest.raises(ValueError):
            suspecti({}, prag)
