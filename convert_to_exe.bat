@echo off
ECHO converting NET2LIBconverter_windows.py to exe using pyinstaller
ECHO NET2LIBconverter_windows.exe will be located in ./dist/NET2LIBconverter_windows.exe as a standalone file.
ECHO note: LIB output will be in same directory as Net file input
ECHO remember to use identifiers for extra added data or files within your python code! See try-catch-except blocks.
START pyinstaller --onefile -w --add-data src/dragndroplogo.png;src --add-data templates/ModelHeader_Public_Release.txt;templates --add-data lib/SIM2PSPICE_ANALOG.LIB;lib --add-data lib/SIM2PSPICE_DIGITAL.LIB;lib --add-data lib/SIM2PSPICE_MISC.LIB;lib --add-data lib/SIM2PSPICE_SPECIAL.LIB;lib --add-data src/ti_logo.png;src NET2LIBconverter_windows.py