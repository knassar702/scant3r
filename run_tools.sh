#!/bin/bash
pip3 install .
echo http://localhost:5000/?u=hello | ~/.local/bin/scant3r -m xss # --proxy http://localhost:8080i/
