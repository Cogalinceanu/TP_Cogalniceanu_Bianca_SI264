import argparse
import base64
import binascii
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]


def ghici_strat(s: str) -> str:
    """Ghicește codarea după forma șirului."""
    if re.search(r"%[0-9a-fA-F]{2}", s):
        return "url"

    # Verificăm hex înainte de Base64.
    if s and len(s) % 2 == 0 and re.fullmatch(r"[0-9a-fA-F]+", s):
        return "hex"

    if (
        s
        and len(s) % 4 == 0
        and re.fullmatch(r"[A-Za-z0-9+/]*={0,2}", s)
    ):
        try:
            base64.b64decode(s, validate=True)
            return "base64"
        except (binascii.Error, ValueError):
            pass

    return "necunoscut"


def desfa(s: str):
    """Întoarce (numele_stratului, rezultat_bytes)."""
    strat = ghici_strat(s)

    if strat == "base64":
        rezultat = base64.b64decode(s, validate=True)
    elif strat == "hex":
        rezultat = bytes.fromhex(s)
    elif strat == "url":
        rezultat = unquote(s).encode("utf-8")
    else:
        rezultat = s.encode("utf-8")

    return strat, rezultat


def citibil(b: bytes) -> bool:
    """Verifică dacă toți octeții sunt caractere ASCII imprimabile."""
    return all(32 <= c <= 126 for c in b)


def decodeaza_straturi(valoare: str, maxim: int = 8):
    """
    Decodifică succesiv straturile Base64, hex și URL.

    Continuă dacă rezultatul este o altă codare recunoscută,
    chiar dacă rezultatul intermediar este text imprimabil.

    Întoarce pașii executați și rezultatul final.
    """
    pasi = []
    curent = valoare
    rezultat_final = valoare

    for _ in range(maxim):
        strat, rezultat = desfa(curent)

        if strat == "necunoscut":
            break

        text_rezultat = rezultat.decode("utf-8", errors="replace")

        pasi.append({
            "strat": strat,
            "rezultat": text_rezultat
        })

        # Păstrăm rezultatul ultimei decodificări.
        rezultat_final = text_rezultat

        # Pentru următorul strat avem nevoie de text ASCII.
        try:
            urmator = rezultat.decode("ascii")
        except UnicodeDecodeError:
            break

        # Evităm repetarea aceleiași valori.
        if urmator == curent:
            break

        # Dacă rezultatul nu reprezintă altă codare,
        # am ajuns la mesajul final.
        if ghici_strat(urmator) == "necunoscut":
            break

        # Continuăm chiar dacă textul intermediar este imprimabil.
        curent = urmator

    return pasi, rezultat_final


def scor_xor(text: str) -> int:
    """
    Atribuie un scor candidaților XOR.
    Textele care conțin FLAG{ primesc prioritate.
    """
    scor = 0

    if "FLAG{" in text.upper():
        scor += 10000

    # Literele și cifrele sunt frecvente în texte obișnuite.
    litere = sum(c.isalpha() for c in text)
    cifre = sum(c.isdigit() for c in text)
    spatii = text.count(" ")

    if text:
        scor += int(100 * (litere + cifre) / len(text))
        scor += min(spatii * 2, 30)

    # Penalizăm șirurile cu multe simboluri neobișnuite.
    simboluri_neobisnuite = sum(
        not (c.isalnum() or c.isspace() or c in "_{}.,:;!?'-")
        for c in text
    )
    scor -= simboluri_neobisnuite * 5

    # Bonus pentru cuvinte și expresii frecvente.
    text_mic = text.lower()
    cuvinte_frecvente = [
        "the", "and", "this", "that",
        "este", "pentru", "mesaj", "secret"
    ]

    for cuvant in cuvinte_frecvente:
        if cuvant in text_mic:
            scor += 20

    return scor


def sparge_xor(cale: Path, limita: int = 20):
    """
    Încearcă toate cele 256 de chei XOR de un octet.

    Returnează cei mai promițători candidați, ordonați după scor.
    """
    date = cale.read_bytes()
    rezultate = []

    for cheie in range(256):
        clar = bytes(octet ^ cheie for octet in date)

        if not clar:
            continue

        # XOR poate produce și date binare.
        if not citibil(clar):
            continue

        text = clar.decode("ascii")
        rezultate.append({
            "cheie": cheie,
            "text": text,
            "scor": scor_xor(text)
        })

    rezultate.sort(
        key=lambda item: item["scor"],
        reverse=True
    )

    return rezultate[:limita]


