# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Collect all data files
datas = [
    ('config/', 'config/'),
    ('src/', 'src/'),
    ('assets/', 'assets/'),
]

# Hidden imports that PyInstaller might miss
hiddenimports = [
    'PIL',
    'PIL.Image',
    'PIL.ImageTk',
    'selenium',
    'selenium.webdriver',
    'selenium.webdriver.chrome',
    'selenium.webdriver.common.by',
    'selenium.webdriver.support',
    'selenium.webdriver.support.ui',
    'selenium.webdriver.support.expected_conditions',
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.scrolledtext',
    'webbrowser',
    'subprocess',
    'threading',
    'datetime',
    'json',
    'os',
    'sys',
    # Custom modules from src directory
    'src.screenshot_capture',
    'src.screenshot_management',
    'src.qa_features',
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ScreenQA',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
# icon='assets/icon.ico'  # Optional: uncomment when icon file is available
)
