# Laboratorul 6 – Informații invizibile: forensics și steganografie

## Lucrarea A – Decoder universal
- Straturi găsite în `probe/mesaj.txt`: completează cu rezultatele afișate de program.
- Cheia XOR găsită în `probe/xor.bin`: completează cheia și textul afișat.
- Hash/parolă: completează algoritmul și parola, dacă aceasta se află în `probe/wordlist.txt`.
- Teste: `pytest -q` (notează rezultatul real).

## Lucrarea B – Forensics
- Tipurile reale ale fișierelor: completează cu output-ul `forensics.py`.
- Metadate EXIF/GPS din `probe/foto.jpg`: copiază valorile afișate.
- Arhiva ascunsă în `probe/ascuns.png`: notează fișierele listate/extrase.
- Mesajul LSB recuperat din `stego.png`: `FLAG{ascuns_in_pixeli}` (dacă folosești mesajul implicit).

## Concluzie
În această lucrare am utilizat Python pentru a identifica și decoda date, a analiza semnături și metadate de fișiere, a recupera o arhivă concatenată și a ascunde/recupera un mesaj prin metoda LSB. Rezultatele exacte depind de fișierele generate local de scriptul de pregătire.
