"""
Gestakomur:
Með gestakomum er átt við hve margir gestir koma til þess að gista. Hver gestur kemur aðeins einu sinni og skal aðeins teljast einu sinni þó svo hann gisti fleiri en eina nótt.
Dæmi: 2 hópar frá Austurríki koma og gista.
Hópur 1 telur þrjá gesti sem gista í fjórar nætur.
Hópur 2 telur tvo gesti sem gista í tvær nætur.
Gestakomurnar sem tilheyra Austurríki eru þá 3 gestir + 2 gestir = 5 gestakomur 

Gistinætur:
Með gistinóttum er átt við hve margar nætur gestirnir gista. Allar nætur sem gestirnir gista eru taldar miðað við hvern gest.
Dæmi: 2 hópar frá Austurríki koma og gista.
Hópur 1 telur þrjá gesti sem gista í fjórar nætur.
Hópur 2 telur tvo gesti sem gista í tvær nætur.
Gistinæturnar fyrir Austurríki eru þá (3 gestir * 4 nætur) + (2 gestir * 2 nætur) = 16 gistinætur 

Útleigð herbergi:
Með útleigðum herbergjum er átt við hversu mörg herbergi voru leigð út samanlagt yfir mánuðinn.
Dæmi: 2 hópar frá Austurríki koma og gista.
Hópur 1 telur þrjá gesti sem gista í fjórar nætur í einu herbergi.
Hópur 2 telur tvo gesti sem gista í tvær nætur í einu herberi.
Fjöldi útleigðra herbergja yfir mánuðinn er þá (1 herbergi * 4 nætur) + (1 herbergi * 2 nætur) = 6 útleigð herbergi 
"""
import argparse
import csv
from collections import defaultdict
from datetime import datetime, timedelta
import phonenumbers
from phonenumbers import COUNTRY_CODE_TO_REGION_CODE as C2R
from utils.regions import R2N


def read_reservations(rfile):
    lines = []
    reservations = csv.DictReader(rfile, delimiter=',', quotechar='"')
    for res in reservations:
        if "Canceled" not in res["Status"]:
            lines.append(parse_reservation(res))
    return lines


def parse_reservation(res):
    try:
        pn = phonenumbers.parse(res["Contact"])
        country = C2R[pn.country_code][0]
    except Exception:
        country = "unknown"

    return {
        "start": datetime.strptime(res["Start date"], "%m/%d/%Y"),
        "end": datetime.strptime(res["End date"], "%m/%d/%Y"),
        "country": country,
        "guests": int(res["# of adults"]),
        "nights": int(res["# of nights"]),
    }


def calculate_stats(reservations, month=None):
    country_guests = defaultdict(lambda: 0)
    country_nights = defaultdict(lambda: 0)
    rooms = 0
    total_nights = 0
    for line in reservations:
        country = line["country"]
        nights = line["nights"]
        if month:
            start = line["start"]
            end = line["end"]
            if start.month != month:
                start = (start.replace(day=1) + timedelta(days=32)).replace(day=1)
            if end.month != month:
                end = end.replace(day=1)
            nights = (end - start).days

        if nights > 0:
            rooms += nights
            country_guests[country] += line["guests"]
            country_nights[country] += nights * line["guests"]
            total_nights += nights * line["guests"]
    return {
        "countries": dict((key, {
            "guests": country_guests[key], 
            "nights": country_nights[key],
        }) for key in country_guests.keys()),
        "total_nights": total_nights,
        "rooms": rooms,
    }
    

def print_stats(stats):
    print("-"*10)
    for key, cstat in stats["countries"].items():
        print(f"{R2N.get(key, key):<50}\t{cstat['guests']:>5}\t{cstat['nights']:>5}")

    print("-"*10)
    print("Útleigð herbergi:", stats["rooms"])
    print("Heildarfjöldi gistinátta:", stats["total_nights"]) 


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("reservations")
    args = parser.parse_args()

    with open(args.reservations, newline="") as csvfile:
        lines = read_reservations(csvfile)
    stats = calculate_stats(lines)
    print_stats(stats)


if __name__ == "__main__":
    main()
