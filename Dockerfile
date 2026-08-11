FROM docker.io/library/python:3.12-bookworm

RUN apt-get update && apt-get install -y git 

RUN apt install -y qt6-base-dev && apt-get install -y libxcb-cursor-dev

RUN pip install PySide6 && pip install pyqtgraph

RUN pip install git+https://github.com/lucyhaddad-dls/sample-absorption.git
