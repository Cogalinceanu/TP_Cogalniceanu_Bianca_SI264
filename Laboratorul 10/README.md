# Laboratorul 10 – Functii si exceptii

**UTM / FCIM / Securitate informationala / Tehnici de programare**

Proiect complet pentru Lucrarea A (A1–A4) si Lucrarea B (B1–B4), realizat pe baza jurnalului `auth.log` furnizat. Foloseste Python 3.9+; pentru rularea programelor nu sunt necesare pachete externe.

## Cum se deschide

1. Dezarhiveaza `Laboratorul_10.zip`.
2. Deschide folderul **Laboratorul_10** in Visual Studio Code (File > Open Folder).
3. Deschide Terminal > New Terminal, in radacina folderului, unde se afla acest README.
4. Ruleaza comenzile de mai jos din acea radacina (nu din interiorul folderului `aparare`).

## Lucrarea A

```powershell
python -m arsenal.aparare.parse_auth arsenal/aparare/start/auth.log
```

Rezultat asteptat:

```text
Esecuri de autentificare: 15
 203.0.113.9: 13
 198.51.100.7: 2
```

A1: `esec(linie)` extrage utilizatorul si IP-ul sau intoarce `None`. A2: `citeste_esecuri(cale)` ignora randurile nevalide si trateaza fisierul lipsa. A3: `pe_ip(esecuri)` intoarce `Counter`. A4: `main()` afiseaza rezumatul.

## Lucrarea B

```powershell
python -m arsenal.aparare.detector arsenal/aparare/start/auth.log
python -m arsenal.aparare.detector arsenal/aparare/start/auth.log --prag 2
python -m arsenal.aparare.detector arsenal/aparare/start/auth.log --json
python -m arsenal.aparare.detector arsenal/aparare/start/auth.log --prag 2 --json
```

Cu pragul implicit 10, suspect este doar `203.0.113.9` (13 incercari). Cu `--prag 2`, ambele IP-uri sunt suspecte. JSON-ul contine `esecuri`, `pe_ip`, `suspecti`.

B1: `suspecti(counts, prag=10)` sorteaza descrescator si valideaza pragul. B2: `raise ValueError` pentru prag invalid. B3: `argparse` si JSON. B4: teste cu pytest.

## Teste si exceptii

Instaleaza pytest, daca nu este instalat:

```powershell
python -m pip install -r requirements.txt
python -m pytest -q arsenal/aparare/test_detector.py
```

Verifica explicit exceptia ceruta in fisa (comanda produce intentionat traceback):

```powershell
python -c "from arsenal.aparare.detector import suspecti; suspecti({}, 0)"
```

Verifica tratarea unui fisier lipsa:

```powershell
python -m arsenal.aparare.parse_auth fisier_inexistent.log
```

## Fisiere

- `arsenal/aparare/start/auth.log` – jurnalul original primit.
- `arsenal/aparare/parse_auth.py` – Lucrarea A.
- `arsenal/aparare/detector.py` – Lucrarea B.
- `arsenal/aparare/test_detector.py` – teste automate.
- `rapoarte/raport_prag_10.json` si `rapoarte/raport_prag_2.json` – exemple generate.
- `requirements.txt` – dependinta pentru teste.

## Predare prin Git

Din radacina depozitului tau Git, copiaza folderul `arsenal/aparare` din acest proiect in folderul `arsenal/aparare` al depozitului (fara a sterge alte laboratoare), apoi ruleaza:

```powershell
git add arsenal/aparare
git commit -m "aparare: parse_auth robust + detector brute force"
git push
```

**Nota:** Optiunile `--fereastra`, `--top` si citirea unui jurnal real sunt marcate optional in fisa; nu sunt cerinte obligatorii pentru lucrarile A si B. Nu analiza jurnale ale unor sisteme fara autorizatie.
