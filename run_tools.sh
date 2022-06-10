#!/bin/bash
pip3 install .
echo http://localhost:5000/?name=hello | ~/.local/bin/scant3r -m xss # --proxy http://localhost:8080i/
