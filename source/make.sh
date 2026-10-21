#!/bin/sh
# Rebuilds pages 01-19 and 21-30 plus the index into ../site
# (page 20, retaining walls, is a hand-built file kept in ../site)
cd "$(dirname "$0")"
python3 build.py ../site pa pb pc pd pe pf pg ph pi pj
python3 index_build.py ../site
