#!/usr/bin/env python3
"""Salena AU – Waveshare UPS HAT (E) (WS-27966) -valvonta.

- Lukee HATin I2C-rekisterit (väylä 1, osoite 0x2d)
- Lähettää arvot SignalK:hon UDP-deltoina (SignalK-datayhteys "ups-hat", UDP-portti 20230)
- Sammuttaa RPi:n hallitusti, kun ulkoinen virta puuttuu ja akku on vähissä

Ajetaan systemd-palveluna rootina (ups-hat.service), koska sammutus vaatii root-oikeudet.
"""

import json
import logging
import os
import socket
import subprocess
import time

from smbus2 import SMBus, i2c_msg

I2C_BUS = 1
ADDR = 0x2D

SIGNALK_UDP = ("127.0.0.1", int(os.environ.get("UPS_SK_PORT", "20230")))
SK_BASE = "electrical.batteries.ups"

INTERVAL_S = 5

# Sammutusehdot (vain kun ulkoinen virta puuttuu)
EXT_POWER_MIN_V = 4.5          # USB-C-sisäänmenon alaraja, jonka alla virta katsotaan puuttuvaksi
SHUTDOWN_SOC = int(os.environ.get("UPS_SHUTDOWN_SOC", "20"))          # %
SHUTDOWN_CELL_MV = int(os.environ.get("UPS_SHUTDOWN_CELL_MV", "3300"))  # alin kenno, mV
CONFIRM_READS = 3              # montako peräkkäistä lukemaa ehdon pitää täyttyä

# Jos 1: ennen sammutusta pyydetään HATia katkaisemaan lähtö (rekisteri 0x01 = 0x55).
# HAT palauttaa virran, kun ulkoinen syöttö palaa, jolloin RPi käynnistyy itsestään.
# Testaa ennen kuin otat käyttöön.
CUT_OUTPUT = os.environ.get("UPS_CUT_OUTPUT", "0") == "1"

log = logging.getLogger("ups-hat")


def read_block(bus, reg, n):
    w = i2c_msg.write(ADDR, [reg])
    r = i2c_msg.read(ADDR, n)
    bus.i2c_rdwr(w, r)
    return list(r)


def u16(b, i):
    return b[i] | (b[i + 1] << 8)


def s16(b, i):
    v = u16(b, i)
    return v - 0x10000 if v & 0x8000 else v


def read_ups(bus):
    status = read_block(bus, 0x02, 1)[0]
    vbus = read_block(bus, 0x10, 6)
    batt = read_block(bus, 0x20, 12)
    cells = read_block(bus, 0x30, 8)
    tte = u16(batt, 8)   # min, 0xffff = ei arviota
    ttf = u16(batt, 10)  # min
    return {
        "status": status,
        "in_v": u16(vbus, 0) / 1000,
        "in_a": u16(vbus, 2) / 1000,
        "in_w": u16(vbus, 4) / 1000,
        "bat_v": u16(batt, 0) / 1000,
        "bat_a": s16(batt, 2) / 1000,       # negatiivinen = purkautuu
        "soc": u16(batt, 4),                # %
        "remaining_mah": u16(batt, 6),
        "tte_min": None if tte == 0xFFFF else tte,
        "ttf_min": None if ttf == 0xFFFF else ttf,
        "cells_mv": [u16(cells, i) for i in range(0, 8, 2)],
    }


def to_delta(d):
    vals = [
        (f"{SK_BASE}.voltage", d["bat_v"]),
        (f"{SK_BASE}.current", d["bat_a"]),
        (f"{SK_BASE}.capacity.stateOfCharge", d["soc"] / 100),
        (f"{SK_BASE}.capacity.remaining", d["remaining_mah"] * 3.6 * d["bat_v"]),  # J
        (f"{SK_BASE}.input.voltage", d["in_v"]),
        (f"{SK_BASE}.input.current", d["in_a"]),
        (f"{SK_BASE}.input.power", d["in_w"]),
        (f"{SK_BASE}.externalPower", d["in_v"] >= EXT_POWER_MIN_V),
    ]
    if d["tte_min"] is not None:
        vals.append((f"{SK_BASE}.capacity.timeRemaining", d["tte_min"] * 60))
    for i, mv in enumerate(d["cells_mv"], 1):
        vals.append((f"{SK_BASE}.cell{i}.voltage", mv / 1000))
    return {
        "updates": [{
            "$source": "ups-hat",
            "values": [{"path": p, "value": v} for p, v in vals],
        }]
    }


def shutdown(reason):
    log.warning("SAMMUTUS: %s", reason)
    if CUT_OUTPUT:
        try:
            with SMBus(I2C_BUS) as bus:
                bus.write_byte_data(ADDR, 0x01, 0x55)
            log.warning("HATin lähdön katkaisu pyydetty")
        except OSError as e:
            log.error("Lähdön katkaisupyyntö epäonnistui: %s", e)
    subprocess.run(["systemctl", "poweroff"], check=False)


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    low_count = 0
    last_ext = None
    log.info("Käynnistetty: SoC-raja %d %%, kennoraja %d mV, CUT_OUTPUT=%s",
             SHUTDOWN_SOC, SHUTDOWN_CELL_MV, CUT_OUTPUT)

    with SMBus(I2C_BUS) as bus:
        while True:
            try:
                d = read_ups(bus)
            except OSError as e:
                log.error("I2C-lukuvirhe: %s", e)
                time.sleep(INTERVAL_S)
                continue

            try:
                sock.sendto(json.dumps(to_delta(d)).encode(), SIGNALK_UDP)
            except OSError as e:
                log.error("SignalK UDP -lähetys epäonnistui: %s", e)

            ext = d["in_v"] >= EXT_POWER_MIN_V
            if ext != last_ext:
                log.info("Ulkoinen virta %s (%.2f V), akku %d %%",
                         "PÄÄLLÄ" if ext else "POIS", d["in_v"], d["soc"])
                last_ext = ext

            min_cell = min(d["cells_mv"])
            if not ext and (d["soc"] <= SHUTDOWN_SOC or min_cell <= SHUTDOWN_CELL_MV):
                low_count += 1
                log.warning("Akku vähissä ilman ulkoista virtaa (%d %%, alin kenno %d mV) %d/%d",
                            d["soc"], min_cell, low_count, CONFIRM_READS)
                if low_count >= CONFIRM_READS:
                    shutdown(f"SoC {d['soc']} %, alin kenno {min_cell} mV")
                    return
            else:
                low_count = 0

            time.sleep(INTERVAL_S)


if __name__ == "__main__":
    main()
