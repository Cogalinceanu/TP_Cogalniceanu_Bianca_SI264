# Laboratorul 6 – Python

## Pregătire
```bash
pip install pillow pytest
python probe/pregateste.py
```
Folosește fișierele `probe/` generate de scriptul oferit la laborator.

## Lucrarea A
```bash
python -m arsenal.forensics.decode "U2FsdXQ="
python -m arsenal.forensics.decode probe/mesaj.txt --fisier
python -m arsenal.forensics.decode probe/xor.bin --fisier --xor
python -m arsenal.forensics.decode HASH_DIN_HASHURI --hash --wordlist probe/wordlist.txt
pytest -q
```
Dacă Python nu găsește pachetul, adaugă fișierele goale `arsenal/__init__.py` și `arsenal/forensics/__init__.py` sau rulează din rădăcina proiectului.

## Lucrarea B
```bash
python forensics.py probe/foto.jpg --exif
python forensics.py probe/ascuns.png --strings --carve
python stego.py ascunde probe/foto.jpg stego.png
python stego.py dezvaluie stego.png
```

## Observații
- `probe/wordlist.txt` trebuie să existe pentru spargerea hash-urilor; dacă scriptul de pregătire nu îl generează, creează o listă locală cu parole de test.
- Nu se pot completa din fișa laboratorului valorile exacte ale parolei, cheii XOR, GPS-ului sau arhivei: acestea sunt create de `probe/pregateste.py` pe calculatorul tău.
- Analizează numai fișierele proprii sau fișierele pregătite pentru laborator.
