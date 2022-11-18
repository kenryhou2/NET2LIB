@echo off
ECHO setting up Tkinterdnd2
chdir /d .\setup\tkinterdnd2-master
START python setup.py install

ECHO once install is finished,
ECHO run "python NET2LIBconverter_windows.py"
chdir /d ..\..\
