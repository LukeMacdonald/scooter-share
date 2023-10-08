#!/usr/bin/env python3

import argparse
import qrcode

parser = argparse.ArgumentParser(prog="make_qr_codes.py",
                                 description="Generate QR codes for scooters")
parser.add_argument("ids", metavar="id", type=int, nargs="+")
args = parser.parse_args()

for id in args.ids:
    qrcode.make(str(id)).save(f"{id}.png")
