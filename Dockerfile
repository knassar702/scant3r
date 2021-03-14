FROM       python
COPY       . /scant3r
WORKDIR    /scant3r
RUN        pip install -r requirements.txt
ENV        SHELL=/bin/bash
CMD        ["python","scant3r.py","--a"]
