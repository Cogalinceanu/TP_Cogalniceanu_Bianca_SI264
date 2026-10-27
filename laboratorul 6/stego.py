"""Ascunderea și recuperarea unui mesaj în pixelii unei imagini, prin LSB."""
import argparse
from pathlib import Path
from PIL import Image

MESAJ_IMPLICIT = b"FLAG{ascuns_in_pixeli}"


def ascunde(imagine_intrare, imagine_iesire, mesaj=MESAJ_IMPLICIT):
    img = Image.open(imagine_intrare).convert("RGB")
    pixeli = list(img.getdata())
    # Octetul NUL marchează sfârșitul mesajului.
    biti = "".join(f"{x:08b}" for x in mesaj + b"\x00")
    if len(biti) > len(pixeli) * 3:
        raise ValueError("Mesajul este prea mare pentru această imagine.")
    pixeli_nou = []
    index_bit = 0
    for r, g, b in pixeli:
        canale = [r, g, b]
        for i in range(3):
            if index_bit < len(biti):
                canale[i] = (canale[i] & ~1) | int(biti[index_bit])
                index_bit += 1
        pixeli_nou.append(tuple(canale))
    img.putdata(pixeli_nou)
    img.save(imagine_iesire, format="PNG")
    print("Mesaj ascuns în:", imagine_iesire)


def dezvaluie(imagine):
    pixeli = list(Image.open(imagine).convert("RGB").getdata())
    biti = []
    for r, g, b in pixeli:
        biti.extend((str(r & 1), str(g & 1), str(b & 1)))
    octeti = []
    for i in range(0, len(biti) - 7, 8):
        octet = int("".join(biti[i:i + 8]), 2)
        if octet == 0:
            break
        octeti.append(octet)
    mesaj = bytes(octeti)
    print("Mesaj recuperat:", mesaj.decode("utf-8", errors="replace"))
    return mesaj


def main():
    p = argparse.ArgumentParser(description="Steganografie LSB")
    sub = p.add_subparsers(dest="comanda", required=True)
    a = sub.add_parser("ascunde", help="ascunde mesajul într-o imagine")
    a.add_argument("intrare", nargs="?", default="probe/foto.jpg")
    a.add_argument("iesire", nargs="?", default="stego.png")
    a.add_argument("--mesaj", default=MESAJ_IMPLICIT.decode())
    d = sub.add_parser("dezvaluie", help="recuperează mesajul din stego.png")
    d.add_argument("imagine", nargs="?", default="stego.png")
    args = p.parse_args()
    if args.comanda == "ascunde":
        ascunde(args.intrare, args.iesire, args.mesaj.encode("utf-8"))
    else:
        dezvaluie(args.imagine)


if __name__ == "__main__":
    main()
