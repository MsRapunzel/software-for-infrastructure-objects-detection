# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/resources/model/building_segmentation.pkl', 'resources/model'),
        ('src/resources/demo_images', 'resources/demo_images'),
        ('src/resources/icons/app_icon.icns', 'resources/icons'),
        ('src/resources/logs', 'resources/logs'),
    ],
    hiddenimports=['PyQt6.sip'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Infrastructure Objects Detector',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Infrastructure Objects Detector',
)

app = BUNDLE(
    coll,
    name='Infrastructure Objects Detector.app',
    icon='src/resources/icons/app_icon.icns',
    bundle_identifier='com.yourdomain.infrastructuredetector',
    info_plist={
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.15',
        'CFBundleTypeIconFile': 'src/resources/icons/app_icon.icns',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0', 
    },
)