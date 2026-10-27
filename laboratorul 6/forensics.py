"""Analiză de fișiere: magic bytes, strings, EXIF/GPS și file carving."""
import argparse
import re
import zipfile
from pathlib import Path
from PIL import Image, ExifTags


def tip_real(cale):
    cap = Path(cale).read_bytes()[:8]
    if cap.startswith(b"%PDF"):
        return "pdf"
    if cap.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if cap.startswith(b"\xff\xd8\xff"):
        return "jpeg"
    if cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    if cap.startswith((b"GIF87a", b"GIF89a")):
        return "gif"
    return "necunoscut (semnătură: " + cap.hex() + ")"


def extrage_strings(cale, lungime_minima=4):
    date = Path(cale).read_bytes()
    return [m.decode("ascii", errors="replace")
            for m in re.findall(rb"[ -~]{" + str(lungime_minima).encode() + rb",}", date)]


def rational_numar(v):
    """Transformă valorile EXIF de tip int sau Rational în float."""
    try:
        return float(v)
    except (TypeError, ValueError, ZeroDivisionError):
        return float(v[0]) / float(v[1])


def coordonate_zecimale(valori, emisfera):
    grade, minute, secunde = [rational_numar(x) for x in valori]
    rezultat = grade + minute / 60 + secunde / 3600
    if emisfera in ("S", "W"):
        rezultat = -rezultat
    return rezultat


def citeste_exif_gps(cale):
    img = Image.open(cale)
    exif = img.getexif()
    for tag_id, valoare in exif.items():
        print(ExifTags.TAGS.get(tag_id, tag_id), "=", valoare)

    gps_id = next((i for i, nume in ExifTags.TAGS.items() if nume == "GPSInfo"), 34853)
    gps = exif.get_ifd(gps_id) if gps_id in exif else {}
    if not gps:
        print("Nu au fost găsite date GPS în EXIF.")
        return
    gps_nume = {ExifTags.GPSTAGS.get(k, k): v for k, v in gps.items()}
    print("GPS:", gps_nume)
    lat = gps_nume.get("GPSLatitude")
    lat_ref = gps_nume.get("GPSLatitudeRef")
    lon = gps_nume.get("GPSLongitude")
    lon_ref = gps_nume.get("GPSLongitudeRef")
    if lat and lat_ref and lon and lon_ref:
        print("Latitudine zecimală:", coordonate_zecimale(lat, lat_ref))
        print("Longitudine zecimală:", coordonate_zecimale(lon, lon_ref))


def extrage_zip(cale, iesire="gasit.zip"):
    date = Path(cale).read_bytes()
    pozitie = date.find(b"PK\x03\x04")
    if pozitie == -1:
        print("Semnătura ZIP nu a fost găsită.")
        return None
    Path(iesire).write_bytes(date[pozitie:])
    print("Arhiva extrasă de la octetul", pozitie, "în", iesire)
    if zipfile.is_zipfile(iesire):
        with zipfile.ZipFile(iesire) as arhiva:
            print("Fișiere în arhivă:", arhiva.namelist())
            arhiva.extractall("extras_zip")
            print("Conținutul a fost extras în folderul extras_zip/")
    else:
        print("S-au găsit octeți ZIP, dar arhiva extrasă pare incompletă sau invalidă.")
    return pozitie


def main():
    p = argparse.ArgumentParser(description="Instrumente de forensics pentru fișiere proprii/de laborator")
    p.add_argument("fisier", help="calea către fișier")
    p.add_argument("--strings", action="store_true", help="afișează șirurile imprimabile")
    p.add_argument("--exif", action="store_true", help="afișează EXIF și GPS pentru o imagine")
    p.add_argument("--carve", action="store_true", help="caută și extrage arhiva ZIP lipită la coadă")
    a = p.parse_args()
    print("Tip real:", tip_real(a.fisier))
    if a.strings:
        for text in extrage_strings(a.fisier):
            print(text)
    if a.exif:
        citeste_exif_gps(a.fisier)
    if a.carve:
        extrage_zip(a.fisier)


if __name__ == "__main__":
    main()