def algoritm_hash(tinta: str) -> str:
    """Identifică algoritmul după lungimea hash-ului."""
    return {
        32: "md5",
        40: "sha1",
        64: "sha256"
    }.get(len(tinta), "")


def sparge_hash(tinta: str, wordlist: Path):
    """
    Compară hash-ul fiecărui cuvânt din wordlist
    cu hash-ul țintă.
    """
    algoritm = algoritm_hash(tinta)

    if not algoritm:
        raise ValueError(
            "Lungime de hash necunoscută. "
            "Se acceptă MD5=32, SHA1=40 sau SHA256=64."
        )

    functie = getattr(hashlib, algoritm)

    with wordlist.open("r", encoding="latin1") as fisier:
        for cuvant in fisier:
            cuvant = cuvant.strip()

            hash_cuvant = functie(
                cuvant.encode("utf-8")
            ).hexdigest()

            if hash_cuvant.lower() == tinta.lower():
                return cuvant

    return None


def main():
    parser = argparse.ArgumentParser(
        description="Decoder universal pentru laboratorul 6"
    )

    parser.add_argument(
        "intrare",
        help="Șirul de decodat sau calea către fișier"
    )

    parser.add_argument(
        "--fisier",
        action="store_true",
        help="Intrarea este o cale de fișier"
    )

    parser.add_argument(
        "--xor",
        action="store_true",
        help="Încearcă toate cheile XOR de un octet"
    )

    parser.add_argument(
        "--hash",
        dest="hash_mode",
        action="store_true",
        help="Intrarea este un hash de parolă"
    )

    parser.add_argument(
        "--wordlist",
        default="probe/wordlist.txt",
        help="Calea către lista de parole"
    )

    parser.add_argument(
        "--json",
        dest="json_path",
        default="arsenal/forensics/fisa.json",
        help="Fișierul JSON în care se salvează rezultatul"
    )

    args = parser.parse_args()

    if args.xor:
        cale = Path(args.intrare)

        rezultate = sparge_xor(cale)

        rezultat_json = {
            "mod": "xor",
            "rezultate": rezultate
        }

        if not rezultate:
            print("Nu au fost găsite variante ASCII imprimabile.")
        else:
            for item in rezultate:
                print(
                    f"cheie: {item['cheie']} | "
                    f"scor: {item['scor']} | "
                    f"text: {item['text']}"
                )

    elif args.hash_mode:
        tinta = args.intrare.strip()

        parola = sparge_hash(
            tinta,
            Path(args.wordlist)
        )

        rezultat_json = {
            "mod": "hash",
            "algoritm": algoritm_hash(tinta),
            "parola": parola
        }

        if parola is not None:
            print("găsit:", parola)
        else:
            print("parola nu se află în wordlist")

    else:
        if args.fisier:
            cale_intrare = Path(args.intrare)
            data = cale_intrare.read_bytes()

            try:
                valoare = data.decode("utf-8").strip()
            except UnicodeDecodeError:
                valoare = data.decode("latin1").strip()
        else:
            valoare = args.intrare

        strat_initial = ghici_strat(valoare)

        pasi, rezultat_final = decodeaza_straturi(valoare)

        rezultat_json = {
            "intrare": args.intrare,
            "strat_initial": strat_initial,
            "pasi": pasi,
            "rezultat_final": rezultat_final
        }

        print("strat:", strat_initial)

        for nr, pas in enumerate(pasi, 1):
            print(
                f"pas {nr} ({pas['strat']}): "
                f"{pas['rezultat']}"
            )

        print("rezultat final:", rezultat_final)

    # Salvăm rezultatul în fișierul JSON.
    cale_json = Path(args.json_path)
    cale_json.parent.mkdir(parents=True, exist_ok=True)

    cale_json.write_text(
        json.dumps(
            rezultat_json,
            ensure_ascii=False,
            indent=4
        ),
        encoding="utf-8"
    )

    print("Fișa JSON a fost salvată în:", cale_json)


if __name__ == "__main__":
    main()