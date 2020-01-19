#!/usr/bin/env bash
python3 scrapers/alberta/alberta.py &
python3 scrapers/nova_scotia/nova_scotia.py &
python3 scrapers/new_brunswick/new_brunswick.py &
python3 scrapers/ontario/ontario.py
