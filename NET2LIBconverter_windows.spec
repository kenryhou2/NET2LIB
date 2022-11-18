# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['NET2LIBconverter_windows.py'],
             pathex=[],
             binaries=[],
             datas=[('src/dragndroplogo.png', 'src'), ('templates/ModelHeader_Public_Release.txt', 'templates'), ('lib/SIM2PSPICE_ANALOG.LIB', 'lib'), ('lib/SIM2PSPICE_DIGITAL.LIB', 'lib'), ('lib/SIM2PSPICE_MISC.LIB', 'lib'), ('lib/SIM2PSPICE_SPECIAL.LIB', 'lib'), ('src/ti_logo.png', 'src')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='NET2LIBconverter_windows',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
