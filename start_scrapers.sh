#!/usr/bin/env bash
python scrapers/alberta/alberta.py &
python scrapers/nova_scotia/nova_scotia.py &
python scrapers/new_brunswick/new_brunswick.py &
python scrapers/ontario/ontario.py