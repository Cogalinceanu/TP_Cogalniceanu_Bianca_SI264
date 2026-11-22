"""Teste offline pentru lucrarile A si B (pytest)."""
import json
from pathlib import Path
from arsenal.privesc.enum import citeste_linii, nume, suid_constatari, sudo_constatari, cron_constatari, enumereaza, utilizatori_implicati, grupare_dupa_risc, main
from arsenal.privesc.diferenta import cai, compara

START = Path(__file__).parent / "start"


def test_doar_ce_e_nou():
    acum = {"a", "b", "c"}
    baza = {"a", "b"}
    assert acum - baza == {"c"}


def test_a1_a2_linii_si_nume():
    linii = citeste_linii(START / "suid.txt")
    assert len(linii) == 14
    assert len({nume(c) for c in linii}) == 13


def test_a3_suid_risc():
    rezultat = suid_constatari(START / "suid.txt")
    assert len(rezultat) == 13
    assert sorted(c["nume"] for c in rezultat if c["risc"] == "mare") == ["cp", "find", "nmap", "vim.basic"]


def test_a4_sudo_cron():
    sudo = sudo_constatari(START / "sudo.txt")
    cron = cron_constatari(START / "crontab.txt")
    assert len(sudo) == 3 and sum(c["risc"] == "mare" for c in sudo) == 2
    assert len(cron) == 3 and cron[0]["user"] == "root"
    assert cron[0]["comanda"] == "cd / && run-parts --report /etc/cron.hourly"


def test_a5_raport():
    raport = enumereaza(START)
    assert list(raport) == ["suid", "sudo", "cron"]
    assert utilizatori_implicati(raport) == {"ana", "root", "www-data"}
    assert len(grupare_dupa_risc(raport)["mare"]) == 6
    assert json.loads(json.dumps(raport)) == raport


def test_b1_b2_b3_diferenta():
    baza, acum, noi, risc, periculoase = compara(START / "baza_suid.txt", START / "suid.txt")
    assert (len(baza), len(acum), len(noi)) == (9, 13, 4)
    assert periculoase == ["/bin/cp", "/usr/bin/find", "/usr/bin/nmap", "/usr/bin/vim.basic"]
    assert set(risc.values()) == {"mare"}


def test_optiuni_json_si_risc(capsys):
    main([str(START), "--json"])
    rezultat = json.loads(capsys.readouterr().out)
    assert len(rezultat["suid"]) == 13
    main([str(START), "--json", "--risc", "mare"])
    filtrat = json.loads(capsys.readouterr().out)
    assert (len(filtrat["suid"]), len(filtrat["sudo"]), len(filtrat["cron"])) == (4, 2, 0)


def test_citire_comentarii_si_dubluri(tmp_path):
    fisier = tmp_path / "exemplu.txt"
    fisier.write_text("# comentariu\n\n /bin/cp \n/bin/cp\n", encoding="utf-8")
    assert citeste_linii(fisier) == ["/bin/cp", "/bin/cp"]
    assert cai(fisier) == {"/bin/cp"}
