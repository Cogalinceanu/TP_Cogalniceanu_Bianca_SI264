# Laboratorul 13 — with si pytest

Deschide folderul Laboratorul_13 in VS Code si terminalul PowerShell in radacina lui.

```powershell
python -m pip install -r requirements.txt
python VERIFICARE_AUTOMATA.py
```

## Comenzi individuale

A1: `python -c "from arsenal.forensics.amprente import tip; print(tip(bytes.fromhex('89504e47')), tip(b'%PDF-1.4'), tip(b'text'))"`

A2: `python -c "from arsenal.forensics.amprente import amprenta_fisier; print(amprenta_fisier('arsenal/forensics/probe/imagine.png'))"`

A3: `python -m arsenal.forensics.amprente arsenal/forensics/probe`

A4: `python -m pytest -q arsenal/forensics/test_amprente.py`

B: `cd reparare` apoi `python -m pytest -q` si `cd ..`.

Optional: `python -c "from arsenal.forensics.amprente import amprente_lenes; print(list(amprente_lenes('arsenal/forensics/probe')))"`

## Reparatii B
1. Mutarea return necunoscut dupa bucla.
2. Deschiderea in mod binar rb cu with.
3. Pastrarea primelor 16 caractere SHA-256, nu 8.
JURNAL_TESTE_B.txt contine rezultatele reale ale fiecarei etape, inclusiv erorile initiale. Testele si probele originale nu au fost modificate.

## Predare
Copiaza arsenal/forensics si reparare in depozitul Git de curs (nu suprascrie alte laboratoare). Din radacina depozitului:
```powershell
git add arsenal/forensics reparare
git commit -m "forensics: tip + amprenta cu with si teste; reparare suita"
git push
```
