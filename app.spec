# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['source/app.py'],
             pathex=[],
             binaries=[],
             datas=[('./data/education.json', './data'), ('./data/plants.json', './data'), ('./data/store_state.json', './data')],
             hiddenimports=[('./source/model.py', './source'), './source/view.py', './source'), './source/controller.py', './source'), './source/MVCInterfaces.py', './source')],
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
          name='app',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
