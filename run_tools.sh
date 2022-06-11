#!/bin/bash
pip3 install .
printf 'http://localhost:5000/?u=hello\nhttp://example.com\nhttp://localhost:5000/dat/?ff=1' | ~/.local/bin/scant3r -m all -o data.json # --proxy http://localhost:8080i/
