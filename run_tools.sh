#!/bin/bash
echo http://localhost:4000/search?u=hello | ~/.local/bin/scant3r -m xss --proxy http://localhost:8080/
