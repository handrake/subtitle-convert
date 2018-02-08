# -*- mode: python -*-
import os
from distutils.sysconfig import get_python_lib

block_cipher = None

version = "0.0.1"

a = Analysis(['subtitle_convert/__main__.py'],
             pathex=[],
             datas=[('subtitle_convert/images/icons/closed-caption-logo.png', 'subtitle_convert/images/icons'),
                    ('subtitle_convert/images/icons/closed-caption-logo.ico', 'subtitle_convert/images/icons'),
                    ('subtitle_convert/main_gui.ui', 'subtitle_convert'),
                    ('subtitle_convert/process_gui.ui', 'subtitle_convert'),
                    ('subtitle_convert/information_gui.ui', 'subtitle_convert')],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='subtitle_convert',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False,
          icon='subtitle_convert\images\icons\closed-caption-logo.ico')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               name='subtitle_convert'+'-'+version,
               strip=False,
               upx=True)
