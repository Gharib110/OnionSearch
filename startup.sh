#!/bin/bash

echo "Running ..."

nohup tor --CookieAuthentication 0 --HashedControlPassword "" --ControlPort 0 --ControlSocket 0 --ClientOnly 1 --NewCircuitPeriod 15 --MaxCircuitDirtiness 15 --NumEntryGuards 8 --PidFile ./torfleet/pids/tor.pid --SocksPort 127.0.0.1:9050 --Log "warn file ./torfleet/log/warnings.log" --Log "err file ./torfleet/log/errors.log" --DataDirectory ./torfleet/data/tor/ > ./torfleet/log/tor.log 2>&1 &

python3 ./app.py
