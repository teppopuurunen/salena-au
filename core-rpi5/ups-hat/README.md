# UPS HAT (E) – valvonta ja hallittu sammutus

Waveshare UPS HAT (E) (WS-27966), I2C-väylä 1, osoite `0x2d`.

`ups_hat.py` lukee HATin 5 s välein ja
- lähettää arvot SignalK:hon UDP-deltoina (porttiin 20230, SignalK-datayhteys `ups-hat`)
- sammuttaa RPi:n hallitusti, kun ulkoinen virta puuttuu (USB-C < 4.5 V) **ja** akku on ≤ 20 % tai alin kenno on ≤ 3300 mV, kolmena peräkkäisenä lukemana.

## SignalK-polut

| Polku | Yksikkö |
|---|---|
| `electrical.batteries.ups.voltage` | V |
| `electrical.batteries.ups.current` | A (negatiivinen = purkautuu) |
| `electrical.batteries.ups.capacity.stateOfCharge` | 0–1 |
| `electrical.batteries.ups.capacity.remaining` | J |
| `electrical.batteries.ups.capacity.timeRemaining` | s (vain purkautuessa) |
| `electrical.batteries.ups.input.voltage` / `.current` / `.power` | V / A / W |
| `electrical.batteries.ups.externalPower` | true/false |
| `electrical.batteries.ups.cell1..4.voltage` | V |
| `electrical.batteries.ups.cellSpread` | V (suurin kenno − pienin; seuraa, kasvaako ero) |

## Asennus

SignalK (OpenPlotter, `~/.signalk/settings.json`) tarvitsee UDP-datayhteyden:
tyyppi *Signal K*, *UDP*, portti `20230`, id `ups-hat`.

```bash
sudo cp ups-hat.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now ups-hat
journalctl -u ups-hat -f
```

Rajat muutetaan `ups-hat.service`:n `Environment=`-riveillä.

## UPS_CUT_OUTPUT

Oletuksena pois. Kun päällä, skripti pyytää ennen sammutusta HATia katkaisemaan lähdön
(rekisteri `0x01` = `0x55`). HAT palauttaa virran, kun ulkoinen syöttö palaa, jolloin RPi
käynnistyy itsestään. Ilman tätä RPi jää sammuneeksi, kunnes virta katkaistaan ja kytketään uudelleen.
Testaa laiturissa ennen kuin luotat tähän.
