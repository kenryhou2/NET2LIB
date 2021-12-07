@echo off
ECHO converting NET2LIBconverter_windows.py to exe using pyinstaller
ECHO NET2LIBconverter_windows.exe will be located in ./dist/NET2LIBconverter_windows.exe as a standalone file.
ECHO note: LIB output will be in same directory as Net file input
START pyinstaller --onefile -w --add-data src/dragndroplogo.png;src --add-data templates/ModelHeader_Public_Release.txt;templates NET2LIBconverter_windows.py